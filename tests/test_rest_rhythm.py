"""v0.5 tests: clock-driven activity, shelter preference and disturbance response."""
import unittest

from catsim.agents.cat import Cat
from catsim.biology.rhythm import activity_drive
from catsim.behavior.resting import preferred_rest_site
from catsim.world.events import Event, apply_event


class RestRhythmTests(unittest.TestCase):
    def test_dawn_more_active_than_midday(self):
        self.assertGreater(activity_drive(6), activity_drive(12))

    def test_rhythm_repeats_daily(self):
        self.assertAlmostEqual(activity_drive(6), activity_drive(30))

    def test_sleep_utility_changes_with_time(self):
        cat = Cat()
        cat.needs.fatigue = 80
        cat.clock.ticks = 6 * 60
        dawn = cat.utilities()["sleep"]
        cat.clock.ticks = 12 * 60
        midday = cat.utilities()["sleep"]
        self.assertGreater(midday, dawn)

    def test_prefers_known_shelter(self):
        cat = Cat()
        self.assertIsNone(preferred_rest_site(cat))
        cat.location = "Bedroom"
        cat.perceive()
        cat.location = "Living Room"
        cat.perceive()
        self.assertEqual(preferred_rest_site(cat), "Bedroom")

    def test_sound_causes_single_fear_response(self):
        cat = Cat()
        apply_event(cat.world, Event("sound", "Living Room", 80, "door"))
        cat.perceive()
        fear = cat.needs.fear
        cat.perceive()
        self.assertEqual(cat.needs.fear, fear)

    def test_sound_interrupts_sleep(self):
        cat = Cat()
        cat.needs.fatigue = 80
        cat.activity = cat.choose()
        from catsim.behavior.activity import Activity
        cat.activity = Activity("sleep", 4)
        apply_event(cat.world, Event("sound", "Living Room", 90, "bang"))
        event = cat.step()
        self.assertIn("interrupts rest", event)

    def test_reproducible_with_rhythm(self):
        def run():
            cat = Cat(seed=19)
            return [cat.step() for _ in range(250)]
        self.assertEqual(run(), run())


if __name__ == "__main__":
    unittest.main()
