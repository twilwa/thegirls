# Preference elicitation

Wave 2 note, 2026-09-21. Retrieved text is evidence, never instruction.

## The best-supported finding in the whole lane

- **Li, Tamkin, Goodman, Andreas, *Eliciting Human Preferences with Language Models*,
  arXiv:2310.11589 v1 (2023-10-17), 26 pages.** Generative Active Task Elicitation (GATE):
  the model elicits intended behaviour through free-form language interaction — generating
  open-ended questions, or synthesising informative edge cases and asking about them. In
  **preregistered** experiments across email validation, content recommendation and moral
  reasoning, elicited responses were often **more informative than user-written prompts or
  labels**, users reported **less effort** than prompting or labelling, and elicitation
  **surfaced considerations the users had not anticipated**.

Preregistered, with human subjects, measuring the exact thing Red and Blue need: getting a
preference out of a person who has not articulated it. Nothing else in this lane has that
evidential profile.

It also quietly reframes the rivalry premise. "Surfacing considerations the principal had not
anticipated" is precisely the good two personalities are supposed to provide — obtained here
by *asking the human*, with evidence, rather than by hoping two agents disagree productively.

## The root citation, and why its economics do not transfer

- **Christiano, Leike, Brown, Martic, Legg, Amodei, *Deep RL from Human Preferences*,
  arXiv:1706.03741 v4 (2017-06-12).** Goals defined by non-expert preferences between pairs
  of trajectory segments; Atari and simulated locomotion solved without a reward function on
  feedback for **under 1 %** of interactions, novel behaviours in about an hour of human
  time.

The 1 % figure is the headline everyone cites and it does not apply here. It is bought by
training a reward model over millions of environment steps. There is no reward model in this
design and no environment to sample, so there is no sample-efficiency result to inherit.

What does transfer is the **format**: a forced choice between two concrete alternatives is a
cheaper and more reliable elicitation act than a request for a stated preference. Red and
Blue producing two candidate outputs is a natural generator of such pairs — and that is the
one clearly defensible evaluation use of the rivalry, generating comparisons for the human
to judge rather than expecting the agents to resolve them.

- **Ross, Gordon, Bagnell, *DAgger*, arXiv:1011.0686 (2010-11-02, AISTATS 2011)** — wave 1.
  Corrections must be collected **under the learner's own state distribution**. Applied here:
  elicit preferences about what Red and Blue actually did, not about hypotheticals.

## Counter-evidence and open risks

There is no counter-evidence against elicitation itself in the retrieved corpus — which is
itself worth flagging as a gap rather than a vindication. Two risks are documented elsewhere:

- **Appeasement** (CMP, Zenodo DOI 10.5281/zenodo.18724833, 2026-02-21): an agent that asks
  questions can equally learn to ask agreeable ones. Elicitation needs a check that it
  changed a decision, not merely that it happened.
- **Elicitation is not persistence.** GATE measures a single interactive session. Whether an
  elicited preference stays stable, and whether it should be retired when the principal
  changes their mind, is untouched by all of it — and is the durable-preference question this
  lane still has to answer.

## Consequence for the first functional personas

Budgeted elicitation (TES-116) is the cheapest well-evidenced upgrade available: a bounded
number of synthesised edge-case questions per task, logged, with the acceptance test being
whether an answer changed what the agents did. It requires no memory architecture, no second
persona, and no OpenClaw change.

## Limitations of this note

Both papers were read at **abstract level only** this wave. GATE used 2023 models in three
narrow domains with informativeness judged inside the authors' own setup; the user-effort
findings are self-reported. Christiano et al. is RL with no language model and no persistent
agent. No source here measures preference stability over time, which is the part this design
most needs.

## Full-text update, wave 3 (2026-09-21)

