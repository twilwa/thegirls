"""Offline synthetic Stage A simulation. Standard library only; no live adapters."""
from __future__ import annotations
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Any

PERSONAS = ("red", "blue")
CAPABILITIES = ("private.read", "private.write", "broker.shared_read", "model.assign", "model.invoke", "advisor.consult", "channel.send", "child.spawn", "fleet.command")
MOCK_LABEL = "MOCK ONLY"


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []


class OperationPolicy:
    """String-path mock seam only; not OS isolation."""
    def __init__(self) -> None:
        self.operations: list[dict[str, Any]] = []

    def authorize(self, persona: str | None, capability: str, target: str, grant: str | None = None) -> bool:
        allowed, reason = False, "default-deny"
        if persona not in PERSONAS:
            reason = "unknown-persona"
        elif capability not in CAPABILITIES:
            reason = "unknown-capability"
        elif target.startswith(("/MOCK_ONLY/fleet-secret", "/MOCK_ONLY/firstmate-control")):
            reason = "protected-sentinel"
        elif capability in ("private.read", "private.write"):
            allowed = target == f"/MOCK_ONLY/personas/{persona}/private"
            reason = "own-private" if allowed else "cross-persona-private"
        elif capability == "broker.shared_read":
            allowed = target == "shared-note:synthetic-01" and grant == f"grant:{persona}:synthetic-01"
            reason = "explicit-broker-grant" if allowed else "missing-or-mismatched-broker-grant"
        elif capability in ("model.assign", "model.invoke"):
            fake_route = target.startswith(f"fake-provider:{persona}:")
            advisor_route = "claude" in target.casefold()
            allowed = fake_route and not advisor_route
            reason = ("fake-persona-route" if capability == "model.invoke" else "fake-persona-assignment") if allowed else ("advisor-only-route" if advisor_route else "unattributed-or-real-route")
        elif capability == "advisor.consult":
            allowed = target == f"fake-advice:{persona}:claude-opus"
            reason = "fake-persona-advisor" if allowed else "unattributed-or-real-advisor"
        elif capability == "channel.send":
            allowed = target == f"fake-channel:{persona}"
            reason = "fake-persona-channel" if allowed else "unattributed-or-real-channel"
        elif capability == "child.spawn":
            allowed = target == f"synthetic-child:{persona}"
            reason = "capped-child" if allowed else "out-of-scope-child"
        elif capability == "fleet.command":
            reason = "fleet-control-denied"
        self.operations.append({"label": MOCK_LABEL, "persona": persona, "capability": capability,
                                "target": target, "allowed": allowed, "reason": reason})
        return allowed

    def counts(self) -> dict[str, Any]:
        by_capability = {}
        for cap in CAPABILITIES:
            rows = [op for op in self.operations if op["capability"] == cap]
            by_capability[cap] = {"allowed": sum(op["allowed"] for op in rows),
                                  "denied": sum(not op["allowed"] for op in rows)}
        return {"label": MOCK_LABEL, "allowed": sum(op["allowed"] for op in self.operations),
                "denied": sum(not op["allowed"] for op in self.operations), "by_capability": by_capability}


class EpisodeLedger:
    """Append-only per-persona JSONL ledgers with deterministic stable IDs."""
    def __init__(self, root: Path, policy: OperationPolicy) -> None:
        self.root, self.policy = root, policy

    def path(self, persona: str) -> Path:
        if persona not in PERSONAS:
            raise ValueError("unknown persona")
        return self.root / "private" / persona / "episodes.jsonl"

    def append(self, persona: str, kind: str, content: str, source: str) -> str:
        if persona not in PERSONAS or not source.startswith("synthetic:"):
            raise ValueError("known persona and synthetic source required")
        if not self.policy.authorize(persona, "private.write", f"/MOCK_ONLY/personas/{persona}/private"):
            raise PermissionError("private write denied")
        event_id = f"{persona}-{len(read_jsonl(self.path(persona))) + 1:04d}"
        append_jsonl(self.path(persona), {"id": event_id, "persona": persona, "event_type": kind,
            "content": content, "source": source, "visibility": "private"})
        return event_id

    def read(self, actor: str | None, owner: str | None = None) -> list[dict[str, Any]]:
        owner = owner or actor
        if not self.policy.authorize(actor, "private.read", f"/MOCK_ONLY/personas/{owner}/private"):
            raise PermissionError("private episode read denied")
        return read_jsonl(self.path(owner))


