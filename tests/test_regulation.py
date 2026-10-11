"""Regression tests for v0.4 behavioral regulation and experimental infrastructure."""
import unittest

from catsim.agents.cat import Cat
from catsim.behavior.regulation import Regulation
from catsim.biology.clock import SimulationClock
from catsim.biology.personality import Personality


class RegulationTests(unittest.TestCase):
    def test_cannot_eat_when_not_hungry(self):
        cat = Cat()
        cat.location = "Kitchen"
        cat.perceive()
        cat.needs.hunger = 4
        cat.needs.thirst = 3
        scores = cat.utilities()
        self.assertNotIn("eat", scores)
        self.assertNotIn("drink", scores)

    def test_eating_allowed_when_hungry(self):
        cat = Cat()
        cat.location = "Kitchen"
        cat.perceive()
        cat.needs.hunger = 80
        self.assertIn("eat", cat.utilities())

    def test_rest_and_sleep_are_gated(self):
        cat = Cat()
        cat.needs.fatigue = 0
        self.assertNotIn("rest", cat.utilities())
        self.assertNotIn("sleep", cat.utilities())

    def test_configurable_threshold(self):
        cat = Cat(regulation=Regulation(eat_start=70))
        cat.location = "Kitchen"
        cat.perceive()
        cat.needs.hunger = 60
        self.assertNotIn("eat", cat.utilities())

    def test_debug_scores_match_selection(self):
        cat = Cat(seed=11)
        activity = cat.choose()
        self.assertEqual(activity.name, max(cat.final_scores, key=cat.final_scores.get))
        for key in cat.scores:
            self.assertAlmostEqual(cat.final_scores[key],
                                   cat.scores[key] + cat.adjustments[key])

    def test_clock_and_metrics(self):
        cat = Cat()
        for _ in range(50):
            cat.step()
        self.assertEqual(cat.clock.ticks, 50)
        self.assertEqual(cat.metrics.ticks, 50)
        self.assertEqual(sum(cat.metrics.locations.values()), 50)

    def test_clock_units(self):
        clock = SimulationClock(tick_minutes=2.5)
        clock.advance()
        self.assertEqual(clock.elapsed_minutes, 2.5)

    def test_invalid_personality(self):
        with self.assertRaises(ValueError):
            Personality(boldness=1.2)

    def test_kitchen_trap_regression(self):
        cat = Cat(seed=42)
        for _ in range(200):
            cat.step()
        # The previous version spent nearly all later ticks in the kitchen.
        # The v0.4 model should not be permanently stuck there.
        self.assertGreater(cat.metrics.locations["Living Room"], 5)


class VersionSixTests(unittest.TestCase):
    def test_time_normalized_rates(self):
        from catsim.biology.needs import Needs
        a, b = Needs(), Needs()
        a.tick(minutes=60)
        for _ in range(60):
            b.tick(minutes=1)
        self.assertAlmostEqual(a.hunger, b.hunger)
        self.assertAlmostEqual(a.thirst, b.thirst)

    def test_configurable_tick_length(self):
        cat = Cat(tick_minutes=15)
        cat.step()
        self.assertEqual(cat.clock.elapsed_minutes, 15)

    def test_invalid_tick_length(self):
        with self.assertRaises(ValueError):
            Cat(tick_minutes=0)

    def test_experiment_reproducibility(self):
        from catsim.simulation.metrics import batch_experiment
        self.assertEqual(batch_experiment(range(3), 40),
                         batch_experiment(range(3), 40))

    def test_navigation_target_reaches_destination(self):
        cat = Cat()
        cat.location = "Bedroom"
        cat.perceive()
        cat.location = "Kitchen"
        cat.perceive()
        cat.navigation_target = "Bedroom"
        cat.needs.hunger = 0
        cat.needs.thirst = 0
        cat.needs.fatigue = 5
        cat.activity = None
        cat.step()
        self.assertEqual(cat.activity.name, "move:Living Room")


if __name__ == "__main__":
    unittest.main()
