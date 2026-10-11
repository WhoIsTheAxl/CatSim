"""Research-driven environment changes: resource perception and provenance."""
import unittest
from catsim.agents.cat import Cat
from catsim.world.environment import Environment
from catsim.world.objects import WorldObject


class EnvironmentalResearchTests(unittest.TestCase):
    def test_separate_water_option(self):
        world = Environment()
        self.assertEqual(world.objects["water_station"].location, "Bedroom")
        self.assertEqual(world.objects["bowl_food"].location, "Kitchen")

    def test_scratching_requires_local_resource(self):
        cat = Cat()
        self.assertIn("scratch", cat.utilities())
        cat.location = "Kitchen"
        cat.perceive()
        self.assertNotIn("scratch", cat.utilities())

    def test_scratching_disappears_when_post_removed(self):
        cat = Cat()
        del cat.world.objects["scratching_post"]
        cat.perceive()
        self.assertNotIn("scratch", cat.utilities())

    def test_scratching_can_be_selected_without_hidden_knowledge(self):
        cat = Cat()
        cat.needs.hunger = 0
        cat.needs.thirst = 0
        cat.needs.play_urge = 0
        cat.needs.grooming_urge = 100
        self.assertIn("scratch", cat.utilities())

    def test_existing_kitchen_water_retained(self):
        world = Environment()
        self.assertEqual(world.objects["bowl_water"].location, "Kitchen")


if __name__ == "__main__":
    unittest.main()