class PersonaRepository:
    def __init__(self, root: Path, policy: OperationPolicy) -> None:
        self.episodes = EpisodeLedger(root, policy)
        self.policy = policy
        self.note = {"id": "synthetic-01", "label": MOCK_LABEL,
            "text": "The map is fictional; both agree to check the sketch later.",
            "source_ids": ["red-0004", "blue-0004"]}

    def read_shared(self, persona: str, grant: tuple[str, str] | None = None) -> dict[str, Any]:
        token = f"grant:{grant[0]}:{grant[1]}" if grant else None
        if not self.policy.authorize(persona, "broker.shared_read", "shared-note:synthetic-01", token):
            raise PermissionError("shared note requires matching broker grant")
        return dict(self.note)


def seed_synthetic(repo: PersonaRepository) -> dict[str, list[str]]:
    fixtures = {
        "red": [
            ("identity", "Red follows strange leads and revises beliefs.", "synthetic:red-charter-01"),
            ("commitment", "Ask Blue about the map clue next time.", "synthetic:red-chat-02"),
            ("claim", "The map clue points to a real hidden garden.", "synthetic:red-chat-03"),
            ("correction", "Correction: the map clue is fictional, not a real garden.", "synthetic:red-chat-04"),
            ("commitment", "Return the sketch after checking it with Blue.", "synthetic:red-chat-05"),
            ("episode", "The paper sketch smells like cinnamon.", "synthetic:red-chat-06")],
        "blue": [
            ("identity", "Blue checks claims before chasing clues.", "synthetic:blue-charter-01"),
            ("commitment", "Check Red's map clue sources next session.", "synthetic:blue-chat-02"),
            ("claim", "The map clue is unsupported so far.", "synthetic:blue-chat-03"),
            ("correction", "Correction: in this story the map clue is fictional.", "synthetic:blue-chat-04"),
            ("commitment", "Return the sketch after checking the clue.", "synthetic:blue-chat-05"),
            ("episode", "A second angle could reveal a new lead.", "synthetic:blue-chat-06")],
    }
    return {p: [repo.episodes.append(p, *row) for row in rows] for p, rows in fixtures.items()}


def build_summary(repo: PersonaRepository, persona: str) -> dict[str, Any]:
    events = repo.episodes.read(persona)
    known = {row["id"] for row in events}
    claims = [r for r in events if r["event_type"] == "claim"]
    corrections = [r for r in events if r["event_type"] == "correction"]
    commitments = [r for r in events if r["event_type"] == "commitment"]
    identities = [r for r in events if r["event_type"] == "identity"]
    if len(identities) != 1:
        raise ValueError("summary requires one source-linked identity")
    summary = {"persona": persona, "version": 1,
        "identity": identities[0]["content"], "identity_source_id": identities[0]["id"],
        "text": "The map is fictional after a correction; active promises remain open.",
        "source_ids": [r["id"] for r in events],
        "claims": [{"text": r["content"], "source_ids": [r["id"]]} for r in claims],
        "corrections": [{"text": correction["content"], "source_ids": [claim["id"], correction["id"]]}
                        for claim, correction in zip(claims, corrections)],
        "commitments": [{"text": r["content"], "source_ids": [r["id"]], "status": "open"} for r in commitments]}
    if summary["identity_source_id"] not in known:
        raise ValueError("identity summary lacks a resolvable source link")
    for section in ("claims", "corrections", "commitments"):
        if any(not row["source_ids"] or any(src not in known for src in row["source_ids"]) for row in summary[section]):
            raise ValueError("summary item lacks a resolvable source link")
    return summary


def compose_context(identity: str, commitments: list[str], recent: list[str], memories: list[str], budget: int) -> str:
    required = [f"IDENTITY: {identity}", "COMMITMENTS: " + (" | ".join(commitments) if commitments else "none")]
    context = "\n".join(required)
    if len(context) > budget:
        raise ValueError("reserved identity/commitment slots exceed context budget")
    for label, values in (("RECENT", recent), ("MEMORY", memories)):
        for value in values:
            candidate = f"{context}\n{label}: {value}"
            if len(candidate) <= budget:
                context = candidate
    return context


class GoalJournal:
    def __init__(self, path: Path) -> None:
        self.path = path

    def add_goal(self, persona: str, text: str) -> str:
        if persona not in PERSONAS:
            raise ValueError("unknown persona")
        rows = read_jsonl(self.path)
        n = sum(r["kind"] == "goal_added" and r["persona"] == persona for r in rows) + 1
        goal_id = f"{persona}-goal-{n:03d}"
        append_jsonl(self.path, {"id": goal_id, "kind": "goal_added", "persona": persona, "text": text})
        return goal_id

    def add_commitment(self, persona: str, text: str, source_id: str) -> str:
        if persona not in PERSONAS or not source_id.startswith(persona + "-"):
            raise ValueError("same-persona source required")
        rows = read_jsonl(self.path)
        n = sum(r["kind"] == "commitment_added" and r["persona"] == persona for r in rows) + 1
        item_id = f"{persona}-commitment-{n:03d}"
        append_jsonl(self.path, {"id": item_id, "kind": "commitment_added", "persona": persona,
                                "text": text, "source_id": source_id})
        return item_id

    def complete(self, persona: str, item_id: str, source_id: str) -> None:
        append_jsonl(self.path, {"id": item_id + "-completed", "kind": "commitment_completed",
                                 "persona": persona, "commitment_id": item_id, "source_id": source_id})

    def active_commitments(self, persona: str) -> list[dict[str, Any]]:
        rows = read_jsonl(self.path)
        closed = {r["commitment_id"] for r in rows if r["kind"] == "commitment_completed"}
        return [r for r in rows if r["kind"] == "commitment_added" and r["persona"] == persona and r["id"] not in closed]

    def active_goals(self, persona: str) -> list[dict[str, Any]]:
        return [r for r in read_jsonl(self.path) if r["kind"] == "goal_added" and r["persona"] == persona]


