"""Shortest-path navigation on the room graph."""
from collections import deque
from catsim.world.model import Place


def next_step(places: dict[str, Place], start: str, destination: str) -> str | None:
    if start == destination:
        return None
    if start not in places or destination not in places:
        return None
    queue = deque([(start, None)])
    visited = {start}
    while queue:
        location, first = queue.popleft()
        for neighbor in places[location].neighbors:
            if neighbor in visited:
                continue
            step = first or neighbor
            if neighbor == destination:
                return step
            visited.add(neighbor)
            queue.append((neighbor, step))
    return None
