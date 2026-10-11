"""v1 research infrastructure invariants; not biological validity tests."""
import unittest
from catsim.research.registry import REGISTRY, audit
from catsim.research.validation import (
    activity_proportions, total_variation, simulate_cohort, compare_cohort,
)


class ScientificValidationTests(unittest.TestCase):
    def test_provenance_is_auditable(self):
        result = audit()
        self.assertGreaterEqual(result["entries"], 4)
        self.assertFalse(result["numerical_parameters_validated"])
        self.assertEqual(result["without_limitations"], [])
        self.assertIn("toy_habituation", REGISTRY)

    def test_activity_proportions_normalize_movement(self):
        result = activity_proportions(
            {"move:Kitchen": 2, "move:Bedroom": 3, "sleep": 5})
        self.assertEqual(result, {"move": 0.5, "sleep": 0.5})

    def test_zero_counts(self):
        self.assertEqual(activity_proportions({}), {})

    def test_distance_identical(self):
        self.assertEqual(total_variation({"sleep": 0.6, "play": 0.4},
                                         {"sleep": 0.6, "play": 0.4}), 0)

    def test_distance_disjoint(self):
        self.assertEqual(total_variation({"sleep": 1.0},
                                         {"play": 1.0}), 1)

    def test_invalid_distribution_rejected(self):
        with self.assertRaises(ValueError):
            total_variation({"sleep": 0.7}, {"sleep": 1.0})
        with self.assertRaises(ValueError):
            activity_proportions({"sleep": -1})

    def test_cohort_is_deterministic(self):
        first = simulate_cohort(seeds=[1, 2], steps=150)
        self.assertEqual(first, simulate_cohort(seeds=[1, 2], steps=150))
        self.assertEqual(first["runs"], 2)
        self.assertFalse(first["scientifically_validated"])
        self.assertAlmostEqual(
            sum(row["mean"] for row in first["behaviors"].values()), 1)

    def test_reference_comparison_not_validation_claim(self):
        cohort = simulate_cohort(seeds=[42], steps=150)
        result = compare_cohort(cohort, {"sleep": 1.0})
        self.assertGreaterEqual(result["total_variation"], 0)
        self.assertLessEqual(result["total_variation"], 1)
        self.assertFalse(result["scientifically_validated"])


if __name__ == "__main__":
    unittest.main()
