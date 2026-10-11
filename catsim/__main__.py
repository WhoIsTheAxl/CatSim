"""CatSim command line entry point and backwards-compatible exports."""
import argparse
from catsim.agents.cat import Cat
from catsim.world.model import WORLD
from catsim.core.math import clamp
from catsim.simulation.runner import run

def main() -> None:
    parser = argparse.ArgumentParser(description="CatSim experimental behavioral simulator")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.steps < 0:
        parser.error("--steps must be nonnegative")
    run(args.steps, args.seed, args.debug)


if __name__ == "__main__":
    main()
