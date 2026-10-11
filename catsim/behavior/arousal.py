"""Interruptible rest and bounded response to perceived disturbances."""


def disturbance_intensity(observations) -> float:
    return max((item.intensity for item in observations if item.kind == "sound"),
               default=0.0)


def should_interrupt_rest(activity, observations, threshold: float = 55.0) -> bool:
    return (activity is not None and activity.name in {"sleep", "rest", "idle"}
            and disturbance_intensity(observations) >= threshold)
