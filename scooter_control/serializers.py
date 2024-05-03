from rest_framework import serializers
from rest_enumfield import EnumField

from .models import ScooterStatus


class ScooterSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    status = EnumField(choices=ScooterStatus, required=True)
    passenger_id = serializers.UUIDField(required=True)


class InPassengerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)


class PassengerIDSerializer(serializers.Serializer):
    passenger_id = serializers.UUIDField(required=True)


class ScooterIDSerializer(serializers.Serializer):
    scooter_id = serializers.UUIDField(required=True)


class OccupyScooterSerializer(serializers.Serializer):
    scooter_id = serializers.UUIDField(required=True)
    passenger_id = serializers.UUIDField(required=True)


class ScooterStatusSerializer(serializers.Serializer):
    status = EnumField(choices=ScooterStatus, required=True)


class ValidationErrorSerializer(serializers.Serializer):
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )


class PaginationSerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=1, default=10, max_value=50)
    offset = serializers.IntegerField(min_value=0, default=0)


class OperationSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, min_length=36, max_length=36)
    done = serializers.BooleanField()
    result = serializers.DictField()


class GetOperationQuerySerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
