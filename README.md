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

## Roadmap

1. Realistic time units and validated activity budgets.
2. Sensory perception and richer spatial memory.
3. Disturbances, recovery and safe-place experiments.
4. Calibrate against published behavioral observations.
5. Optional 2D/3D visualization independent of simulation core.

Contributions should distinguish observed findings from implementation hypotheses.
