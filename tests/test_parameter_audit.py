"""V1 scientific transparency checks."""
import unittest
from catsim.research.parameter_audit import inventory, audit_parameters


class ParameterAuditTests(unittest.TestCase):
    def test_inventory_includes_major_model_groups(self):
        groups = inventory()
        self.assertEqual(set(groups), {
            "metabolism", "activity_budget", "regulation",
            "sleep_pressure", "toy_habituation",
        })
        self.assertIn("hunger_per_hour", groups["metabolism"])
        self.assertIn("sleep_recovery_per_hour", groups["activity_budget"])

    def test_audit_does_not_claim_calibration(self):
        result = audit_parameters()
        self.assertFalse(result["all_numeric_coefficients_empirically_fitted"])
        self.assertGreater(result["numeric_parameters"], 10)

    def test_inventory_is_stable(self):
        self.assertEqual(inventory(), inventory())


if __name__ == "__main__":
    unittest.main()
