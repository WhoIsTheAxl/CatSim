"""v0.9: new actions, sleep pressure and observation-based eligibility."""
import unittest
from catsim.agents.cat import Cat
from catsim.biology.sleep_pressure import SleepPressure
from catsim.biology.activity_budget import ActivityBudget, apply_activity
from catsim.biology.needs import Needs


class V09ActionsTests(unittest.TestCase):
    def test_new_actions_available(self):
        cat = Cat()
        scores = cat.utilities()
        self.assertIn("stretch", scores)
        self.assertIn("observe", scores)
        self.assertIn("bat_toy", scores)

    def test_toy_action_requires_perception(self):
        cat = Cat()
        cat.location = "Kitchen"
        cat.perceive()
        self.assertNotIn("bat_toy", cat.utilities())

    def test_batting_reduces_play_urge(self):
        needs = Needs()
        initial = needs.play_urge
        apply_activity(needs, "bat_toy", 5, ActivityBudget())
        self.assertLess(needs.play_urge, initial)

    def test_sleep_pressure_grows_and_recovers(self):
        state = SleepPressure()
        initial = state.value
        state.advance("observe", 60)
        self.assertGreater(state.value, initial)
        state.advance("sleep", 60)
        self.assertLess(state.value, initial)

    def test_sleep_pressure_affects_sleep_utility(self):
        cat = Cat()
        cat.needs.fatigue = 80
        before = cat.utilities()["sleep"]
        cat.sleep_pressure.advance("observe", 60)
        self.assertGreater(cat.utilities()["sleep"], before)

    def test_150_tick_activity_accounting(self):
        cat = Cat(seed=42)
        for _ in range(150):
            cat.step()
        self.assertEqual(sum(cat.metrics.activity_ticks.values()), 150)

    def test_seeded_reproducibility(self):
        def run():
            cat = Cat(seed=14)
            return [cat.step() for _ in range(150)]
        self.assertEqual(run(), run())


if __name__ == "__main__":
    unittest.main()
