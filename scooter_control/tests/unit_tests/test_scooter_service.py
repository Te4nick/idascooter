from django.test import TestCase

from scooter_control.models import Scooter, ScooterStatus
from scooter_control.services import ScooterService


class ScooterServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = ScooterService()

    def test_add_scooter(self):
        added_scooter = self.service.add_scooter()

        self.assertEqual(self.service.scooters[added_scooter.id].id, added_scooter.id)
        self.assertEqual(self.service.scooters[added_scooter.id].status, ScooterStatus.VACANT)
        self.assertEqual(self.service.scooters[added_scooter.id].passenger_id, None)

