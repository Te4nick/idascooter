import time
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from scooter_control.models import ScooterStatus
from scooter_control.views import ScooterViewSet


class ScooterControlSystemTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def get_valid_scooter(self):
        request = self.factory.get(
            '/api/v1/scooter/',
        )
        return ScooterViewSet.as_view({'get': 'get_scooter'})(request)

    def post_valid_passenger(self):
        request = self.factory.post(
            '/api/v1/passenger/',
            {
                'name': 'Dmitriy',
                'surname': 'Nagiev',
            },
        )
        return ScooterViewSet.as_view({'post': 'post_passenger'})(request)

    def test_get_scooter_valid(self):
        response = self.get_valid_scooter()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ScooterStatus.VACANT.name)
        self.assertEqual(response.data['passenger_id'], None)

    def test_post_passenger_valid(self):
        response = self.post_valid_passenger()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_passenger_validation_error(self):
        request = self.factory.post(
            '/api/v1/passenger/',
            {
                'i am': 'error',
            },
        )
        response = ScooterViewSet.as_view({'post': 'post_passenger'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_occupy_scooter_valid(self):
        passenger_id = self.post_valid_passenger().data['passenger_id']
        scooter_data = self.get_valid_scooter().data

        request = self.factory.post(
            f'/api/v1/scooter/occupy',
            {
                'scooter_id': scooter_data['id'],
                'passenger_id': passenger_id,
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_occupy_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_occupy_scooter_not_found(self):
        request = self.factory.post(
            f'/api/v1/scooter/occupy',
            {
                'scooter_id': uuid4(),
                'passenger_id': uuid4(),
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_occupy_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_occupy_scooter_validation_error(self):
        request = self.factory.post(
            '/api/v1/scooter/occupy',
            {
                'i am': 'error',
            },
        )
        response = ScooterViewSet.as_view({'post': 'post_occupy_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_vacant_scooter_valid(self):
        scooter_data = self.get_valid_scooter().data

        request = self.factory.post(
            f'/api/v1/scooter/vacant',
            {
                'scooter_id': scooter_data['id'],
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_vacant_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_vacant_scooter_not_found(self):
        request = self.factory.post(
            f'/api/v1/scooter/vacant',
            {
                'scooter_id': uuid4(),
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_vacant_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_vacant_scooter_validation_error(self):
        request = self.factory.post(
            '/api/v1/scooter/vacant',
            {
                'i am': 'error',
            },
        )
        response = ScooterViewSet.as_view({'post': 'post_vacant_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_broken_scooter_valid(self):
        scooter_data = self.get_valid_scooter().data

        request = self.factory.post(
            f'/api/v1/scooter/broken',
            {
                'scooter_id': scooter_data['id'],
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_broken_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_broken_scooter_not_found(self):
        request = self.factory.post(
            f'/api/v1/scooter/broken',
            {
                'scooter_id': uuid4(),
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_broken_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_broken_scooter_validation_error(self):
        request = self.factory.post(
            '/api/v1/scooter/broken',
            {
                'i am': 'error',
            },
        )
        response = ScooterViewSet.as_view({'post': 'post_broken_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_scooters_list_valid(self):
        request = self.factory.get(
            '/api/v1/scooter/all',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooters_list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_scooters_list_validation_error(self):
        request = self.factory.get(
            '/api/v1/scooter/all?limit=unlimited',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooters_list'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_scooter_broken_valid(self):
        scooter_data = self.get_valid_scooter().data
        desired_data = {
            'id': scooter_data['id'],
            'status': ScooterStatus.BROKEN.name,
            'passenger_id': scooter_data['passenger_id'],
        }

        request = self.factory.post(
            f'/api/v1/scooter/broken',
            {
                'scooter_id': scooter_data['id'],
            }
        )
        response = ScooterViewSet.as_view({'post': 'post_broken_scooter'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = self.factory.get(
            f'/api/v1/scooter/broken?scooter_id={scooter_data['id']}',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooter_broken'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, desired_data)

    def test_get_scooter_broken_no_content(self):
        scooter_data = self.get_valid_scooter().data

        request = self.factory.get(
            f'/api/v1/scooter/broken?scooter_id={scooter_data['id']}',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooter_broken'})(request)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_get_scooter_broken_not_found(self):
        request = self.factory.get(
            f'/api/v1/scooter/broken?scooter_id={uuid4()}',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooter_broken'})(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, None)

    def test_get_scooter_broken_validation_error(self):
        request = self.factory.get(
            f'/api/v1/scooter/broken?scooter_id=i_am_error',
        )
        response = ScooterViewSet.as_view({'get': 'get_scooter_broken'})(request)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_log_file_success(self):
        request = self.factory.get("/api/v1/log")
        response = ScooterViewSet.as_view({"get": "get_log_file"})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["done"], False)
        self.assertEqual(response.data["result"], None)

    def test_get_log_file_status_success(self):
        desired_response_data = {
            "id": None,
            "done": True,
            "result": {
                "path": "static/log/passengers.csv"
            },
        }

        request = self.factory.get("/api/v1/log")
        response = ScooterViewSet.as_view({"get": "get_log_file"})(request)
        desired_response_data["id"] = response.data['id']

        time.sleep(1)

        request = self.factory.get(f"/api/v1/log/status?id={response.data['id']}")
        response = ScooterViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, desired_response_data)

    def test_get_log_file_status_validation_error(self):
        desired_response_data = {
            "errors": {
                "id": [
                    "This field is required."
                ]
            }
        }

        request = self.factory.get("/api/v1/log/status?cannot=validate")
        response = ScooterViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, desired_response_data)

    def test_get_log_file_status_not_found(self):
        op_id = uuid4()

        request = self.factory.get(f"/api/v1/log/status?id={op_id}")
        response = ScooterViewSet.as_view({"get": "get_log_file_status"})(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
