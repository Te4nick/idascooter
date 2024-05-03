from uuid import uuid4

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

    def test_get_scooter_success(self):
        scooter = Scooter()
        self.service.scooters[scooter.id] = scooter
        self.assertEqual(self.service.get_scooter(scooter.id), scooter)

    def test_get_scooter_not_found(self):
        self.assertEqual(self.service.get_scooter(uuid4()), None)

    def test_occupy_scooter_success(self):
        scooter = Scooter()
        self.service.scooters[scooter.id] = scooter
        passenger_id = uuid4()

        self.assertEqual(self.service.occupy_scooter(scooter.id, passenger_id), True)

        self.assertEqual(self.service.scooters[scooter.id].id, scooter.id)
        self.assertEqual(self.service.scooters[scooter.id].status, ScooterStatus.OCCUPIED)
        self.assertEqual(self.service.scooters[scooter.id].passenger_id, passenger_id)

    def test_occupy_scooter_not_found(self):
        self.assertEqual(self.service.occupy_scooter(uuid4(), uuid4()), False)

    def test_vacant_scooter_success(self):
        scooter = Scooter()
        scooter.status = ScooterStatus.OCCUPIED
        scooter.passenger_id = uuid4()
        self.service.scooters[scooter.id] = scooter

        self.assertEqual(self.service.vacant_scooter(scooter.id), True)

        self.assertEqual(self.service.scooters[scooter.id].id, scooter.id)
        self.assertEqual(self.service.scooters[scooter.id].status, ScooterStatus.VACANT)
        self.assertEqual(self.service.scooters[scooter.id].passenger_id, None)

    def test_vacant_scooter_not_found(self):
        self.assertEqual(self.service.vacant_scooter(uuid4()), False)

    def test_break_scooter_success(self):
        scooter = Scooter()
        self.service.scooters[scooter.id] = scooter

        self.assertEqual(self.service.break_scooter(scooter.id), True)

        self.assertEqual(self.service.scooters[scooter.id].id, scooter.id)
        self.assertEqual(self.service.scooters[scooter.id].status, ScooterStatus.BROKEN)
        self.assertEqual(self.service.scooters[scooter.id].passenger_id, scooter.passenger_id)

    def test_break_scooter_not_found(self):
        self.assertEqual(self.service.break_scooter(uuid4()), False)

    def test_get_scooter_list_success(self):
        scooters_list: list[Scooter] = []

        for i in range(10):
            scooters_list.append(Scooter())
            self.service.scooters[scooters_list[i].id] = scooters_list[i]

        self.assertListEqual(self.service.get_scooter_list(), scooters_list)

    def test_is_scooter_broken_success(self):
        scooter = Scooter()
        scooter.status = ScooterStatus.BROKEN
        self.service.scooters[scooter.id] = scooter

        self.assertEqual(self.service.is_scooter_broken(scooter.id), True)

    def test_is_scooter_broken_false(self):
        scooter = Scooter()
        self.service.scooters[scooter.id] = scooter

        self.assertEqual(self.service.is_scooter_broken(scooter.id), False)

    def test_is_scooter_broken_not_found(self):
        self.assertEqual(self.service.is_scooter_broken(uuid4()), None)
