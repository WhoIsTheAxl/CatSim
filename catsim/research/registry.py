"""Trace evidence provenance separately from unvalidated simulation parameters."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    key: str
    citation: str
    status: str
    note: str


REGISTRY = {
    "environmental_needs": Evidence(
        "environmental_needs",
        "Ellis et al. (2013), AAFP/ISFM Feline Environmental Needs Guidelines, "
        "doi:10.1177/1098612X13477537",
        "evidence-backed",
        "Safe places, resource access, play and environmental familiarity matter.",
    ),
    "utility_scores": Evidence(
        "utility_scores", "CatSim implementation", "experimental",
        "All numeric weights, cooldowns, durations and thresholds are unvalidated.",
    ),
}
