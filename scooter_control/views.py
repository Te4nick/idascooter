from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# from .models import Scooter
from .serializers import (
    ScooterSerializer,
    ScooterIDSerializer,
    InPassengerSerializer,
    PassengerIDSerializer,
    ValidationErrorSerializer,
    OccupyScooterSerializer,
    PaginationSerializer,
    OperationSerializer,
    GetOperationQuerySerializer,
)
from .services import (
    LogService,
    OperationService,
    ScooterService,
    PassengerService,
)


class ScooterViewSet(ViewSet):
    scooter_service = ScooterService()
    log_service = LogService()
    ops_service = OperationService()
    passenger_service = PassengerService()

    @extend_schema(
        summary="Get new scooter",
        responses={
            status.HTTP_201_CREATED: ScooterSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_scooter(self, request):
        s = self.scooter_service.add_scooter()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ScooterSerializer(s).data
        )

    @extend_schema(
        summary="Post new passenger information",
        request=InPassengerSerializer,
        responses={
            status.HTTP_201_CREATED: PassengerIDSerializer,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_passenger(self, request):
        in_passenger = InPassengerSerializer(data=request.data)
        if not in_passenger.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": in_passenger.errors}).data,
            )

        new_passenger_id = self.passenger_service.add_passenger(**in_passenger.data)
        self.log_service.write_entry(**in_passenger.data)
        return Response(
            status=status.HTTP_201_CREATED,
            data=PassengerIDSerializer({"passenger_id": new_passenger_id}).data
        )

    @extend_schema(
        summary="Occupy scooter by user",
        request=OccupyScooterSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_occupy_scooter(self, request):
        in_occupy = OccupyScooterSerializer(data=request.data)
        if not in_occupy.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": in_occupy.errors}).data,
            )

        if self.passenger_service.get_passenger(UUID(in_occupy.data["passenger_id"])) is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        if not self.scooter_service.occupy_scooter(
            scooter_id=UUID(in_occupy.data["scooter_id"]),
            passenger_id=UUID(in_occupy.data["passenger_id"]),
        ):
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Vacant scooter by id",
        request=ScooterIDSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["POST"])
    def post_vacant_scooter(self, request):
        in_data = ScooterIDSerializer(data=request.data)
        if not in_data.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": in_data.errors}).data,
            )

        if self.scooter_service.vacant_scooter(UUID(in_data.data["scooter_id"])):
            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            status=status.HTTP_404_NOT_FOUND
        )

    @extend_schema(
        summary="Post scooter status is broken",
        request=ScooterIDSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def post_broken_scooter(self, request):
        query_ser = ScooterIDSerializer(data=request.data)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        if self.scooter_service.break_scooter(UUID(query_ser.data["scooter_id"])):
            return Response(
                status=status.HTTP_200_OK,
            )

        return Response(
            status=status.HTTP_404_NOT_FOUND,
        )

    @extend_schema(
        summary="Get scooters list",
        parameters=[PaginationSerializer],
        responses={
            status.HTTP_200_OK: ScooterSerializer(many=True),
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_scooters_list(self, request):
        query_ser = PaginationSerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )

        scooters = self.scooter_service.get_scooter_list(**query_ser.data)

        return Response(
            status=status.HTTP_200_OK,
            data=ScooterSerializer(scooters, many=True).data,
        )

    @extend_schema(
        summary="Get notification if scooter is broken",
        parameters=[ScooterIDSerializer],
        responses={
            status.HTTP_200_OK: ScooterSerializer,
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_scooter_broken(self, request):
        query_ser = ScooterIDSerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=query_ser.errors,
            )
        if (scooter := self.scooter_service.get_scooter(UUID(query_ser.data["scooter_id"]))) is not None:
            if self.scooter_service.is_scooter_broken(scooter.id):
                return Response(
                    status=status.HTTP_200_OK,
                    data=ScooterSerializer(scooter).data,
                )
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            status=status.HTTP_404_NOT_FOUND,
        )

    @extend_schema(
        summary="Generate passengers.csv and get operation details",
        responses={
            status.HTTP_200_OK: OperationSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_log_file(self, _):
        op_id = self.ops_service.execute_operation(self.log_service.get_log_file_path)
        op = self.ops_service.get_operation(op_id)
        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(op).data,
        )

    @extend_schema(
        summary="Get passengers.csv generation status",
        parameters=[GetOperationQuerySerializer],
        responses={
            status.HTTP_200_OK: OperationSerializer,
            status.HTTP_404_NOT_FOUND: None,
            status.HTTP_422_UNPROCESSABLE_ENTITY: ValidationErrorSerializer,
        },
        auth=False,
    )
    @action(detail=False, methods=["GET"])
    def get_log_file_status(self, request):
        query_ser = GetOperationQuerySerializer(data=request.query_params)
        if not query_ser.is_valid():
            return Response(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                data=ValidationErrorSerializer({"errors": query_ser.errors}).data,
            )

        op = self.ops_service.get_operation(UUID(query_ser.data.get("id")))
        if op is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            status=status.HTTP_200_OK,
            data=OperationSerializer(
                {
                    "id": op.id,
                    "done": op.done,
                    "result": {
                        "path": op.result,
                    },
                }
            ).data,
        )
