from uuid import uuid4

from django.test import TestCase

from scooter_control.models import Passenger
from scooter_control.services import PassengerService


class PassengerServiceTest(TestCase):
    def setUp(self) -> None:
        self.service = PassengerService()

    def test_add_passenger(self):
        passenger = Passenger(name='Water', surname='Rock')
        added_passenger_id = self.service.add_passenger(passenger.name, passenger.surname)
        self.assertEqual(self.service.passengers[added_passenger_id].name, passenger.name)
        self.assertEqual(self.service.passengers[added_passenger_id].surname, passenger.surname)

    def test_get_passenger_success(self):
        passenger = Passenger(name='Water', surname='Rock')
        passenger_id = uuid4()
        self.service.passengers[passenger_id] = passenger
        self.assertEqual(passenger, self.service.get_passenger(passenger_id))


