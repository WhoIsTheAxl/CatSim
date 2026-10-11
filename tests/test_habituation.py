"""v0.9: toy habituation and seeded behavior regression."""
import unittest
from catsim.agents.cat import Cat
from catsim.behavior.habituation import PlayHabituation


class HabituationTests(unittest.TestCase):
    def test_play_reduces_interest(self):
        state = PlayHabituation()
        initial = state.play_multiplier
        state.advance("play", 60)
        self.assertLess(state.play_multiplier, initial)

    def test_time_step_invariance(self):
        a, b = PlayHabituation(), PlayHabituation()
        a.advance("play", 60)
        for _ in range(60):
            b.advance("play", 1)
        self.assertAlmostEqual(a.familiarity, b.familiarity)

    def test_interest_recovers_when_not_playing(self):
        state = PlayHabituation()
        state.advance("play", 60)
        reduced = state.play_multiplier
        state.advance("rest", 60)
        self.assertGreater(state.play_multiplier, reduced)

    def test_novel_toy_restores_interest(self):
        state = PlayHabituation()
        state.advance("play", 60)
        state.novel_toy()
        self.assertEqual(state.play_multiplier, 1)

    def test_repeated_play_lowers_utility(self):
        cat = Cat()
        before = cat.utilities()["play"]
        cat.play_habituation.advance("play", 60)
        self.assertLess(cat.utilities()["play"], before)

    def test_determinism_and_metrics(self):
        def run():
            cat = Cat(seed=42)
            events = [cat.step() for _ in range(150)]
            return events, cat.metrics.report()
        self.assertEqual(run(), run())
        self.assertEqual(sum(run()[1]["activity_ticks"].values()), 150)


if __name__ == "__main__":
    unittest.main()
