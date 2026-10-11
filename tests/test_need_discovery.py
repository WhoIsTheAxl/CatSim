"""v0.8 regression coverage for needs, exploration and activity accounting."""
import unittest
from catsim.agents.cat import Cat
from catsim.behavior.activity import Activity


class NeedDiscoveryTests(unittest.TestCase):
    def test_unknown_food_is_not_omniscient(self):
        cat = Cat()
        self.assertFalse(any("food" in kinds for kinds in cat.memory.resources.values()))
        self.assertNotIn("eat", cat.utilities())

    def test_hunger_motivates_search_without_food_memory(self):
        cat = Cat()
        cat.needs.hunger = 85
        cat.needs.play_urge = 0
        moves = {key: score for key, score in cat.utilities().items()
                 if key.startswith("move:")}
        self.assertTrue(moves)
        self.assertGreater(max(moves.values()), cat.utilities()["idle"])

    def test_known_food_motivates_navigation(self):
        cat = Cat()
        cat.location = "Kitchen"
        cat.perceive()
        cat.location = "Living Room"
        cat.perceive()
        cat.needs.hunger = 85
        self.assertGreater(cat.utilities()["move:Kitchen"], 100)

    def test_no_search_when_needs_satisfied(self):
        cat = Cat()
        cat.needs.hunger = 0
        cat.needs.thirst = 0
        cat.needs.curiosity = 0
        cat.needs.fatigue = 0
        cat.needs.fear = 0
        self.assertFalse(any(key.startswith("move:") for key in cat.utilities()))

    def test_urgent_hunger_interrupts_play(self):
        cat = Cat()
        cat.needs.hunger = 90
        cat.activity = Activity("play", 9)
        event = cat.step()
        self.assertIn("interrupts activity", event)
        self.assertIn("starts move:", event)

    def test_metrics_count_interrupted_activity(self):
        cat = Cat()
        cat.needs.hunger = 90
        cat.activity = Activity("play", 9)
        cat.step()
        self.assertEqual(sum(cat.metrics.activity_ticks.values()), 1)
        self.assertEqual(sum(cat.metrics.actions.values()), 1)

    def test_debug_action_matches_final_scores(self):
        cat = Cat()
        cat.navigation_target = "Bedroom"
        action = cat.choose()
        self.assertEqual(action.name, max(cat.final_scores, key=cat.final_scores.get))

    def test_multi_seed_determinism(self):
        from catsim.simulation.metrics import batch_experiment
        a = batch_experiment(range(4), 120)
        b = batch_experiment(range(4), 120)
        self.assertEqual(a, b)
        self.assertEqual(sum(a["activity_ticks"].values()), 4 * 120)


if __name__ == "__main__":
    unittest.main()
