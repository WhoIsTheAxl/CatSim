"""Auditable provenance for research-informed CatSim mechanisms.

A paper supporting a *mechanism* does not validate CatSim's numerical rates.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    key: str
    citation: str
    status: str
    note: str
    doi: str | None = None
    model_component: str | None = None
    limitation: str = ""


REGISTRY = {
    "environmental_needs": Evidence(
        "environmental_needs",
        "Ellis et al. (2013), AAFP/ISFM Feline Environmental Needs Guidelines",
        "research-informed",
        "Safe places, separated resources, play opportunities and familiarity matter.",
        "10.1177/1098612X13477537",
        "world / cognition / resting",
        "Clinical environmental recommendations do not determine action probabilities.",
    ),
    "toy_habituation": Evidence(
        "toy_habituation",
        "Hall, Bradshaw & Robinson (2002), Object play in adult domestic cats",
        "research-informed",
        "Play responses can habituate to unchanged objects and recover with stimulus changes.",
        "10.1016/S0168-1591(02)00153-3",
        "behavior/habituation.py",
        "Toy-specific effects and numeric decay/recovery rates are not calibrated.",
    ),
    "two_process_sleep": Evidence(
        "two_process_sleep",
        "Borbély (1982), A two process model of sleep regulation",
        "cross-species-theory",
        "Separate homeostatic sleep pressure from circadian modulation.",
        "10.1111/j.1365-2869.1982.tb00324.x",
        "biology/sleep_pressure.py / biology/rhythm.py",
        "General sleep-regulation framework; does not establish feline-specific rates.",
    ),
    "utility_scores": Evidence(
        "utility_scores", "CatSim implementation", "experimental",
        "All numeric weights, cooldowns, durations and thresholds are unvalidated.",
        model_component="cognition/decision.py / biology",
        limitation="No independent parameter fitting or predictive validation.",
    ),
}


def audit() -> dict[str, object]:
    """Machine-readable evidence audit without implying biological validity."""
    statuses = {}
    for item in REGISTRY.values():
        statuses[item.status] = statuses.get(item.status, 0) + 1
    return {
        "entries": len(REGISTRY),
        "statuses": statuses,
        "missing_doi": sorted(k for k, v in REGISTRY.items() if v.doi is None),
        "without_limitations": sorted(k for k, v in REGISTRY.items()
                                      if not v.limitation),
        "numerical_parameters_validated": False,
    }
