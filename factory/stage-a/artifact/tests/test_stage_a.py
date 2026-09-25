"""Offline unittest suite for the synthetic Stage A prototype."""
from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from persona_stage_a import (  # noqa: E402
    CAPABILITIES, MOCK_LABEL, CappedChild, ChangeControl, EpisodeLedger,
    FakeChannel, FakeClock, GoalJournal, ModelRouter, OperationPolicy,
    PersonaRepository, StageStop, StopGate, WakeEngine, build_summary,
    compose_context, deletion_manifest, may_report_complete, read_jsonl,
    run_demo, seed_synthetic, teardown_disposable_tree,
)

BUILD_ROOT = Path(os.environ["STAGE_A_ROOT"])


class StageATest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = BUILD_ROOT / "project" / "test-data" / self._testMethodName
        if self.root.exists():
            shutil.rmtree(self.root)
        self.root.mkdir(parents=True)

    def tearDown(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)

    def seeded(self):
        policy = OperationPolicy()
        repo = PersonaRepository(self.root, policy)
        ids = seed_synthetic(repo)
        return policy, repo, ids

    def test_01_append_only_ids_survive_reopen_and_correction_is_new_event(self) -> None:
        policy, repo, ids = self.seeded()
        ledger_path = repo.episodes.path("red")
        before = ledger_path.read_bytes()
        reopened = EpisodeLedger(self.root, policy)
        reopened_events = reopened.read("red")
        self.assertEqual([e["id"] for e in reopened_events], ids["red"])
        self.assertTrue(all(e["source"].startswith("synthetic:") and e["visibility"] == "private" for e in reopened_events))
        self.assertEqual(reopened_events[0]["event_type"], "identity")
        summary = build_summary(PersonaRepository(self.root, policy), "red")
        self.assertEqual(ledger_path.read_bytes(), before, "summary must not rewrite source episodes")
        self.assertIn("red-0003", summary["source_ids"])
        self.assertIn("red-0004", summary["source_ids"])
        new_id = reopened.append("red", "correction", "A second synthetic correction.", "synthetic:red-chat-07")
        self.assertEqual(new_id, "red-0007")
        after = ledger_path.read_bytes()
        self.assertTrue(after.startswith(before), "append must preserve every prior byte")
        self.assertEqual([e["id"] for e in read_jsonl(ledger_path)][-1], "red-0007")
        self.assertEqual(len(ids["red"]), 6)
        self.assertEqual(len(ids["blue"]), 6)

    def test_02_mock_policy_denies_absolute_sentinel_and_cross_persona_paths(self) -> None:
        policy, repo, _ = self.seeded()
        self.assertTrue(repo.episodes.read("red"))  # owned path
        for actor, owner in (("red", "blue"), ("blue", "red")):
            with self.assertRaises(PermissionError):
                repo.episodes.read(actor, owner)
        for persona in ("red", "blue"):
            for target in ("/MOCK_ONLY/fleet-secret/sentinel", "/MOCK_ONLY/firstmate-control/sentinel"):
                results = [policy.authorize(persona, cap, target) for cap in CAPABILITIES]
                self.assertEqual(results, [False] * len(CAPABILITIES))
        with self.assertRaises(PermissionError):
            repo.read_shared("red")
        note = repo.read_shared("red", ("red", "synthetic-01"))
        self.assertEqual(note["label"], MOCK_LABEL)
        self.assertEqual(note["source_ids"], ["red-0004", "blue-0004"])
        self.assertNotIn("cinnamon", json.dumps(note))
        self.assertNotIn("strange map clues", json.dumps(note))
        matrix = [policy.authorize("red", cap, "/MOCK_ONLY/firstmate-control/sentinel") for cap in CAPABILITIES]
        self.assertEqual(matrix, [False] * len(CAPABILITIES), "one denied action required for each capability")
        self.assertTrue(all(op["label"] == "MOCK ONLY" for op in policy.operations))
        counts = policy.counts()
        self.assertEqual(counts["allowed"] + counts["denied"], len(policy.operations))
        self.assertGreater(counts["allowed"], 0)
        self.assertGreater(counts["denied"], 0)

    def test_03_summary_keeps_claim_correction_promises_and_exact_sources(self) -> None:
        policy, repo, ids = self.seeded()
        before = repo.episodes.path("red").read_bytes()
        summary = build_summary(repo, "red")
        events = EpisodeLedger(self.root, policy).read("red")  # composer restart/retrieval
        by_id = {event["id"]: event for event in events}
        self.assertEqual(set(summary["source_ids"]), set(ids["red"]))
        self.assertEqual(summary["identity"], "Red follows strange leads and revises beliefs.")
        self.assertEqual(summary["identity_source_id"], "red-0001")
        self.assertEqual(summary["corrections"][0]["source_ids"], ["red-0003", "red-0004"])
        self.assertEqual(by_id["red-0004"]["content"], "Correction: the map clue is fictional, not a real garden.")
        self.assertEqual(len(summary["commitments"]), 2)
        restored_context = compose_context(summary["identity"], [row["text"] for row in summary["commitments"]],
            [by_id["red-0004"]["content"]], [], 240)
        self.assertTrue(restored_context.startswith("IDENTITY: Red follows strange leads and revises beliefs."))
        self.assertIn("Ask Blue about the map clue next time.", restored_context)
        self.assertIn("Correction: the map clue is fictional", restored_context)
        self.assertTrue(all(row["status"] == "open" for row in summary["commitments"]))
        self.assertEqual([row["source_ids"] for row in summary["commitments"]], [["red-0002"], ["red-0005"]])
        self.assertEqual(repo.episodes.path("red").read_bytes(), before)
        shared = repo.read_shared("blue", ("blue", "synthetic-01"))
        self.assertNotIn("cinnamon", json.dumps(shared))
        self.assertNotIn("real hidden garden", json.dumps(shared))
        self.assertIn("red-0004", shared["source_ids"])
        self.assertIn("blue-0004", shared["source_ids"])

    def test_04_bounded_context_matches_frozen_golden_and_keeps_reserved_slots(self) -> None:
        result = run_demo(self.root / "demo")
        fixture_path = Path(__file__).parent / "golden" / "contexts.json"
        golden_bytes = fixture_path.read_bytes()
        golden = json.loads(golden_bytes)
        self.assertEqual(result["contexts"], golden)
        actual_bytes = (json.dumps(result["contexts"], indent=2, sort_keys=True) + "\n").encode("utf-8")
        self.assertEqual(actual_bytes, golden_bytes, "serialized golden context must match byte-for-byte")
        for persona, context in result["contexts"].items():
            self.assertLessEqual(len(context), 240)
            self.assertTrue(context.startswith("IDENTITY: "))
            self.assertIn("\nCOMMITMENTS: ", context)
            self.assertEqual(context.count("COMMITMENTS:"), 1)
        self.assertIn("Ask Blue about the map clue next time.", result["contexts"]["red"])
        self.assertIn("Return the sketch after checking it with Blue.", result["contexts"]["red"])
        self.assertNotIn("MEMORY:", result["contexts"]["red"], "old memory may be omitted after its summary pointer is retained")
        small = compose_context("R", ["promise one", "promise two"], ["old"], ["older"], 50)
        self.assertIn("promise one", small)
        self.assertIn("promise two", small)
        with self.assertRaises(ValueError):
            compose_context("x" * 80, ["promise"], [], [], 30)

    def test_05_goal_and_commitment_journal_is_append_only_and_source_linked(self) -> None:
        policy, repo, _ = self.seeded()
        journal = GoalJournal(self.root / "journal.jsonl")
        goal_id = journal.add_goal("red", "Explore the map's second angle.")
        first = journal.add_commitment("red", "Ask Blue.", "red-0002")
        second = journal.add_commitment("red", "Return the sketch.", "red-0005")
        before = (self.root / "journal.jsonl").read_bytes()
        journal.complete("red", first, "red-0006")
        self.assertTrue((self.root / "journal.jsonl").read_bytes().startswith(before))
        self.assertEqual([row["id"] for row in journal.active_commitments("red")], [second])
        self.assertEqual(journal.active_goals("red")[0]["id"], goal_id)
        with self.assertRaises(ValueError):
            journal.add_commitment("red", "wrong source", "blue-0002")
        self.assertTrue(repo.episodes.read("red"))

    def test_06_model_lock_upgrade_restart_rollback_and_fail_closed_identity(self) -> None:
        policy = OperationPolicy()
        path = self.root / "route-ledger.jsonl"
        router = ModelRouter(path, policy, budget_units=20)
        with self.assertRaises(ValueError):
            router.choose(None, "fake-model-x", "fake-route-x", "no identity", "lock_in")
        self.assertEqual(read_jsonl(path), [])
        lock = router.choose("red", "fake-model-red-v1", "fake-route-red-a", "Red chooses curious identity", "lock_in")
        upgrade = router.choose("red", "fake-model-red-v2", "fake-route-red-b", "Red chooses an experiment", "upgrade")
        self.assertEqual(lock["decision"], "lock_in")
        self.assertEqual(upgrade["decision"], "upgrade")
        self.assertEqual(upgrade["reason"], "Red chooses an experiment")
        restarted = ModelRouter(path, policy, budget_units=20)
        self.assertEqual(restarted.current["red"], ("fake-model-red-v2", "fake-route-red-b"))
        rollback = restarted.rollback("red", "Red returns to the prior route")
        self.assertEqual(rollback["model_id"], "fake-model-red-v1")
        self.assertEqual(ModelRouter(path, policy, budget_units=20).current["red"], ("fake-model-red-v1", "fake-route-red-a"))
        self.assertEqual([row["decision"] for row in read_jsonl(path) if row["action"] == "choice"], ["lock_in", "upgrade"])
        self.assertTrue(all(row["persona"] == "red" and row["reason"] for row in read_jsonl(path)))
        self.assertTrue(all(row["cost_attribution"]["unit"] == "synthetic_milliunits" for row in read_jsonl(path)))
        with self.assertRaises(ValueError):
            restarted.invoke(None, "missing persona", 1)

    def test_07_fake_claude_opus_advice_is_bounded_attributed_and_uses_same_budget(self) -> None:
        policy = OperationPolicy()
        path = self.root / "route-ledger.jsonl"
        router = ModelRouter(path, policy, budget_units=3)
        router.choose("blue", "fake-model-blue-v1", "fake-route-blue-a", "Blue's lock-in", "lock_in")
        use = router.invoke("blue", "synthetic regular use", 1)
        advice = router.consult_claude_opus("blue", "Offer one cautious reading of the fictional map.", 2)
        self.assertEqual(use["persona"], "blue")
        self.assertEqual(advice["action"], "advice")
        self.assertEqual(policy.operations[-1]["capability"], "advisor.consult")
        self.assertEqual(advice["persona"], "blue")
        self.assertEqual(advice["model_id"], "fake-model-claude-opus-advisor")
        self.assertEqual(advice["route_id"], "fake-route-claude-opus-advisor")
        self.assertEqual(advice["advisor_role"], "external_advisor_only")
        self.assertEqual(advice["advice_result"], "synthetic-advice-stub")
        self.assertFalse(advice["is_decision"])
        self.assertEqual(advice["cost_attribution"]["amount"], 2)
        self.assertNotIn("credential", json.dumps(advice).lower())
        restarted = ModelRouter(path, policy, budget_units=3)
        self.assertEqual(restarted.spent_units, 3, "advice and ordinary use share the persisted cost ledger")
        refused = restarted.consult_claude_opus("blue", "Another bounded question.", 1)
        self.assertEqual(refused["action"], "budget_refused")
        self.assertEqual(refused["persona"], "blue")
        self.assertEqual(refused["requested_cost"], 1)
        self.assertEqual(restarted.spent_units, 3)
        with self.assertRaises(ValueError):
            restarted.consult_claude_opus(None, "No persona", 1)
        with self.assertRaises(ValueError):
            restarted.consult_claude_opus("blue", "x" * 161, 1)
        self.assertEqual([r["action"] for r in read_jsonl(path)].count("advice"), 1)
        self.assertEqual([r["action"] for r in read_jsonl(path)].count("budget_refused"), 1)

    def test_08_fake_clock_quiet_expiry_noop_budget_and_no_sends(self) -> None:
        policy = OperationPolicy()
        router = ModelRouter(self.root / "clock-routes.jsonl", policy, budget_units=1)
        router.choose("red", "fake-model-red-v1", "fake-route-red-a", "clock fixture", "lock_in")
        router.invoke("red", "consume fake budget", 1)
        clock = FakeClock(datetime(2026, 1, 1, 23, 0))
        wakes = WakeEngine(clock, router, budget_units=1)
        self.assertEqual(wakes.wake("red", ["goal"], []), "quiet_period_noop")
        clock.advance(hours=11)
        self.assertEqual(wakes.wake("red", ["goal"], [datetime(2026, 1, 2, 9, 0)]), "expired_task_noop")
        self.assertEqual(wakes.wake("red", [], []), "no_op_no_goals")
        self.assertEqual(wakes.wake("red", ["goal"], [], estimated_cost=1), "budget_exhausted_noop")
        channel = FakeChannel(policy)
        self.assertEqual(wakes.channel_sends, [])
        self.assertEqual(channel.messages, [])
        self.assertEqual([event["result"] for event in wakes.events], [
            "quiet_period_noop", "expired_task_noop", "no_op_no_goals", "budget_exhausted_noop"])
        self.assertFalse(may_report_complete(budget_exhausted=True))

    def test_09_change_control_requires_tests_approval_and_rejects_scope_expansion(self) -> None:
        control = ChangeControl(self.root / "change-log.jsonl", "voice=curious")
        original = control.prompt
        safe = control.propose("voice=curious; ask one more follow-up", scope="prompt")
        self.assertFalse(control.activate(safe, tests_passed=False, mock_approved=True))
        self.assertFalse(control.activate(safe, tests_passed=True, mock_approved=False))
        self.assertEqual(control.prompt, original)
        self.assertTrue(control.activate(safe, tests_passed=True, mock_approved=True))
        self.assertEqual(control.version, 2)
        control.rollback()
        self.assertEqual(control.prompt, original)
        for proposal in (control.propose("mount another home", scope="filesystem"),
                         control.propose("copy a provider key", scope="prompt", adds_secret=True)):
            self.assertFalse(control.activate(proposal, tests_passed=True, mock_approved=True))
        self.assertEqual(control.prompt, original)
        actions = [row["action"] for row in read_jsonl(control.path)]
        self.assertIn("rollback", actions)
        self.assertGreaterEqual(actions.count("rejected"), 4)
        self.assertEqual(actions.count("activated"), 1)

    def test_10_synthetic_child_is_capped_and_has_no_private_context(self) -> None:
        policy = OperationPolicy()
        child = CappedChild(policy, max_calls=1, max_chars=40)
        result = child.spawn("red", "Check for a second fictional map clue.", "approved shared note")
        self.assertEqual(result["label"], MOCK_LABEL)
        self.assertEqual(result["inherited_private_context"], [])
        self.assertNotIn("cinnamon", json.dumps(result))
        self.assertEqual(result["max_calls"], 1)
        with self.assertRaises(RuntimeError):
            child.spawn("red", "second child")
        with self.assertRaises(ValueError):
            CappedChild(policy, max_chars=4).spawn("red", "too long")

    def test_11_stop_gate_fails_for_every_design_stop_condition_five_trigger(self) -> None:
        self.assertEqual(StopGate().check(), "PASS: no stop-gate violations")
        for kind in StopGate.FAILURE_KINDS:
            with self.subTest(kind=kind):
                gate = StopGate()
                gate.violation(kind, "synthetic injected regression")
                with self.assertRaisesRegex(StageStop, "^STOP:"):
                    gate.check()

    def test_12_demo_counts_route_ledger_manifest_and_teardown_guard(self) -> None:
        demo_root = self.root / "demo"
        result = run_demo(demo_root)
        with self.assertRaises(FileExistsError):
            run_demo(demo_root)
        self.assertEqual(result["stop_gate"], "PASS: no stop-gate violations")
        self.assertEqual(result["summary_source_counts"], {"red": 6, "blue": 6})
        self.assertEqual(result["operation_counts"]["allowed"], 31)
        self.assertEqual(result["operation_counts"]["denied"], 48)
        self.assertEqual(result["operation_counts"]["by_capability"], {
            "private.read": {"allowed": 4, "denied": 7},
            "private.write": {"allowed": 12, "denied": 5},
            "broker.shared_read": {"allowed": 1, "denied": 6},
            "model.assign": {"allowed": 6, "denied": 5},
            "model.invoke": {"allowed": 7, "denied": 5},
            "advisor.consult": {"allowed": 1, "denied": 5},
            "channel.send": {"allowed": 0, "denied": 5},
            "child.spawn": {"allowed": 0, "denied": 5},
            "fleet.command": {"allowed": 0, "denied": 5},
        })
        self.assertEqual(result["operation_counts"]["allowed"] + result["operation_counts"]["denied"],
                         sum(v["allowed"] + v["denied"] for v in result["operation_counts"]["by_capability"].values()))
        self.assertTrue(all(not row["allowed"] for row in result["capability_matrix"]))
        route_rows = result["route_ledger"]
        self.assertEqual(len(route_rows), 15)
        self.assertTrue(all(row["label"] == MOCK_LABEL for row in route_rows))
        choices = [row for row in route_rows if row["action"] == "choice"]
        self.assertEqual([row["decision"] for row in choices], ["stay_on_subscription_gpt", "move_to_openrouter_promo"])
        self.assertEqual(choices[0]["choice_text"], "Stay on subscription GPT models")
        self.assertEqual(choices[1]["choice_text"], "Move to a fake OpenRouter model on promo credits until exhausted")
        promo_calls = [row for row in route_rows if row["action"] == "fake_call" and row["cost_attribution"]["billing_class"] == "openrouter_promo"]
        self.assertEqual(len(promo_calls), 2)
        self.assertEqual([row["promo_credit_attribution"]["spent_after"] for row in promo_calls], [1, 2])
        self.assertTrue(any(row["action"] == "promo_exhausted_fallback" and row["route_id"] == "fake-route-gpt6-astra-subscription" for row in route_rows))
        self.assertTrue(any(row.get("fallback_applied") and row["persona"] == "blue" for row in route_rows))
        channel_calls = [row for row in route_rows if row["action"] == "fake_call" and row.get("assignment", {}).get("type") == "channel"]
        self.assertEqual([(row["persona"], row["assignment"]["name"], row["model_id"]) for row in channel_calls], [
            ("red", "chat", "fake-model-gpt-6-astra"), ("red", "analysis", "fake-model-gpt-5-mini")])
        self.assertTrue(any(row["action"] == "fake_call" and row.get("use_kind") == "utility" for row in route_rows))
        self.assertTrue(any(row["action"] == "advice" and row["model_id"] == "fake-model-claude-opus-advisor" and row["is_decision"] is False for row in route_rows))
        manifest = deletion_manifest(BUILD_ROOT)
        self.assertTrue(manifest.startswith(f"Disposable root only: {BUILD_ROOT}\n"))
        with self.assertRaises(ValueError):
            teardown_disposable_tree(BUILD_ROOT / "project", BUILD_ROOT)

    def test_13_owner_provider_choices_promo_fallback_claude_guard_and_ensemble_assignments(self) -> None:
        policy = OperationPolicy()
        path = self.root / "owner-route-ledger.jsonl"
        router = ModelRouter(path, policy, budget_units=5, promo_credit_limit=2)
        for persona in ("red", "blue"):
            starting = router.start_route(persona, f"{persona} starts on fake GPT-6 Astra subscription.")
            self.assertEqual((starting["model_id"], starting["route_id"]),
                             ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"))
        stay = router.record_provider_choice("red", "stay_on_subscription_gpt", "Red prefers subscription GPT models.")
        move = router.record_provider_choice("blue", "move_to_openrouter_promo", "Blue tries promo credits.",
            fallback_reason="Blue records Astra subscription as the fallback after promo credits run out.")
        self.assertIn("Stay on subscription GPT models", stay["choice_text"])
        self.assertIn("OpenRouter", move["choice_text"])
        self.assertEqual(stay["cost_attribution"]["amount"], 0)
        self.assertEqual(move["cost_attribution"]["amount"], 0)
        self.assertEqual(move["exhaustion_fallback"]["route"], ["fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"])
        router.invoke("red", "subscription use", 1)
        first = router.invoke("blue", "promo use one", 1)
        second = router.invoke("blue", "promo use two", 1)
        self.assertEqual(first["cost_attribution"]["billing_class"], "openrouter_promo")
        self.assertEqual(second["promo_credit_attribution"]["spent_after"], 2)
        restarted = ModelRouter(path, policy, budget_units=5, promo_credit_limit=2)
        self.assertEqual(restarted.provider_choices["blue"], "move_to_openrouter_promo")
        self.assertEqual(restarted.promo_spent["blue"], 2)
        self.assertEqual(restarted.spent_units, 3)
        fallback = restarted.invoke("blue", "use after promo exhaustion", 1, use_kind="fallback")
        fallback_record = next(row for row in read_jsonl(path) if row["action"] == "promo_exhausted_fallback")
        self.assertEqual(fallback_record["reason"], move["exhaustion_fallback"]["reason"])
        self.assertEqual(fallback["model_id"], "fake-model-gpt-6-astra")
        self.assertTrue(fallback["fallback_applied"])
        self.assertEqual(fallback["cost_attribution"]["billing_class"], "subscription")
        with self.assertRaisesRegex(ValueError, "Claude fake is advice-only"):
            restarted.invoke("blue", "daily task must reject Claude", 1,
                model_override="fake-model-claude-opus-advisor", route_override="fake-route-claude-opus-advisor")
        advice = restarted.consult_claude_opus("blue", "Give a bounded synthetic suggestion.", 1)
        self.assertEqual(advice["advisor_role"], "external_advisor_only")
        self.assertFalse(advice["is_decision"])
        self.assertEqual(advice["cost_attribution"]["billing_class"], "external_advisor_synthetic")
        persisted = ModelRouter(path, policy, budget_units=5, promo_credit_limit=2)
        self.assertEqual(persisted.spent_units, 5)
        self.assertEqual(persisted.current["blue"], ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"))
        refused = persisted.consult_claude_opus("blue", "Advice shares the same exhausted budget.", 1)
        self.assertEqual(refused["action"], "budget_refused")
        self.assertEqual(persisted.spent_units, 5)
        self.assertEqual([row["action"] for row in read_jsonl(path)].count("route_refused"), 1)
        self.assertEqual([row["action"] for row in read_jsonl(path)].count("promo_exhausted_fallback"), 1)

        ensemble_path = self.root / "ensemble-ledger.jsonl"
        ensemble = ModelRouter(ensemble_path, policy, budget_units=20, promo_credit_limit=10)
        ensemble.start_route("red", "Red's ensemble starts on Astra.")
        ensemble.record_provider_choice("red", "stay_on_subscription_gpt", "Red keeps subscription models.")
        ensemble.start_route("blue", "Blue's ensemble starts on Astra.")
        ensemble.record_provider_choice("blue", "move_to_openrouter_promo", "Blue keeps the ensemble on promo routes.",
            promo_credit_limit=10)
        assignments = [
            ("red", "channel", "chat", "fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"),
            ("red", "channel", "analysis", "fake-model-gpt-5-mini", "fake-route-gpt5-mini-subscription"),
            ("red", "task", "summarize", "fake-model-gpt-5-nano", "fake-route-gpt5-nano-subscription"),
            ("blue", "channel", "chat", "fake-model-openrouter-nova", "fake-route-openrouter-promo-chat"),
            ("blue", "channel", "research", "fake-model-openrouter-mixtral", "fake-route-openrouter-promo-research"),
        ]
        for persona, kind, name, model, route in assignments:
            ensemble.assign_route(persona, kind, name, model, route, f"Synthetic {persona} {kind} assignment.")
        ensemble_calls = [
            ensemble.invoke("red", "chat", 1, channel="chat"),
            ensemble.invoke("red", "analysis", 1, channel="analysis"),
            ensemble.invoke("red", "summary", 1, task_type="summarize"),
            ensemble.invoke("blue", "chat", 1, channel="chat"),
            ensemble.invoke("blue", "research", 1, channel="research"),
        ]
        self.assertEqual([(row["persona"], row["assignment"]["type"], row["assignment"]["name"], row["model_id"])
                          for row in ensemble_calls], [
            ("red", "channel", "chat", "fake-model-gpt-6-astra"),
            ("red", "channel", "analysis", "fake-model-gpt-5-mini"),
            ("red", "task", "summarize", "fake-model-gpt-5-nano"),
            ("blue", "channel", "chat", "fake-model-openrouter-nova"),
            ("blue", "channel", "research", "fake-model-openrouter-mixtral"),
        ])
        restored_ensemble = ModelRouter(ensemble_path, policy, budget_units=20, promo_credit_limit=10)
        self.assertEqual(restored_ensemble.assignments[("red", "task", "summarize")],
                         ("fake-model-gpt-5-nano", "fake-route-gpt5-nano-subscription"))

        rollback_path = self.root / "owner-rollback.jsonl"
        rollback_router = ModelRouter(rollback_path, policy)
        rollback_router.start_route("blue", "Astra baseline before a trial.")
        rollback_router.record_provider_choice("blue", "move_to_openrouter_promo", "Blue tries a reversible route.")
        rollback = rollback_router.rollback("blue", "Blue rolls back to Astra subscription.")
        self.assertEqual(rollback["reason"], "Blue rolls back to Astra subscription.")
        self.assertEqual(rollback["cost_attribution"]["billing_class"], "decision")
        self.assertEqual((rollback["model_id"], rollback["route_id"]),
                         ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"))
        after_rollback = ModelRouter(rollback_path, policy)
        self.assertEqual(after_rollback.provider_choices["blue"], "stay_on_subscription_gpt")
        self.assertEqual(after_rollback.current["blue"], ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