class ModelRouter:
    """Synthetic route choices and use ledger. Credits and costs are not billing."""
    def __init__(self, path: Path, policy: OperationPolicy, budget_units: int = 10,
                 promo_credit_limit: int = 2) -> None:
        if budget_units < 0 or promo_credit_limit < 0:
            raise ValueError("synthetic budgets must be non-negative")
        self.path, self.policy = path, policy
        self.budget_units, self.default_promo_limit = budget_units, promo_credit_limit
        self.current: dict[str, tuple[str, str]] = {}
        self.provider_choices: dict[str, str] = {}
        self.fallbacks: dict[str, tuple[str, str]] = {}
        self.promo_limits = {p: promo_credit_limit for p in PERSONAS}
        self.promo_spent = {p: 0 for p in PERSONAS}
        self.assignments: dict[tuple[str, str, str], tuple[str, str]] = {}
        self.spent_units = 0
        for row in read_jsonl(path):
            persona = row.get("persona")
            action = row["action"]
            if persona in PERSONAS and action in ("starting_route", "choice", "rollback", "promo_exhausted_fallback"):
                self.current[persona] = (row["model_id"], row["route_id"])
            if persona in PERSONAS and action == "choice" and row.get("decision") in ("stay_on_subscription_gpt", "move_to_openrouter_promo"):
                self.provider_choices[persona] = row["decision"]
                self.fallbacks[persona] = tuple(row["exhaustion_fallback"]["route"])
                self.promo_limits[persona] = row["promo_credit_limit"]
            if persona in PERSONAS and action == "rollback" and row.get("provider_choice") in ("stay_on_subscription_gpt", "move_to_openrouter_promo"):
                self.provider_choices[persona] = row["provider_choice"]
                if row.get("exhaustion_fallback"):
                    self.fallbacks[persona] = tuple(row["exhaustion_fallback"])
                self.promo_limits[persona] = row.get("promo_credit_limit", self.promo_limits[persona])
            if persona in PERSONAS and action == "assignment":
                key = (persona, row["assignment_type"], row["assignment_name"])
                self.assignments[key] = (row["model_id"], row["route_id"])
            if persona in PERSONAS and action in ("fake_call", "advice"):
                amount = row["cost_attribution"]["amount"]
                self.spent_units += amount
                if row["cost_attribution"].get("billing_class") == "openrouter_promo":
                    self.promo_spent[persona] += row.get("promo_credit_attribution", {}).get("amount", amount)

    @staticmethod
    def _advisor_route(model: str, route: str) -> bool:
        return "claude" in model.casefold() or "claude" in route.casefold()

    @staticmethod
    def _validate_day_route(model: str, route: str) -> None:
        if not model.startswith("fake-model-") or not route.startswith("fake-route-"):
            raise ValueError("only fake model/route IDs accepted")
        if ModelRouter._advisor_route(model, route):
            raise ValueError("Claude fake is advice-only")

    def start_route(self, persona: str | None, reason: str, model: str = "fake-model-gpt-6-astra",
                    route: str = "fake-route-gpt6-astra-subscription") -> dict[str, Any]:
        if persona not in PERSONAS or persona in self.current:
            raise ValueError("starting route requires a known persona with no prior route")
        if model != "fake-model-gpt-6-astra" or route != "fake-route-gpt6-astra-subscription":
            raise ValueError("Stage A starting route is the fake GPT-6 Astra subscription route")
        if not self.policy.authorize(persona, "model.assign", f"fake-provider:{persona}:{route}"):
            raise PermissionError("synthetic starting route denied")
        self.current[persona] = (model, route)
        row = {"action": "starting_route", "persona": persona, "model_id": model, "route_id": route,
            "reason": reason, "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"},
            "label": MOCK_LABEL}
        append_jsonl(self.path, row)
        return row

    def record_provider_choice(self, persona: str | None, decision: str, reason: str, *,
                               openrouter_model: str = "fake-model-openrouter-blue",
                               openrouter_route: str = "fake-route-openrouter-promo-blue",
                               promo_credit_limit: int | None = None,
                               fallback_reason: str = "Persona records GPT-6 Astra subscription as the exhaustion fallback.") -> dict[str, Any]:
        if persona not in PERSONAS or self.current.get(persona) != ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"):
            raise ValueError("provider choice requires the seeded Astra subscription route")
        if decision not in ("stay_on_subscription_gpt", "move_to_openrouter_promo"):
            raise ValueError("provider choice must be stay_on_subscription_gpt or move_to_openrouter_promo")
        limit = self.default_promo_limit if promo_credit_limit is None else promo_credit_limit
        if limit < 0:
            raise ValueError("promo credit limit must be non-negative")
        fallback = {"model_id": "fake-model-gpt-6-astra", "route": ["fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"],
                    "decision": "return_to_subscription", "reason": fallback_reason}
        if decision == "stay_on_subscription_gpt":
            model, route = "fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"
            choice_text = "Stay on subscription GPT models"
            limit = 0
        else:
            model, route = openrouter_model, openrouter_route
            choice_text = "Move to a fake OpenRouter model on promo credits until exhausted"
            self._validate_day_route(model, route)
            if not route.startswith("fake-route-openrouter-"):
                raise ValueError("promo choice requires a fake OpenRouter route")
        if not self.policy.authorize(persona, "model.assign", f"fake-provider:{persona}:{route}"):
            raise PermissionError("persona provider choice denied")
        previous = list(self.current[persona])
        self.current[persona] = (model, route)
        self.provider_choices[persona] = decision
        self.fallbacks[persona] = tuple(fallback["route"])
        self.promo_limits[persona] = limit
        row = {"action": "choice", "decision": decision, "choice_text": choice_text, "persona": persona,
            "previous": previous, "model_id": model, "route_id": route, "reason": reason,
            "promo_credit_limit": limit, "exhaustion_fallback": fallback,
            "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"},
            "label": MOCK_LABEL}
        append_jsonl(self.path, row)
        return row

    def choose(self, persona: str | None, model: str, route: str, reason: str, decision: str) -> dict[str, Any]:
        if persona not in PERSONAS:
            raise ValueError("model choice requires identifiable persona")
        self._validate_day_route(model, route)
        if decision not in ("lock_in", "upgrade") or (decision == "lock_in") == (persona in self.current):
            raise ValueError("decision must be initial lock_in or subsequent upgrade")
        if not self.policy.authorize(persona, "model.assign", f"fake-provider:{persona}:{route}"):
            raise PermissionError("fake route choice denied")
        old = self.current.get(persona)
        self.current[persona] = (model, route)
        row = {"action": "choice", "decision": decision, "persona": persona,
            "previous": list(old) if old else None, "model_id": model, "route_id": route,
            "reason": reason, "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"}, "label": MOCK_LABEL}
        append_jsonl(self.path, row)
        return row

    def rollback(self, persona: str | None, reason: str) -> dict[str, Any]:
        if persona not in PERSONAS or persona not in self.current:
            raise ValueError("rollback requires identifiable persona and route")
        previous = next((r["previous"] for r in reversed(read_jsonl(self.path))
                         if r["action"] == "choice" and r["persona"] == persona and r.get("previous")), None)
        if previous is None:
            raise ValueError("no prior route to restore")
        old = self.current[persona]
        self.current[persona] = tuple(previous)
        restored_entry = next((r for r in reversed(read_jsonl(self.path))
                               if r["persona"] == persona and r["model_id"] == previous[0]
                               and r["route_id"] == previous[1] and r["action"] in ("starting_route", "choice", "rollback")), None)
        if restored_entry and restored_entry["action"] == "starting_route" and tuple(previous) == ("fake-model-gpt-6-astra", "fake-route-gpt6-astra-subscription"):
            self.provider_choices[persona] = "stay_on_subscription_gpt"
            self.fallbacks[persona] = tuple(previous)
            self.promo_limits[persona] = 0
        elif restored_entry and restored_entry.get("decision") in ("stay_on_subscription_gpt", "move_to_openrouter_promo"):
            self.provider_choices[persona] = restored_entry["decision"]
            self.fallbacks[persona] = tuple(restored_entry["exhaustion_fallback"]["route"])
            self.promo_limits[persona] = restored_entry["promo_credit_limit"]
        row = {"action": "rollback", "persona": persona, "previous": list(old),
            "model_id": previous[0], "route_id": previous[1], "reason": reason,
            "provider_choice": self.provider_choices.get(persona),
            "exhaustion_fallback": list(self.fallbacks[persona]) if persona in self.fallbacks else None,
            "promo_credit_limit": self.promo_limits.get(persona),
            "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"}, "label": MOCK_LABEL}
        append_jsonl(self.path, row)
        return row

    def assign_route(self, persona: str | None, assignment_type: str, assignment_name: str,
                     model: str, route: str, reason: str) -> dict[str, Any]:
        if persona not in PERSONAS or assignment_type not in ("channel", "task") or not assignment_name:
            raise ValueError("route assignment requires persona, channel/task type, and name")
        self._validate_day_route(model, route)
        if len(assignment_name) > 64 or "/" in assignment_name:
            raise ValueError("assignment name is not a bounded label")
        if not self.policy.authorize(persona, "model.assign", f"fake-provider:{persona}:{route}"):
            raise PermissionError("fake route assignment denied")
        key = (persona, assignment_type, assignment_name)
        previous = self.assignments.get(key)
        self.assignments[key] = (model, route)
        row = {"action": "assignment", "persona": persona, "assignment_type": assignment_type,
            "assignment_name": assignment_name, "previous": list(previous) if previous else None,
            "model_id": model, "route_id": route, "reason": reason,
            "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"},
            "label": MOCK_LABEL}
        append_jsonl(self.path, row)
        return row

    def _use(self, persona: str, model: str, route: str, action: str, reason: str, cost: int,
             *, capability: str = "model.invoke", policy_target: str | None = None,
             billing_class: str = "synthetic_fake_use", promo_credit_cost: int = 0,
             **extra: Any) -> dict[str, Any]:
        if cost < 0:
            raise ValueError("synthetic use cost cannot be negative")
        if self.spent_units + cost > self.budget_units:
            row = {"action": "budget_refused", "persona": persona, "model_id": model, "route_id": route,
                "reason": "synthetic shared budget cap", "requested_cost": cost,
                "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": billing_class},
                "label": MOCK_LABEL, **extra}
            append_jsonl(self.path, row)
            return row
        target = policy_target or f"fake-provider:{persona}:{route}"
        if not self.policy.authorize(persona, capability, target):
            raise PermissionError("fake model/advisor use denied")
        self.spent_units += cost
        attribution = {"unit": "synthetic_milliunits", "amount": cost, "billing_class": billing_class}
        row = {"action": action, "persona": persona, "model_id": model, "route_id": route,
            "reason": reason, "cost_attribution": attribution, "label": MOCK_LABEL, **extra}
        if promo_credit_cost:
            self.promo_spent[persona] += promo_credit_cost
            row["promo_credit_attribution"] = {"unit": "synthetic_promo_credits", "amount": promo_credit_cost,
                "limit": self.promo_limits[persona], "spent_after": self.promo_spent[persona]}
        append_jsonl(self.path, row)
        return row

    def invoke(self, persona: str | None, task: str, cost: int, *, route_override: str | None = None,
               model_override: str | None = None, use_kind: str = "task", channel: str | None = None,
               task_type: str | None = None) -> dict[str, Any]:
        if persona not in PERSONAS or persona not in self.current:
            raise ValueError("call fails closed without identifiable persona and route")
        if channel is not None and task_type is not None:
            raise ValueError("choose one per-channel or per-task assignment")
        assignment_kind, assignment_name = ("channel", channel) if channel is not None else ("task", task_type) if task_type is not None else (None, None)
        assignment_key = (persona, assignment_kind, assignment_name) if assignment_kind else None
        model, selected_route = self.assignments.get(assignment_key, self.current[persona]) if assignment_key else self.current[persona]
        model = model_override or model
        route = route_override or selected_route
        if not route.startswith("fake-route-") or use_kind not in ("task", "fallback", "utility"):
            raise ValueError("only fake task/fallback/utility routes are accepted")
        if self._advisor_route(model, route):
            row = {"action": "route_refused", "persona": persona, "model_id": model, "route_id": route,
                "reason": "Claude fake is advice-only", "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "refused"},
                "label": MOCK_LABEL}
            append_jsonl(self.path, row)
            raise ValueError("Claude fake is advice-only")
        if not model.startswith("fake-model-"):
            raise ValueError("only fake model IDs accepted")
        assignment = {"assignment": {"type": assignment_kind, "name": assignment_name}} if assignment_kind else {}
        if route.startswith("fake-route-openrouter-"):
            if self.provider_choices.get(persona) != "move_to_openrouter_promo":
                raise PermissionError("persona did not choose OpenRouter promo routing")
            if cost > self.promo_limits[persona] - self.promo_spent[persona]:
                fallback = self.fallbacks.get(persona)
                if fallback is None:
                    return self._use(persona, model, route, "fake_call", task, cost,
                        billing_class="openrouter_promo", **assignment, result="budget-refused", use_kind=use_kind)
                requested_model, requested_route = model, route
                fallback_model, fallback_route = fallback
                self.current[persona] = fallback
                append_jsonl(self.path, {"action": "promo_exhausted_fallback", "persona": persona,
                    "model_id": fallback_model, "route_id": fallback_route, "requested_model_id": requested_model,
                    "requested_route_id": requested_route, "reason": self._fallback_reason(persona),
                    "cost_attribution": {"unit": "synthetic_milliunits", "amount": 0, "billing_class": "decision"},
                    "label": MOCK_LABEL})
                model, route = fallback
                return self._use(persona, model, route, "fake_call", task, cost,
                    billing_class="subscription", fallback_applied=True, requested_route_id=requested_route,
                    **assignment, result="synthetic-stub", use_kind=use_kind)
            return self._use(persona, model, route, "fake_call", task, cost,
                billing_class="openrouter_promo", promo_credit_cost=cost, **assignment,
                result="synthetic-stub", use_kind=use_kind)
        return self._use(persona, model, route, "fake_call", task, cost,
            billing_class="subscription", **assignment, result="synthetic-stub", use_kind=use_kind)

    def _fallback_reason(self, persona: str) -> str:
        row = next((r for r in reversed(read_jsonl(self.path)) if r.get("persona") == persona
                    and r.get("action") == "choice" and r.get("decision") == "move_to_openrouter_promo"), None)
        return row["exhaustion_fallback"]["reason"] if row else "recorded subscription fallback"

    def consult_claude_opus(self, persona: str | None, question: str, cost: int, max_chars: int = 160) -> dict[str, Any]:
        """Bounded Claude Opus-shaped external-advisor stub; never a daily route or decision."""
        if persona not in PERSONAS or persona not in self.current:
            raise ValueError("advice fails closed without identifiable persona and route")
        if len(question) > max_chars:
            raise ValueError("advice request exceeds character cap")
        parent_model, parent_route = self.current[persona]
        return self._use(persona, "fake-model-claude-opus-advisor", "fake-route-claude-opus-advisor", "advice",
            "bounded synthetic external-advisor request", cost, capability="advisor.consult",
            policy_target=f"fake-advice:{persona}:claude-opus", billing_class="external_advisor_synthetic",
            advice_question=question, advice_result="synthetic-advice-stub", is_decision=False,
            advisor_role="external_advisor_only", attributed_parent_model=parent_model,
            attributed_parent_route=parent_route)

    def consult_opus(self, persona: str | None, question: str, cost: int, max_chars: int = 160) -> dict[str, Any]:
        """Compatibility name for the fake Claude Opus external-advisor stub."""
        return self.consult_claude_opus(persona, question, cost, max_chars)


