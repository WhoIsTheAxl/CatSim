"""Activity frequencies and room occupancy for experiments."""
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class Metrics:
    actions: Counter = field(default_factory=Counter)
    locations: Counter = field(default_factory=Counter)
    ticks: int = 0
    activity_ticks: Counter = field(default_factory=Counter)

    def record(self, event: str, location: str) -> None:
        self.ticks += 1
        self.locations[location] += 1
        if "starts " in event:
            self.actions[event.split("starts ", 1)[1].split(";", 1)[0]] += 1
        if "starts " in event or "continues " in event:
            activity = event.split("starts ", 1)[1] if "starts " in event else event.split("continues ", 1)[1]
            self.activity_ticks[activity.split(";", 1)[0]] += 1

    def report(self) -> dict:
        return {"ticks": self.ticks, "actions": dict(self.actions),
                "locations": dict(self.locations),
                "activity_ticks": dict(self.activity_ticks)}


def batch_experiment(seeds=range(10), steps=500):
    """Reproducible aggregate simulation experiment (not empirical validation)."""
    from catsim.agents.cat import Cat
    if steps < 0:
        raise ValueError('steps must be nonnegative')
    results = []
    for seed in seeds:
        cat = Cat(seed=seed)
        for _ in range(steps):
            cat.step()
        results.append(cat.metrics.report())
    actions = Counter()
    locations = Counter()
    activity_ticks = Counter()
    for report in results:
        actions.update(report['actions'])
        locations.update(report['locations'])
        activity_ticks.update(report['activity_ticks'])
    return {'runs': len(results), 'steps_per_run': steps,
            'actions': dict(actions), 'locations': dict(locations),
            'activity_ticks': dict(activity_ticks),
            'individual_runs': results}
