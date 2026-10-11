# CatSim V1

CatSim V1 is the first research-informed source release of the modular
Python domestic-cat behavior simulator. Its cat agent, Mochi, has internal
needs, local perception, memory, navigation, utility-based action selection,
time-scaled activity effects and configurable simulation time.

## Included features

- Observation-based food, water, shelter and toy discovery.
- Navigation through a small multi-room environment.
- Feeding, drinking, grooming, playing, batting toys, stretching,
  observing, scratching, resting, sleeping, hiding and exploration.
- Toy habituation and experimental sleep-pressure regulation.
- Resource-choice improvements and a visible scratching surface.
- Seeded reproducibility, unit tests, activity budgets and cohort summaries.
- Research provenance registry and descriptive distribution-comparison tools.

## Scientific scope and limitations

**Research-informed does not mean biologically validated.** Environmental
guidelines motivate available resources; toy habituation research motivates
interest changes; general sleep-regulation theory motivates separate sleep
pressure. Action utilities, thresholds, metabolism, durations, and coefficients
are hypotheses rather than fitted values from domestic-cat datasets.

The 150-tick demo is a debugging scenario, **not** a 24-hour feline activity
budget. A seed cohort samples decision randomness, not biological diversity.
No independent empirical validation or predictive accuracy is claimed.

## Run from source

Requires Python 3.10+ (no external runtime dependencies expected):

```sh
python -m unittest discover -s tests -v
python -m catsim --steps 150 --debug
```

To run a compact multi-seed experiment:

```sh
python - <<'PY'
from catsim.research.validation import simulate_cohort
print(simulate_cohort(seeds=range(10), steps=150))
PY
```

## Source code

The release includes GitHub-generated source ZIP/TAR archives plus a
`CatSim-v1-source.zip` built from the exact `v1` commit. No binary
executable or APK is included.