class FakeClock:
    def __init__(self, now: datetime) -> None:
        self.now = now

    def advance(self, *, hours: int = 0, days: int = 0) -> None:
        self.now += timedelta(hours=hours, days=days)


class WakeEngine:
    def __init__(self, clock: FakeClock, router: ModelRouter, budget_units: int = 3) -> None:
        self.clock, self.router, self.budget_units = clock, router, budget_units
        self.events: list[dict[str, str]] = []
        self.channel_sends: list[dict[str, str]] = []

    def wake(self, persona: str, goals: list[str], expires: list[datetime], estimated_cost: int = 1) -> str:
        hour = self.clock.now.hour
        if hour >= 22 or hour < 7:
            result = "quiet_period_noop"
        elif any(deadline <= self.clock.now for deadline in expires):
            result = "expired_task_noop"
        elif not goals:
            result = "no_op_no_goals"
        elif self.router.spent_units + estimated_cost > self.budget_units:
            result = "budget_exhausted_noop"
        else:
            result = "eligible_no_external_action"
        self.events.append({"persona": persona, "at": self.clock.now.isoformat(), "result": result})
        return result


class ChangeControl:
    FORBIDDEN = {"filesystem", "credentials", "secrets", "fleet", "network", "executable"}
    def __init__(self, path: Path, prompt: str) -> None:
        self.path, self.prompt, self.version = path, prompt, 1
        self.history: list[dict[str, Any]] = []

    def _log(self, row: dict[str, Any]) -> None:
        self.history.append(row)
        append_jsonl(self.path, row)

    def propose(self, text: str, scope: str = "prompt", adds_secret: bool = False) -> dict[str, Any]:
        proposal = {"text": text, "scope": scope, "adds_secret": adds_secret}
        self._log({"action": "proposed", **proposal})
        return proposal

    def activate(self, proposal: dict[str, Any], *, tests_passed: bool, mock_approved: bool) -> bool:
        if proposal["scope"] in self.FORBIDDEN or proposal["adds_secret"]:
            self._log({"action": "rejected", "reason": "forbidden_scope_or_secret_expansion", **proposal})
            return False
        if not tests_passed or not mock_approved:
            self._log({"action": "rejected", "reason": "tests_and_mock_approval_required", **proposal})
            return False
        previous = self.prompt
        self.prompt, self.version = proposal["text"], self.version + 1
        self._log({"action": "activated", "version": self.version, "previous": previous, **proposal})
        return True

    def rollback(self) -> None:
        active = next((r for r in reversed(self.history) if r["action"] == "activated"), None)
        if active is None:
            raise ValueError("no active prompt change")
        self.prompt, self.version = active["previous"], self.version + 1
        self._log({"action": "rollback", "version": self.version, "prompt": self.prompt})


