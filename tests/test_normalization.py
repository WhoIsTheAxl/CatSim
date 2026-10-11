"""v0.7 invariants: time normalization and stable behavior."""
import unittest
from catsim.agents.cat import Cat
from catsim.biology.activity_budget import ActivityBudget, apply_activity
from catsim.biology.needs import Needs


class NormalizationTests(unittest.TestCase):
    def test_rest_effect_scales_with_elapsed_minutes(self):
        a, b = Needs(), Needs()
        budget = ActivityBudget()
        apply_activity(a, "rest", 20, budget)
        for _ in range(20):
            apply_activity(b, "rest", 1, budget)
        self.assertAlmostEqual(a.fatigue, b.fatigue)

    def test_play_fatigue_scales_with_elapsed_minutes(self):
        a, b = Needs(), Needs()
        budget = ActivityBudget()
        apply_activity(a, "play", 12, budget)
        for _ in range(12):
            apply_activity(b, "play", 1, budget)
        self.assertAlmostEqual(a.fatigue, b.fatigue)

    def test_idle_always_available(self):
        cat = Cat()
        cat.cooldowns["idle"] = 100
        self.assertIn("idle", cat.utilities())

    def test_stable_low_need_state_does_not_force_travel(self):
        cat = Cat()
        cat.location = "Bedroom"
        cat.perceive()
        cat.needs.curiosity = 0
        cat.needs.fatigue = 0
        cat.needs.hunger = 0
        cat.needs.thirst = 0
        cat.needs.play_urge = 0
        cat.needs.grooming_urge = 0
        cat.needs.fear = 0
        self.assertEqual(cat.choose().name, "idle")

    def test_duration_is_time_normalized(self):
        a, b = Cat(tick_minutes=1), Cat(tick_minutes=5)
        a.needs.fatigue = 90
        b.needs.fatigue = 90
        a.location = b.location = "Bedroom"
        a.perceive()
        b.perceive()
        x, y = a.choose(), b.choose()
        self.assertEqual(x.name, "sleep")
        self.assertEqual(y.name, "sleep")
        self.assertEqual(x.remaining, y.remaining * 5)

    def test_no_instant_rest_recovery(self):
        cat = Cat()
        cat.needs.fatigue = 25
        cat.activity = None
        before = cat.needs.fatigue
        cat.step()
        self.assertLess(abs(cat.needs.fatigue - before), 2)

    def test_reproducible_200_steps(self):
        def run():
            cat = Cat(seed=17)
            return [cat.step() for _ in range(200)]
        self.assertEqual(run(), run())


if __name__ == "__main__":
    unittest.main()
