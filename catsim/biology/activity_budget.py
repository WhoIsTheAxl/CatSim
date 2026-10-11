"""Time-scaled activity effects.

Coefficients are explicit simulation hypotheses, not measured cat physiology.
The same elapsed duration should produce the same total effect irrespective
of simulation tick size.
"""
from dataclasses import dataclass
from catsim.core.math import clamp


@dataclass(frozen=True)
class ActivityBudget:
    sleep_recovery_per_hour: float = 9.0
    rest_recovery_per_hour: float = 3.0
    travel_fatigue_per_hour: float = 3.0
    play_fatigue_per_hour: float = 5.0
    food_relief_per_hour: float = 180.0
    water_relief_per_hour: float = 300.0
    grooming_relief_per_hour: float = 20.0
    play_relief_per_hour: float = 20.0
    hide_fear_relief_per_hour: float = 8.0
    investigate_relief_per_hour: float = 12.0


def apply_activity(needs, name: str, minutes: float, budget: ActivityBudget):
    if minutes < 0:
        raise ValueError("minutes must be nonnegative")
    h = minutes / 60.0
    if name == "sleep":
        needs.fatigue = clamp(needs.fatigue - budget.sleep_recovery_per_hour * h)
    elif name == "rest":
        needs.fatigue = clamp(needs.fatigue - budget.rest_recovery_per_hour * h)
    elif name == "eat":
        needs.hunger = clamp(needs.hunger - budget.food_relief_per_hour * h)
    elif name == "drink":
        needs.thirst = clamp(needs.thirst - budget.water_relief_per_hour * h)
    elif name == "groom":
        needs.grooming_urge = clamp(needs.grooming_urge - budget.grooming_relief_per_hour * h)
    elif name in {"play", "bat_toy"}:
        factor = 0.5 if name == "bat_toy" else 1.0
        needs.play_urge = clamp(needs.play_urge - budget.play_relief_per_hour * h * factor)
        needs.fatigue = clamp(needs.fatigue + budget.play_fatigue_per_hour * h * factor)
    elif name == "hide":
        needs.fear = clamp(needs.fear - budget.hide_fear_relief_per_hour * h)
    elif name == "investigate":
        needs.curiosity = clamp(needs.curiosity - budget.investigate_relief_per_hour * h)
    elif name.startswith("move:"):
        needs.fatigue = clamp(needs.fatigue + budget.travel_fatigue_per_hour * h)
