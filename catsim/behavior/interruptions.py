"""Need-driven interruption of nonessential activities.

Urgent resource needs may interrupt play, grooming, idling or quiet rest.
A cat already eating or drinking is not interrupted by its own needs.
Threshold margins prevent oscillation around eligibility boundaries.
"""


def urgent_need(cat) -> bool:
    n, reg = cat.needs, cat.regulation
    return (n.hunger >= reg.eat_start + 15 or
            n.thirst >= reg.drink_start + 15)


def should_interrupt_for_needs(cat) -> bool:
    activity = cat.activity
    if activity is None:
        return False
    if activity.name not in {"play", "groom", "idle", "rest", "investigate"}:
        return False
    if not urgent_need(cat):
        return False
    # If neither resource is known, exploration can still find one.
    # Avoid needless cancellation when there is no actionable alternative.
    options = cat.utilities()
    movement = max((value for name, value in options.items()
                    if name.startswith("move:")), default=0)
    immediate = max(options.get("eat", 0), options.get("drink", 0))
    return max(movement, immediate) >= 25
