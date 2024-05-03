from uuid import UUID
from ..models import Scooter, ScooterStatus


class ScooterService:
    def __init__(self):
        self.scooters: dict[UUID: Scooter] = dict()

    def add_scooter(self) -> Scooter:
        s = Scooter()
        self.scooters[s.id] = s
        return s

    def get_scooter(self, scooter_id: UUID) -> Scooter | None:
        return self.scooters.get(scooter_id)

    def occupy_scooter(self, scooter_id: UUID, passenger_id: UUID) -> bool:
        if scooter_id in self.scooters:
            s: Scooter = self.scooters[scooter_id]
            s.status = ScooterStatus.OCCUPIED
            s.passenger_id = passenger_id
            return True
        return False

    def vacant_scooter(self, scooter_id: UUID) -> bool:
        if scooter_id in self.scooters:
            s: Scooter = self.scooters[scooter_id]
            s.status = ScooterStatus.VACANT
            s.passenger_id = None
            return True
        return False

    def break_scooter(self, scooter_id: UUID) -> bool:
        if scooter_id in self.scooters:
            s: Scooter = self.scooters[scooter_id]
            s.status = ScooterStatus.BROKEN
            return True
        return False

    def get_scooter_list(self, limit: int = None, offset: int = None) -> list[Scooter]:
        scooters_list: list[Scooter] = list(self.scooters.values())
        out_scooters: list[Scooter] = []
        if limit is None:
            limit = 10
        if offset is None:
            offset = 0
        try:
            for i in range(offset, offset + limit):
                out_scooters.append(scooters_list[i])
        except IndexError:
            return out_scooters
        return out_scooters

    def is_scooter_broken(self, scooter_id: UUID) -> bool | None:
        if scooter_id in self.scooters:
            s: Scooter = self.scooters[scooter_id]
            return s.status == ScooterStatus.BROKEN
        return None
