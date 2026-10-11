from catsim.agents.cat import Cat

def run(steps: int = 100, seed: int = 42, debug: bool = False) -> list[str]:
    cat = Cat(seed=seed)
    events = []
    for tick in range(1, steps + 1):
        event = cat.step()
        n = cat.needs
        line = (f"[T={tick:03}] {cat.name} {event} | {cat.location} "
                f"H={n.hunger:.1f} T={n.thirst:.1f} F={n.fatigue:.1f} "
                f"Fear={n.fear:.1f}")
        events.append(line)
        print(line)
        if debug and "starts " in event:
            print("  utilities:", ", ".join(
                f"{key}={value:.1f}" for key, value in
                sorted(cat.scores.items(), key=lambda item: -item[1])))
    return events