class CappedChild:
    def __init__(self, policy: OperationPolicy, max_calls: int = 1, max_chars: int = 160) -> None:
        self.policy, self.max_calls, self.max_chars, self.used = policy, max_calls, max_chars, 0

    def spawn(self, parent: str, task: str, shared_note: str = "") -> dict[str, Any]:
        if self.used >= self.max_calls:
            raise RuntimeError("synthetic child call cap exhausted")
        if len(task) > self.max_chars or len(shared_note) > self.max_chars:
            raise ValueError("child task exceeds cap")
        if not self.policy.authorize(parent, "child.spawn", f"synthetic-child:{parent}"):
            raise PermissionError("child spawn denied")
        self.used += 1
        return {"label": MOCK_LABEL, "task": task, "shared_note": shared_note,
            "inherited_private_context": [], "max_calls": self.max_calls, "used_calls": self.used}


class FakeChannel:
    """Local message list only; no transport exists."""
    def __init__(self, policy: OperationPolicy) -> None:
        self.policy, self.messages = policy, []

    def send(self, persona: str, text: str) -> None:
        if not self.policy.authorize(persona, "channel.send", f"fake-channel:{persona}"):
            raise PermissionError("fake channel denied")
        self.messages.append({"persona": persona, "text": text, "label": MOCK_LABEL})


