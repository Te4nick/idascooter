from django.db import models
from enum import Enum
from uuid import UUID, uuid4


class ScooterStatus(Enum):
    BROKEN = -1
    VACANT = 0
    OCCUPIED = 1


class Passenger:
    name: str
    surname: str

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'{self.name} {self.surname}'


class Scooter:
    id: UUID
    status: ScooterStatus
    passenger_id: UUID | None

    def __init__(self) -> None:
        self.id: UUID = uuid4()
        self.status: ScooterStatus = ScooterStatus.VACANT
        self.passenger_id: UUID | None = None

    def is_broken(self):
        return self.status == ScooterStatus.BROKEN


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
            self.id == other.id
            and self.done == other.done
            and self.result == other.result
        )

