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