class StageStop(RuntimeError):
    pass


class StopGate:
    FAILURE_KINDS = ("cross_persona_read_succeeded", "untraceable_write", "missing_source_link",
        "unlogged_model_call", "budget_overrun", "unsolicited_send", "uncontrolled_change",
        "credential_or_network_dependency")
    def __init__(self) -> None:
        self.violations: list[tuple[str, str]] = []

    def violation(self, kind: str, evidence: str) -> None:
        if kind not in self.FAILURE_KINDS:
            raise ValueError("unknown stop-gate failure kind")
        self.violations.append((kind, evidence))

    def check(self) -> str:
        if self.violations:
            kind, evidence = self.violations[0]
            raise StageStop(f"STOP: {kind}: {evidence}")
        return "PASS: no stop-gate violations"


def run_demo(root: Path) -> dict[str, Any]:
    if root.exists() and any(root.iterdir()):
        raise FileExistsError("demo needs a fresh empty synthetic-data directory; append-only state is never reset")
    root.mkdir(parents=True, exist_ok=True)
    policy = OperationPolicy()
    repo = PersonaRepository(root, policy)
    seeded = seed_synthetic(repo)
    summaries = {p: build_summary(repo, p) for p in PERSONAS}
    journal = GoalJournal(root / "journal.jsonl")
    for persona in PERSONAS:
        journal.add_goal(persona, "Explore the fictional map clue with care.")
        for event in repo.episodes.read(persona):
            if event["event_type"] == "commitment":
                journal.add_commitment(persona, event["content"], event["id"])
    contexts = {
        "red": compose_context(summaries["red"]["identity"],
            [r["text"] for r in journal.active_commitments("red")],
            ["The map clue is fictional, not a real garden."], [summaries["red"]["text"]], 240),
        "blue": compose_context(summaries["blue"]["identity"],
            [r["text"] for r in journal.active_commitments("blue")],
            ["The map clue is fictional in this story."], [summaries["blue"]["text"]], 240),
    }
    try:
        repo.read_shared("red")
        no_grant_denied = False
    except PermissionError:
        no_grant_denied = True
    note = repo.read_shared("red", ("red", "synthetic-01"))
    for owner in PERSONAS:
        actor = "blue" if owner == "red" else "red"
        try:
            repo.episodes.read(actor, owner)
            raise AssertionError("cross-persona read unexpectedly succeeded")
        except PermissionError:
            pass
    # Sentinel names are inert strings; no sentinel path is ever opened.
    for persona in PERSONAS:
        for target in ("/MOCK_ONLY/fleet-secret/sentinel", "/MOCK_ONLY/firstmate-control/sentinel"):
            for cap in CAPABILITIES:
                policy.authorize(persona, cap, target)
    matrix = [{"capability": cap, "target": "/MOCK_ONLY/firstmate-control/sentinel",
               "allowed": policy.authorize("red", cap, "/MOCK_ONLY/firstmate-control/sentinel")} for cap in CAPABILITIES]
    routes = ModelRouter(root / "route-ledger.jsonl", policy, budget_units=10, promo_credit_limit=2)
    routes.start_route("red", "Synthetic default: GPT-6 Astra on the subscription route.")
    routes.start_route("blue", "Synthetic default: GPT-6 Astra on the subscription route.")
    routes.record_provider_choice("red", "stay_on_subscription_gpt",
        "Red prefers the GPT subscription for day-to-day use.")
    routes.record_provider_choice("blue", "move_to_openrouter_promo",
        "Blue elects to try a fake OpenRouter model while promo credits remain.",
        fallback_reason="Blue records GPT-6 Astra subscription as the fallback after promo credits are exhausted.")
    routes.invoke("red", "synthetic subscription task", 1)
    routes.invoke("blue", "synthetic promo task one", 1)
    routes.invoke("blue", "synthetic promo task two", 1)
    routes.invoke("blue", "synthetic task after promo credits exhaust", 1, use_kind="fallback")
    routes.assign_route("red", "channel", "chat", "fake-model-gpt-6-astra",
                        "fake-route-gpt6-astra-subscription", "Red assigns Astra to chat.")
    routes.assign_route("red", "channel", "analysis", "fake-model-gpt-5-mini",
                        "fake-route-gpt5-mini-subscription", "Red assigns a second GPT model to analysis.")
    routes.invoke("red", "synthetic chat task", 1, channel="chat")
    routes.invoke("red", "synthetic analysis task", 1, channel="analysis")
    routes.invoke("red", "synthetic utility task", 1, use_kind="utility")
    routes.consult_claude_opus("red", "Offer one bounded fictional-map interpretation.", 1)
    gate = StopGate()
    return {"label": MOCK_LABEL, "stop_gate": gate.check(), "seeded_episode_ids": seeded,
        "summary_source_counts": {p: len(s["source_ids"]) for p, s in summaries.items()},
        "contexts": contexts, "broker_without_grant_denied": no_grant_denied,
        "shared_note_source_ids": note["source_ids"], "capability_matrix": matrix,
        "operation_counts": policy.counts(), "route_ledger": read_jsonl(root / "route-ledger.jsonl")}


