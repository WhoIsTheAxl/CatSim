# CatSim 🐈

**A Python cat-behavior simulator informed by published feline science.**

CatSim models how a cat's needs, environment, familiarity, and ongoing activities influence its choices. The goal is a reproducible simulation platform, **not** a claim that our current numerical rules are biologically validated.

## Quick start

Requires Python 3.10+; no dependencies.

```bash
python -m catsim --steps 100 --seed 42
python -m catsim --steps 50 --seed 42 --debug
python -m unittest discover -s tests -v
```

## Architecture

```text
catsim/
  __main__.py          CLI only
  core/math.py         Shared numeric utilities
  world/model.py       Locations and world topology
  world/objects.py     Independently movable resources
  world/environment.py Mutable world state
  world/events.py      External environmental stimuli
  perception/          Local observations and sensory filtering
  cognition/goals.py   Goal data representation
  behavior/navigation.py  Room-graph pathfinding
  research/registry.py Evidence provenance
  biology/needs.py     Physiological state dynamics
  biology/clock.py     Explicit simulation time
  biology/personality.py Individual traits
  behavior/regulation.py Eligibility thresholds
  simulation/metrics.py Activity and room statistics
  cognition/memory.py  Familiarity and discovered resources
  cognition/decision.py  Utility scoring and action selection
  behavior/activity.py   Activity data and duration
  behavior/execution.py  Behavior outcomes and cooldowns
  agents/cat.py        Agent orchestration
  simulation/runner.py Simulation loop and diagnostics
tests/
  test_simulation.py
```

Each domain owns its behavior. The CLI does not contain simulation logic. Numerical assumptions remain experimental and should eventually be configured and validated independently.

## v1.0 research pass 2 — Evidence-to-code comparison

**Literature reviewed:** Ellis et al. (2013), AAFP/ISFM Feline
Environmental Needs Guidelines, DOI 10.1177/1098612X13477537.
The guidelines recommend multiple separated key resources, safe places,
opportunities for scratching and predatory play, and individual choice.

**Codebase comparison (before changes):**
- `world/objects.py`: food and water co-located in Kitchen; no scratching
  surface or toileting resources; two shelters already present.
- `cognition/decision.py`: local toy/shelter/food/water observation already
  supported; no scratching action.
- `biology/activity_budget.py`: fixed meal and drinking relief rates;
  **not** measurements of actual intake or satiety.
- `biology/sleep_pressure.py`: independent state, but rates and thresholds
  remain hypotheses, not polysomnographic calibration.

**Implemented in this pass:**
- Added a separate water station in Bedroom **while retaining Kitchen water
  for backwards compatibility**; this is a partial resource-separation step.
- Added a visible scratching post in Living Room and an observation-gated
  `scratch` action with a 2-minute provisional duration.
- Added evidence provenance and five environment/perception regression tests.

**Remaining scientific gaps:** Food and water are still co-located in Kitchen,
there is no litter resource, scratch motivation is heuristic, and no measured
activity-budget calibration exists. The guideline is a welfare recommendation,
**not a numerical model of how often cats scratch or drink**. This pass
improves the represented environment, not demonstrated predictive accuracy.

## v1.0 research track — Scientific validation infrastructure (in progress)

**v1.0 is NOT scientifically validated yet.** This initial research pass adds:

- An auditable evidence registry with publication identifiers, model mappings,
  evidence status and limitations. The general two-process sleep framework is
  explicitly marked **cross-species theory**, not feline calibration.
- `catsim.research.validation.simulate_cohort` for seeded, reproducible
  behavioral proportions (movement destinations are aggregated).
- `total_variation` and `compare_cohort` to compare modeled activity
  distributions with **user-supplied** empirical proportions.
- Eight software tests for distribution correctness and provenance.

Example (summary only; no giant debug output):

```bash
python - <<'PY'
from catsim.research.validation import simulate_cohort
from catsim.research.registry import audit
print(audit())
print(simulate_cohort(seeds=range(10), steps=150))
PY
```

### Validation protocol before any realism claim

1. Select a defined target population (e.g., indoor adult companion cats),
   context, time window, measurement method and relevant health constraints.
2. Extract quantitative reference distributions from accessible original
   publications. Record sample size, sampling biases and uncertainty.
3. Define an observation mapping between study behaviors and simulator
   actions. Never equate `rest` with EEG-confirmed sleep.
4. Fit parameters on a training dataset, preserving a separate validation
   dataset. Report error bars and sensitivity across seeds and assumptions.
5. Test sleep bouts, feeding intervals, play and location use over appropriate
   observation windows. Short 150-tick runs are debugging samples, **not**
   representative 24-hour activity budgets.
6. Publish discrepancies and unsupported assumptions rather than tuning to
   a visually appealing trace.

