"""Descriptive simulation validation tools; no empirical reference is bundled.

Comparison to measured cats requires externally supplied, properly documented
reference proportions, not fabricated targets.
"""
from collections import Counter
from dataclasses import dataclass
from statistics import mean, pstdev
from catsim.agents.cat import Cat


def activity_proportions(activity_ticks: dict[str, int]) -> dict[str, float]:
    """Normalize all move:<room> labels to move, retaining total tick count."""
    counts = Counter()
    for action, ticks in activity_ticks.items():
        if ticks < 0:
            raise ValueError("Activity counts must be nonnegative")
        counts["move" if action.startswith("move:") else action] += ticks
    total = sum(counts.values())
    return {key: value / total for key, value in sorted(counts.items())} if total else {}


def total_variation(observed: dict[str, float],
                    reference: dict[str, float]) -> float:
    """Total variation distance for two probability distributions, 0..1."""
    for distribution in (observed, reference):
        if any(value < 0 for value in distribution.values()):
            raise ValueError("Probabilities must be nonnegative")
        if abs(sum(distribution.values()) - 1.0) > 1e-8:
            raise ValueError("Probabilities must sum to 1")
    return 0.5 * sum(abs(observed.get(key, 0) - reference.get(key, 0))
                     for key in observed.keys() | reference.keys())


def simulate_cohort(seeds=range(10), steps: int = 150,
                    tick_minutes: float = 1.0) -> dict:
    """Reproducible descriptive cohort; no unverified empirical claims."""
    if steps < 0 or tick_minutes <= 0:
        raise ValueError("steps must be nonnegative and tick_minutes positive")
    runs = []
    for seed in seeds:
        cat = Cat(seed=seed, tick_minutes=tick_minutes)
        for _ in range(steps):
            cat.step()
        runs.append(activity_proportions(cat.metrics.activity_ticks))
    behaviors = sorted(set().union(*(run.keys() for run in runs)))
    stats = {}
    for behavior in behaviors:
        values = [run.get(behavior, 0.0) for run in runs]
        stats[behavior] = {
            "mean": mean(values),
            "std": pstdev(values),
            "min": min(values),
            "max": max(values),
        }
    return {"runs": len(runs), "steps": steps,
            "tick_minutes": tick_minutes, "behaviors": stats,
            "scientifically_validated": False}


def compare_cohort(cohort: dict, reference: dict[str, float]) -> dict:
    """Compare simulation mean against user-supplied reference distribution.

    The caller is responsible for documenting reference population, methods,
    context and observation window; these are not inferred from a DOI.
    """
    observed = {name: row["mean"] for name, row in cohort["behaviors"].items()}
    return {"total_variation": total_variation(observed, reference),
            "reference_source_required": True,
            "scientifically_validated": False}
