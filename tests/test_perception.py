import unittest

from catsim.agents.cat import Cat
from catsim.behavior.navigation import next_step
from catsim.perception.sensory_system import SensorySystem
from catsim.world.environment import Environment
from catsim.world.events import Event, apply_event
from catsim.world.objects import WorldObject


class PerceptionTests(unittest.TestCase):
    def test_only_local_visible_objects_are_perceived(self):
        world = Environment()
        world.add_object(WorldObject("hidden", "toy", "Living Room", visible=False))
        observed = SensorySystem().observe("Living Room", world)
        self.assertEqual({o.object_id for o in observed}, {"mouse_toy", "scratching_post"})
        self.assertNotIn("hidden", {o.object_id for o in observed})

    def test_resource_is_learned_after_arrival(self):
        cat = Cat()
        self.assertNotIn("Kitchen", cat.memory.resources)
        cat.location = "Kitchen"
        cat.perceive()
        self.assertEqual(cat.memory.resources["Kitchen"], {"food", "water"})
        self.assertEqual(cat.memory.object_locations["bowl_food"], "Kitchen")

    def test_moved_resource_updates_on_reobservation(self):
        world = Environment()
        cat = Cat(world=world)
        cat.location = "Kitchen"
        cat.perceive()
        world.move_object("bowl_food", "Bedroom")
        cat.perceive()
        self.assertNotIn("bowl_food", cat.memory.object_locations)
        self.assertEqual(cat.memory.resources["Kitchen"], {"water"})
        cat.location = "Bedroom"
        cat.perceive()
        self.assertEqual(cat.memory.object_locations["bowl_food"], "Bedroom")

    def test_unknown_resource_not_used_in_decision(self):
        cat = Cat()
        self.assertNotIn("Kitchen", cat.memory.resources)
        cat.needs.hunger = 95
        scores = cat.utilities()
        self.assertNotIn("eat", scores)

    def test_shortest_path(self):
        world = Environment()
        self.assertEqual(next_step(world.places, "Kitchen", "Bedroom"), "Living Room")
        self.assertIsNone(next_step(world.places, "Bedroom", "Bedroom"))

    def test_event_is_perceived_only_in_room(self):
        world = Environment()
        apply_event(world, Event("sound", "Kitchen", 80, "noise"))
        cat = Cat(world=world)
        self.assertFalse(any(o.object_id == "noise" for o in cat.observations))
        cat.location = "Kitchen"
        cat.perceive()
        self.assertTrue(any(o.object_id == "noise" for o in cat.observations))

    def test_reproducible_simulation(self):
        def sample():
            cat = Cat(seed=123)
            return [cat.step() for _ in range(200)]
        self.assertEqual(sample(), sample())


if __name__ == "__main__":
    unittest.main()