**No empirical activity targets or fitted physiological coefficients are
bundled yet.** Passing tests proves software invariants, not cat realism.

## v0.9 — Completed experimental feature set (pending test verification)

- **Toy habituation:** play with an unchanged toy reduces future interest;
  interest recovers during other activities. Toy novelty can reset habituation.
- **Sleep pressure:** an independent homeostatic state rises during waking
  activities and falls during sleep. It contributes to sleep utility alongside
  fatigue and the existing daily rhythm. This is a simplified mechanism,
  **not** a validated feline sleep model.
- **Additional actions:** `stretch` (brief low-commitment movement),
  `observe` (quiet environmental attention), and `bat_toy` (shorter,
  lower-intensity toy interaction). Toy batting requires a perceived toy.
  Actions remain utility-driven, not artificially rotated.
- **Tests:** added dedicated tests for new actions, toy perception, sleep
  pressure, need effects, seeded reproducibility and tick accounting.
- **Limitations:** Numerical rates, action durations and utility weights
  are hypotheses; observe/stretch currently have no specialized physiological
  outcome. Sleep is not yet divided into REM/non-REM stages. Activity
  comparisons to real cats are a v1.0 research milestone.

## v0.9 — Behavioral habituation (first implementation pass)

- Added time-scaled **toy-play habituation**: repeating play with an unchanged
  toy progressively lowers its attractiveness, while time spent on other
  activities allows interest to recover.
- A `novel_toy()` reset is available for future toy-rotation and stimulus
  change events; **automatic toy rotation is not implemented yet**.
- Added six tests for habituation, recovery, time scaling, novelty, utility
  effects and deterministic simulation.

