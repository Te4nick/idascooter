from uuid import UUID, uuid4
from ..models import Passenger


class PassengerService:
    def __init__(self):
        self.passengers: dict[UUID: Passenger] = dict()

    def add_passenger(self, name: str, surname: str) -> UUID:
        """
        Register new passenger in the system
        :param name: Passenger name
        :param surname: Passenger surname
        :return: Created Passenger ID
        """
        passenger_id = uuid4()
        self.passengers[passenger_id] = Passenger(name, surname)
        return passenger_id

    def get_passenger(self, passenger_id: UUID) -> Passenger | None:
        """
        Get a passenger
        :param passenger_id: Passenger ID
        :return: Passenger object or None if no passenger is found
        """
        if passenger_id in self.passengers:
            return self.passengers[passenger_id]
        return None
