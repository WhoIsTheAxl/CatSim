"""Rest-site preference based on perceived shelter and learned familiarity."""
from catsim.behavior.navigation import next_step


def site_comfort(cat, location: str) -> float:
    """Estimate comfort from memory only; no hidden world-resource access."""
    resources = cat.memory.resources.get(location, set())
    shelter = 24.0 if "shelter" in resources else 0.0
    familiarity = cat.memory.familiarity.get(location, 0) * 0.08
    return shelter + familiarity


def preferred_rest_site(cat) -> str | None:
    """Return best known shelter with a navigable route, if any."""
    candidates = [
        location for location, kinds in cat.memory.resources.items()
        if "shelter" in kinds and
        (location == cat.location or
         next_step(cat.world.places, cat.location, location) is not None)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda location: (site_comfort(cat, location), location))
