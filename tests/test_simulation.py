import unittest
from catsim.__main__ import Cat, WORLD, clamp


class CatSimTests(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(-5), 0)
        self.assertEqual(clamp(120), 100)

    def test_deterministic(self):
        def events():
            cat = Cat(seed=123)
            return [cat.step() for _ in range(120)]
        self.assertEqual(events(), events())

    def test_discovers_resources_on_arrival(self):
        cat = Cat()
        self.assertNotIn("Kitchen", cat.memory.resources)
        cat.location = "Kitchen"
        cat.memory.observe(WORLD["Kitchen"])
        self.assertEqual(cat.memory.resources["Kitchen"], {"food", "water"})

    def test_needs_bounded(self):
        cat = Cat(seed=7)
        for _ in range(1000):
            cat.step()
            for value in vars(cat.needs).values():
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 100)

    def test_no_endless_grooming(self):
        cat = Cat(seed=42)
        actions = [cat.step() for _ in range(150)]
        self.assertLess(sum("starts groom" in e for e in actions), 30)


if __name__ == "__main__":
    unittest.main()