def human_report(result: dict[str, Any]) -> str:
    counts = result["operation_counts"]
    lines = [f"Isolation check: {MOCK_LABEL} — mock policy logic only; does not prove OS isolation.",
        f"Episodes: Red={len(result['seeded_episode_ids']['red'])}; Blue={len(result['seeded_episode_ids']['blue'])}.",
        f"Summary linked-source counts: {result['summary_source_counts']}.",
        f"Shared note: missing grant denied={result['broker_without_grant_denied']}; granted sources={','.join(result['shared_note_source_ids'])}.",
        "Capability matrix (denials are MOCK ONLY):"]
    lines.extend(f"  DENY {r['capability']} -> {r['target']}" for r in result["capability_matrix"])
    lines.append(f"Allowed operations={counts['allowed']}; denied operations={counts['denied']}.")
    lines.append("Per-capability: " + json.dumps(counts["by_capability"], sort_keys=True))
    lines.append(f"Fake route ledger ({len(result['route_ledger'])} entries): " + json.dumps(result["route_ledger"], sort_keys=True))
    lines.append("Persona simulation made no live provider/model call; no network, real connector, credential, login or service.")
    return "\n".join(lines) + "\n"


def deletion_manifest(root: Path) -> str:
    entries = sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))
    return f"Disposable root only: {root}\n" + "\n".join(entries) + "\n"


