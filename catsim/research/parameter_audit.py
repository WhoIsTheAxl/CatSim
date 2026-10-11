"""Explicit inventory of uncalibrated numeric model parameters.

This is a reproducible audit of defaults, not an empirical calibration.
"""
from dataclasses import asdict
from catsim.biology.activity_budget import ActivityBudget
from catsim.biology.metabolism import Metabolism
from catsim.biology.sleep_pressure import SleepPressure
from catsim.behavior.habituation import PlayHabituation
from catsim.behavior.regulation import Regulation


def inventory() -> dict[str, dict]:
    """Return model parameters and scientific status without running a cat."""
    return {
        "metabolism": asdict(Metabolism()),
        "activity_budget": asdict(ActivityBudget()),
        "regulation": asdict(Regulation()),
        "sleep_pressure": asdict(SleepPressure()),
        "toy_habituation": asdict(PlayHabituation()),
    }


def audit_parameters() -> dict:
    groups = inventory()
    return {
        "parameter_groups": len(groups),
        "numeric_parameters": sum(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for group in groups.values() for value in group.values()
        ),
        "all_numeric_coefficients_empirically_fitted": False,
        "parameters": groups,
    }