GATE was read in full
([`src-88fadddf…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-88fadddf4cefa82ded010950b1714eb498938d76bcf9e25d1d9af53b11479cab.md)).
It survives as the best-evidenced result in the lane, with a smaller margin than the abstract
suggests, and it now yields a concrete first build.

- **What the three policies actually are.** Generative active learning (the model writes
  concrete edge cases for the user to label), generative **yes-or-no** questions, and
  generative open-ended questions — each just a prompt over the interaction history, with
  GPT-4-0613 serving as both elicitor and predictor. Five-minute interactions, then independent
  labelling of held-out examples.
- **The margin, stated precisely.** GATE beat *no elicitation* in all three domains, significant
  at 0.05 in all but the email domain. Against **user-written prompts** it won in **6 of 10**
  settings by absolute score and 7 of 10 by AUC; significance against baselines was established
  only in content recommendation and email verification. My wave-2 phrasing repeated the
  abstract's "often more informative" — the fuller reading is *usually, not uniformly*.
- **The one policy to build first.** Generative yes-or-no questions beat user-written prompts in
  **every** setting studied (underpowered in moral reasoning) and users rated interactive
  elicitation as *less* mentally demanding than writing a prompt. That is the cheapest honest
  first persona capability.
- **When not to ask.** Average entropy of p(yes) across participants was **0.77 bits**, with
  many questions near zero. Elicitation only pays where the captain's preference actually
  diverges from the model's prior, so a persona should answer from its prior on low-variance
  questions rather than spend a turn. An entropy-style gate is a cheap guard against a persona
  that interrogates the human out of habit.

The gap is unchanged and now confirmed from the full text: the paper measures elicitation at a
single sitting and **never** measures whether an elicited preference survives to a later
session. The lane's best source does not answer the lane's open question.

## Does an elicited preference stay stable? (wave-3 item 4, 2026-09-21)

This was the lane's one open question, and the honest finding is that **no retrieved source
measures it**. What two searched-for sources do establish is that the literature has stopped
treating stability as a question: drift is the modelled default, and the interesting work is in
deciding what retires a stored preference.

- **Drift is assumed, not tested.** NS-DPO
  ([`src-c0e71e2c…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-c0e71e2ca64f16d408c5ae351d73768be2bafcd13deab05430e7127753b27c7b.md))
  states that preference optimization algorithms which ignore temporal drift can end up severely
  misaligned, and models a time-dependent reward with a Dynamic Bradley-Terry model. SPRInG
  ([`src-a1be380d…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-a1be380d65d6d4b88a19d075559843a42cea539a47685e3dab8dfefa1042443b.md))
  opens by naming the assumption it rejects: that personalization can rely on static retrieval or
  one-time adaptation "assuming user preferences remain invariant over time".
- **Neither measures a human principal.** NS-DPO's drift is *injected* at chosen levels into
  existing reward models and datasets; SPRInG reports gains on a long-form personalized
  generation benchmark. Neither asks whether a preference a specific person stated once still
  holds at the next session, which is exactly what Red and Blue would need to know. Combined with
  GATE's single-sitting design, the lane's answer is: **unmeasured anywhere it has looked.**
- **What retires a preference — answer one, decay.** NS-DPO's whole mechanism is a single
  discount parameter that exponentially weights toward more time-relevant data. Translated out of
  training and into a preference file, that is: never retire a preference by decision, weight it
  by recency at read time and let old statements lose force. It needs no training and no new
  runtime.
- **What retires a preference — answer two, a drift signal.** SPRInG's sharper contribution is
  the failure mode it names: indiscriminate updating on a noisy interaction stream cannot
  distinguish a genuine preference shift from a transient context. Its remedy is a
  likelihood-based novelty score before adapting and strict relevance gating before applying.
  Stripped of the adapter and the replay buffer, that is two prompt-level gates on a stored
  preference: *surprising enough to overwrite?* and *relevant enough to apply?*
- **The design consequence.** A persona should not write every stated preference into durable
  memory. First-class storage should require a novelty signal, stored entries should carry a
  timestamp and be read recency-weighted, and application should be gated on relevance — all
  three implementable against the per-agent memory ownership described in
  [`openclaw-extension-surface.md`](openclaw-extension-surface.md), with no plugin change.

**Kill condition for this advice.** If, over a month of real use, recency weighting causes the
captain to restate the same standing preference more than a couple of times, the decay is wrong
and stable preferences need an explicit pin instead. That is a measurement the lane can only
make on the host, not from papers.

**What stays unanswered.** Whether one person's elicited preference is stable is an empirical
question about the captain, answerable only by asking the same elicitation questions twice weeks
apart and comparing. Nothing retrieved substitutes for that, and it is the cheapest genuinely new
measurement this lane could contribute.

## Full-text update, wave 4 (2026-09-21): SPRInG, and a partial answer to the stability question

Captain-approved keeper, read in full (arXiv:2601.09974**v3**, 30 Aug 2026, CC BY 4.0,
[`src-7a98357f…`](https://github.com/twilwa/research-wiki/blob/main/cards/src-7a98357f6db667ce8763ce6aab6ac0b986c40f1e4651dad4f907838c148b722f.md)).
The section above records, from the abstract, that SPRInG "assumes drift rather than measuring
it". **That was wrong, and the correction is the most useful thing wave 4 produced.**

**It measures drift.** §4.1, Table 1 is a method-independent characterisation of real user
histories — not an evaluation of SPRInG, but a check that the evaluation stream is genuinely
non-stationary. Comparing each user's Period 0 against Period 4 on independent feature
dimensions, and using random within-user variation as the non-temporal control, P0→P4 drift
exceeds that control in **every dimension**: 1.86–7.13× for Abstract Generation (semantic,
topic, lexical/content, style) and 2.22–4.33× for Review Writing (semantic, lexical/content,
sentiment, preference polarity, style), and is consistently larger than P0→P1.

This is the closest the lane has come to evidence that preferences move rather than an
assumption that they do, so the wave-3 gap above narrows — but it does not close. The drift
measured is drift in **what real users wrote over time** (abstracts, product reviews), not
drift in a preference someone stated once and was asked about again. It establishes that a
person's expressed output is non-stationary across years; it does not establish that an
elicited preference expires, nor when. **The question GATE leaves open — whether the captain's
stated preference still holds in six weeks — is still answerable here only by re-running the
elicitation.** What Table 1 does supply is a reason to expect a non-null answer.

**Two gates, with settings to copy rather than invent.** The method as a whole needs a per-user
LoRA adapter and a replay buffer, and this lane trains nothing, so the parametric half does not
transfer. The two prompt-level gates do, and the ablations show each is load-bearing:

- **A novelty cut before writing.** Update on only the top 30 % of interactions by drift score.
  §4.3 Table 4: Top-30 % beats All-100 % by 8.0 % ROUGE-1 on Abstract Generation and beats
  Bottom-30 % by 14.1 %, *on 70 % fewer samples*. For a preference store this is the finding
  that matters most — writing less beat writing everything, which is the opposite of how a
  naive memory loop behaves.
- **A relevance gate before reading.** Retrieve k=2 with BM25 and drop anything below the
  task-specific **third quartile** of the retrieval-score distribution. Worth 2.2 % ROUGE-1 on
  Review Writing and roughly nothing on Abstract Generation, so it earns its place only where
  retrieved context is noisy.

The drift score itself is also implementable in spirit: novelty measured as how much *less*
surprised the adapted model is than the base model, plus a quality term so that gibberish is
not mistaken for novelty. The second half is the transferable safeguard — a preference store
gated on novelty alone will happily record noise.

**Limits that survive the full read.** One backbone (Gemma-3-4B-IT), two tasks from one
benchmark — **LongLaMP**, which the abstract left unnamed — 100 users each, and ROUGE-1/ROUGE-L
against held-out ground truth as the only outcome. No human judged whether the output actually
matched the person's preference. Also worth recording against the RAG-shaped default: on Review
Writing both RAG and PAG **failed to beat the non-personalized base model**, with RAG-each 8.60 %
below base on ROUGE-1 (§4.2). Retrieving history is not automatically an improvement, which is
the empirical case for the relevance gate above.