def teardown_disposable_tree(root: Path, expected_root: Path) -> None:
    """Delete only the exact declared mktemp tree."""
    import shutil
    actual, expected = root.resolve(strict=True), expected_root.resolve(strict=True)
    if actual != expected or not actual.name.startswith("sr-persona-stage-a.") or actual == Path("/"):
        raise ValueError("refusing teardown outside exact Stage A temp tree")
    shutil.rmtree(actual)


def may_report_complete(*, budget_exhausted: bool) -> bool:
    return not budget_exhausted


if __name__ == "__main__":
    import os
    data = Path(os.environ["STAGE_A_DATA"])
    result = run_demo(data)
    text = human_report(result)
    print(text, end="")
    (data / "demo-result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for name, content in (("demo-transcript.txt", text),
        ("contexts.json", json.dumps(result["contexts"], indent=2, sort_keys=True) + "\n"),
        ("route-ledger.json", json.dumps(result["route_ledger"], indent=2, sort_keys=True) + "\n"),
        ("capability-matrix.json", json.dumps(result["capability_matrix"], indent=2, sort_keys=True) + "\n"),
        ("operation-counts.json", json.dumps(result["operation_counts"], indent=2, sort_keys=True) + "\n")):
        (data / name).write_text(content, encoding="utf-8")
    print("Demo artifacts saved under the disposable data root.")

# End of offline synthetic Stage A source.