**Research connection:** Hall, Bradshaw & Robinson (2002), *Object play in
adult domestic cats: the roles of habituation and disinhibition*,
[DOI 10.1016/S0168-1591(02)00153-3](https://doi.org/10.1016/S0168-1591(02)00153-3),
observed habituation to an unchanged toy and renewed play after changing toy
characteristics. The **numerical habituation rates are invented model
parameters, not fitted experimental estimates**.

### Road to v1.0: evidence and calibration

v1.0 should require a traceable evidence registry (population, methods,
sample sizes, outcomes, limitations), reference activity-budget distributions,
multi-seed comparison experiments, parameter sensitivity analysis and explicit
holdout validation. Sleep bouts, meal patterns, individual differences and
environmental context require additional research before claiming realism.
Passing software tests is not scientific validation.

## v0.8 — Need-directed behavior and activity measurement (experimental)

- **Resource discovery:** Hunger and thirst can motivate exploration even when
  food or water has not yet been observed. Search prioritizes less-familiar
  adjacent rooms; it does **not** inspect hidden objects or know where food is.
- **Resource-directed navigation:** Previously observed resources motivate
  return trips. Existing navigation targets compete through the same utility
  scores as other actions; debug scores and selected actions stay consistent.
- **Urgent interruption:** Urgent hunger or thirst can preempt play, grooming,
  idle, quiet rest or investigation when an actionable option exists.
- **Behavioral time budgets:** Metrics now track time spent executing each
  activity in ticks (including interrupted starts), in addition to start counts
  and room occupancy. Convert ticks to minutes using the clock's tick length.
- **Regression tests:** Unknown-resource behavior, exploration, navigation,
  interruption, metrics and seeded determinism.

The coefficients are **untested behavioral hypotheses**. These changes
address logical failures observed in v0.7, but do not establish that the
resulting activity budgets match real cats. Empirical calibration, sleep
architecture, meal sizes, stimulus habituation and welfare-relevant behavioral
variation remain open research tasks.

## v0.7 — The Normalization Overhaul (experimental)

The first normalization pass changes **both** physiological rates and behavior
execution. It addresses a major v0.6 inconsistency: needs accumulated slowly
per simulated hour, but resting, sleeping, playing and feeding caused enormous
instantaneous changes after just a few ticks.

- `catsim/biology/activity_budget.py` applies action effects incrementally,
  proportional to simulated elapsed minutes. All coefficients are **model
  assumptions**, not values measured in domestic cats.
- Rest, sleep, feeding, drinking, grooming, play, hiding, investigation and
  movement no longer create fixed, end-of-action physiology jumps.
- Activities have durations in **simulated minutes**; the simulation clock
  converts them to tick counts. Cooldowns use simulated minutes too.
- Idling is always eligible. Familiar, low-novelty environments no longer
  automatically force negative-utility room-to-room movement.
- Rest is more attractive at observed shelters. A new regression suite checks
  duration scaling, reproducibility and no forced movement.

**Important limitations:** Sleep architecture, meal-size dynamics, habituation,
safety assessment, event scheduling and statistical comparison with empirical
cat observations remain future work. Tick durations not evenly dividing an
activity's duration round up to a whole tick. Behavior thresholds and all rates
remain uncalibrated. Passing software tests establishes correctness against
specified invariants, **not biological validity**.

## v0.6 — Biological time, navigation and experiments (experimental)

- `Metabolism` provides configurable per-hour need-change rates, applied using `SimulationClock.tick_minutes`.
- `Cat(tick_minutes=..., metabolism=...)` enables controlled time-scale experiments.
- Resource navigation now retains a destination across intermediate rooms until arrival or a competing immediate need.
- `catsim.simulation.metrics.batch_experiment(seeds, steps)` aggregates action and occupancy statistics over reproducible seeds.
- Five regression tests cover time normalization, clock configuration, batch determinism and navigation.

**Scientific status:** Per-hour rates, activity durations, feeding/sleeping effects and navigation priority rules are still hypotheses. This version changes the simulation's baseline dynamics substantially; compare runs cautiously. Tests must be run locally/CI before treating the release as stable.

## v0.5 — Research-informed rest and activity (experimental)

- Daily activity drive with configurable simulation-clock input; twilight peaks are a **hypothesis-inspired curve**, not fitted measurements.
- Rest/sleep motivation changes with time of day.
- Shelter-aware sleep preference based on **remembered** resource locations.
- Newly detected loud sounds can interrupt rest; a sound is not counted as a new threat every tick.
- Dedicated tests in `tests/test_rest_rhythm.py` and Python 3.14 CI coverage.

Evidence: AAFP/ISFM environmental needs guidelines (2013) describe the importance of secure resting locations. Published activity studies show that cat rhythms vary with environment and individuals; a single twilight curve cannot represent every cat. See [comparison of indoor/outdoor activity and feeding rhythms](https://pmc.ncbi.nlm.nih.gov/articles/PMC9494968/).

**Limitations:** Rhythm coefficients, time scale, noise threshold, and shelter scores are unvalidated; disturbance events must still be injected explicitly; this does not simulate sleep physiology or actual sleep-stage architecture.

## v0.4 — Behavioral regulation and observability

- **Action eligibility:** eating, drinking, sleeping, resting, grooming, playing, hiding and investigating have configurable minimum-need gates. These are **unvalidated simulation parameters**.
- **Exploration:** a baseline exploratory drive competes with physiological needs, reducing the kitchen-trap failure mode.
- **Individual differences:** configurable boldness, curiosity and playfulness coefficients.
- **Clock:** explicit tick duration and elapsed simulated time (not a biologically calibrated clock).
- **Metrics:** count started activities and room occupancy for experimental comparisons.
- **Debug scores:** raw utility and randomized final utility are shown together.
- **Regression tests:** `tests/test_regulation.py` covers behavior gating and instrumentation.

The goal object remains a lightweight record, **not** a complete persistent multi-room planning system. Future work includes persistent goals, time-dependent activity patterns, stimulus decay and calibration to real feline observations.

## v0.2 prototype

- Internal hunger, thirst, fatigue, fear, curiosity and grooming motivation.
- Connected rooms with food, water, shelter and toys.
- Exploration learns resource locations instead of knowing the entire world.
- Action persistence, durations and cooldowns to reduce oscillation and grooming loops.
- Reproducible runs and optional utility-score diagnostics.
- Unit tests for reproducibility, resource learning, and behavioral invariants.

## Research basis and limits

The [2013 AAFP/ISFM Feline Environmental Needs Guidelines](https://doi.org/10.1177/1098612X13477537) motivate safe places, separate resources, play/predatory opportunities and familiarity. See [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11383066/).

**Evidence-backed:** Cats benefit from appropriate safe places, resources and environmental opportunities.

**Research-informed modeling:** Security, familiarity and resource access influence behavioral choices.

**Experimental / unvalidated:** All numeric scores, rates, thresholds, personality coefficients and action durations in this prototype. Outputs must not be interpreted as scientific predictions or veterinary guidance.

## Continuous integration

The [GitHub Actions test workflow](.github/workflows/tests.yml) runs on **every push**, on pull requests, and by manual dispatch. It compiles Python sources, runs the `tests/` suite, and smoke-tests the CLI on Python 3.10–3.13.

## Perception prototype

Resources are individual world objects. Cats perceive only visible objects in their current room, remember discovered resources, and update those memories after observing changes. Navigation supports shortest paths across connected rooms. External sound and novel-object events can be injected into the environment.

**Current limitations:** senses are room-local abstractions, goal records do not yet provide full multi-room intention persistence, stimulus decay is not yet implemented, and behavior coefficients remain experimental.

## Roadmap

1. Realistic time units and validated activity budgets.
2. Sensory perception and richer spatial memory.
3. Disturbances, recovery and safe-place experiments.
4. Calibrate against published behavioral observations.
5. Optional 2D/3D visualization independent of simulation core.

Contributions should distinguish observed findings from implementation hypotheses.
