from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from poultry.views import *


class FlockSourceViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, and deleting flock sources.

        """

        self.factory = APIRequestFactory()
        self.viewset = FlockSourceViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        })
        self.url = reverse('poultry:flock-sources-list')
        self.valid_data = {'source': FlockSourceChoices.This_Farm}
        self.invalid_data = {'source': 'Invalid Source'}

    def test_create_flock_source(self):
        """
        Test the create operation for a flock source.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a flock source is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlockSource.objects.count(), 1)
        self.assertEqual(FlockSource.objects.get().source, FlockSourceChoices.This_Farm)

    def test_list_flock_sources(self):
        """
        Test the list operation for flock sources.

        - Create two flock sources.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flock sources.

        """

        FlockSource.objects.create(source=FlockSourceChoices.Uzima_Chicken)
        FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm)

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = FlockSource.objects.all()
        serializer = FlockSourceSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(FlockSource.objects.count(), 2)

    def test_create_invalid_flock_source(self):
        """
        Test the create operation with invalid data for a flock source.

        - Create a POST request with invalid data.
        - Execute the create view with the request.
        - Check that the response status code is 400 (Bad Request).
        - Check that no flock source is created.

        """

        request = self.factory.post(self.url, self.invalid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FlockSource.objects.count(), 0)

    def test_delete_flock_source(self):
        """
        Test the delete operation for a flock source.

        - Create a flock source.
        - Create a DELETE request for the specific flock source URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock source is deleted.

        """

        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        delete_url = reverse('poultry:flock-sources-detail', args=[flock_source.pk])

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=flock_source.pk)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(FlockSource.objects.count(), 0)


class HousingStructureViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, retrieving, updating, and deleting housing structures.

        """

        self.factory: APIRequestFactory = APIRequestFactory()
        self.viewset = HousingStructureViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update'
        })
        self.retrieve_viewset: HousingStructureViewSet = HousingStructureViewSet.as_view({'get': 'retrieve'})
        self.url: str = reverse('poultry:housing-structures-list')
        self.valid_data: dict = {
            'type': HousingStructureTypeChoices.Deep_Litter_House,
            'category': HousingStructureCategoryChoices.Growers_House
        }

    def test_create_housing_structure(self):
        """
        Test the create operation for a housing structure.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a housing structure is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HousingStructure.objects.count(), 1)
        self.assertEqual(HousingStructure.objects.get().type, HousingStructureTypeChoices.Deep_Litter_House)
        self.assertEqual(HousingStructure.objects.get().category, HousingStructureCategoryChoices.Growers_House)

    def test_list_housing_structures(self):
        """
        Test the list operation for housing structures.

        - Create two housing structures.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized housing structures.

        """

        HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Battery_Cage,
            category=HousingStructureCategoryChoices.Broilers_House
        )

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = HousingStructure.objects.all()
        serializer = HousingStructureSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(HousingStructure.objects.count(), 2)

    def test_retrieve_housing_structure(self):
        """
        Test the retrieve operation for a housing structure.

        - Create a housing structure.
        - Create a GET request for the specific housing structure URL.
        - Execute the retrieve view with the request.
        - Compare the response data with the serialized housing structure.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        retrieve_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})

        request = self.factory.get(retrieve_url)
        response = self.retrieve_viewset(request, pk=housing_structure.pk)

        serializer = HousingStructureSerializer(housing_structure)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_housing_structure(self):
        """
        Test the update operation for a housing structure.

        - Create a housing structure.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the housing structure is updated with the new data.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        update_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})
        updated_data = {
            'type': HousingStructureTypeChoices.Battery_Cage,
            'category': HousingStructureCategoryChoices.Broilers_House
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=housing_structure.pk)

        housing_structure.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(housing_structure.type, HousingStructureTypeChoices.Battery_Cage)
        self.assertEqual(housing_structure.category, HousingStructureCategoryChoices.Broilers_House)

    def test_delete_housing_structure(self):
        """
        Test the delete operation for a housing structure.

        - Create a housing structure.
        - Create a DELETE request for the specific housing structure URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the housing structure is deleted.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        delete_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=housing_structure.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HousingStructure.objects.count(), 0)


class FlockViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, retrieving, updating, and deleting flocks.

        """

        self.factory: APIRequestFactory = APIRequestFactory()
        self.viewset = FlockViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update'
        })
        self.retrieve_viewset = FlockViewSet.as_view({'get': 'retrieve'})
        self.url: str = reverse('poultry:flocks-list')
        self.valid_data: dict = {
            'source': FlockSource.objects.create(source=FlockSourceChoices.Uzima_Chicken).pk,
            'date_of_hatching': date.today() - timezone.timedelta(weeks=4),
            'chicken_type': ChickenTypeChoices.Broiler,
            'initial_number_of_birds': 100,
            'current_rearing_method': RearingMethodChoices.Deep_Litter,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Deep_Litter_House,
                category=HousingStructureCategoryChoices.Broilers_House
            ).pk,
        }

    def test_create_flock(self):
        """
        Test the create operation for a flock.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a flock is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flock.objects.count(), 1)
        self.assertEqual(Flock.objects.get().chicken_type, ChickenTypeChoices.Broiler)

    def test_list_flocks(self):
        """
        Test the list operation for flocks.

        - Create a flock.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flocks.

        """

        Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.This_Farm),
            date_of_hatching=date.today() - timezone.timedelta(weeks=8),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=200,
            current_rearing_method=RearingMethodChoices.Barn_System,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Closed_Shed,
                category=HousingStructureCategoryChoices.Brooder_Chick_House
            ),
        )

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = Flock.objects.all()
        serializer = FlockSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Flock.objects.count(), 1)

    def test_retrieve_flock(self):
        """
        Test the retrieve operation for a flock.

        - Create a flock.
        - Create a GET request for the specific flock URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flock.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kuku_Chick),
            date_of_hatching=date.today() - timezone.timedelta(weeks=10),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=250,
            current_rearing_method=RearingMethodChoices.Barn_System,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Pasture_Housing,
                category=HousingStructureCategoryChoices.Growers_House
            ),
            date_established=date.today() - timezone.timedelta(weeks=10)
        )
        retrieve_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})

        request = self.factory.get(retrieve_url)
        response = self.retrieve_viewset(request, pk=flock.pk)

        serializer = FlockSerializer(flock)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_flock(self):
        """
        Test the update operation for a flock.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the flock is updated with the new data.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.Multi_Purpose,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.Free_Range,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Closed_Shed,
                category=HousingStructureCategoryChoices.Growers_House
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Open_Sided_Shed,
                category=HousingStructureCategoryChoices.Layers_House
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        flock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.Multi_Purpose)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.Layers_House)

    def test_delete_flock(self):
        """
        Test the delete operation for a flock.

        - Create a flock.
        - Create a DELETE request for the specific flock URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock is deleted.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Uzima_Chicken),
            date_of_hatching=date.today() - timezone.timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=120,
            current_rearing_method=RearingMethodChoices.Deep_Litter,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Pasture_Housing,
                category=HousingStructureCategoryChoices.Broilers_House
            ),
        )
        delete_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=flock.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flock.objects.count(), 0)

    def test_update_chicken_type_same_value(self):
        """
        Test updating the chicken type with the same value.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the flock is updated with the new data.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.Multi_Purpose,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.Free_Range,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Closed_Shed,
                category=HousingStructureCategoryChoices.Growers_House
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'chicken_type': ChickenTypeChoices.Multi_Purpose,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Open_Sided_Shed,
                category=HousingStructureCategoryChoices.Layers_House
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        flock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.Multi_Purpose)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.Layers_House)

    def test_update_chicken_type_different_value(self):
        """
        Test updating the chicken type with a different value.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 400 (Bad Request).

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.Multi_Purpose,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.Free_Range,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Closed_Shed,
                category=HousingStructureCategoryChoices.Growers_House
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'chicken_type': ChickenTypeChoices.Broiler,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Open_Sided_Shed,
                category=HousingStructureCategoryChoices.Layers_House
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.Multi_Purpose)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.Growers_House)


class FlockHistoryViewSetTestCase(APITestCase):
    """
    Test case for the FlockHistoryViewSet.

    This test case validates the behavior of the FlockHistoryViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary components for the test case.

        It creates a flock, flock history, and defines the URLs for the endpoints.

        """
        self.factory = APIRequestFactory()
        self.view_retrieve = FlockHistoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = FlockHistoryViewSet.as_view({'get': 'list'})

        self.flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.Multi_Purpose,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.Free_Range,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.Closed_Shed,
                category=HousingStructureCategoryChoices.Growers_House
            )
        )

        self.flock_history = FlockHistory.objects.filter(flock=self.flock).first()

        self.url_retrieve = reverse('poultry:flock-histories-detail', kwargs={'pk': self.flock.pk})
        self.url_list = reverse('poultry:flock-histories-list')

    def test_get_flock_history_detail(self):
        """
        Test the 'retrieve' endpoint of the FlockHistoryViewSet.

        It sends a GET request to the endpoint to retrieve the flock history detail and verifies the response.

        """
        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.flock_history.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FlockHistorySerializer(self.flock_history)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_pen_inventory_list(self):
        """
        Test the 'list' endpoint of the FlockHistoryViewSet.

        It sends a GET request to the endpoint to retrieve the pen inventory list and verifies the response.

        """
        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FlockHistorySerializer(FlockHistory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class FlockMovementViewSetTestCase(APITestCase):
    """
    Test case for the FlockMovementViewSet.

    This test case validates the behavior of the FlockMovementViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a flock, housing structures, and a flock movement.

        """
        self.factory = APIRequestFactory()
        self.view = FlockMovementViewSet.as_view(
            {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.url = reverse('poultry:flock-movements-list')

        # Create a flock for testing
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.to_structure_2 = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=self.from_structure,
        )

    def test_flock_movement_list(self):
        """
        Test the 'list' endpoint of the FlockMovementViewSet.

        It sends a GET request to the endpoint and verifies the response.

        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_flock_movement_create(self):
        """
        Test the 'create' endpoint of the FlockMovementViewSet.

        It sends a POST request to the endpoint with the necessary data and verifies the response.

        """
        data = {
            'flock': self.flock.id,
            'from_structure': self.flock.current_housing_structure.id,
            'to_structure': self.to_structure.id,
        }
        request = self.factory.post(self.url, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlockMovement.objects.count(), 1)

        # Retrieve the updated flock from the database
        updated_flock = Flock.objects.get(id=self.flock.id)
        self.assertEqual(updated_flock.current_housing_structure, self.to_structure)

    def test_flock_movement_retrieve(self):
        """
        Test the 'retrieve' endpoint of the FlockMovementViewSet.

        It sends a GET request to the endpoint with a specific flock movement ID and verifies the response.

        """
        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        request = self.factory.get(url)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 200)

    def test_flock_movement_update(self):
        """
        Test the 'update' endpoint of the FlockMovementViewSet.

        It sends a PUT request to the endpoint with the necessary data and verifies the response.

        """
        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        data = {
            'flock': self.flock.id,
            'from_structure': self.flock.current_housing_structure.id,
            'to_structure': self.to_structure_2.id,
        }
        request = self.factory.put(url, data)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 200)

        # Retrieve the updated flock from the database
        updated_flock = Flock.objects.get(id=self.flock.id)
        self.assertEqual(updated_flock.current_housing_structure, self.to_structure_2)

    def test_flock_movement_delete(self):
        """
        Test the 'destroy' endpoint of the FlockMovementViewSet.

        It sends a DELETE request to the endpoint with a specific flock movement ID and verifies the response.

        """
        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        request = self.factory.delete(url)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FlockMovement.objects.count(), 0)


class FlockInspectionRecordViewSetTestCase(APITestCase):
    """
    Test case for the FlockInspectionRecordViewSet.

    This test case validates the behavior of the FlockInspectionRecordViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates housing structures, a flock source, and a flock.

        """
        self.factory = APIRequestFactory()
        self.viewset = FlockInspectionRecordViewSet.as_view(
            {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.viewset_retrieve = FlockInspectionRecordViewSet.as_view(
            {'get': 'retrieve'})
        self.url = reverse('poultry:flock-inspection-records-list')

        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.flock_source = FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm)
        self.flock = Flock.objects.create(
            source=self.flock_source,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=self.from_structure,
        )

    def test_list_records(self):
        """
        Test the 'list' endpoint of the FlockInspectionRecordViewSet.

        It sends a GET request to the endpoint and verifies the response.

        """
        request = self.factory.get(self.url)
        response = self.viewset(request)
        records = FlockInspectionRecord.objects.all()
        serializer = FlockInspectionRecordSerializer(records, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_record(self):
        """
        Test the 'create' endpoint of the FlockInspectionRecordViewSet.

        It sends a POST request to the endpoint with the necessary data and verifies the response.

        """
        data = {
            'flock': self.flock.pk
        }

        request = self.factory.post(self.url, data)
        response = self.viewset(request)
        record = FlockInspectionRecord.objects.last()
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_record(self):
        """
        Test the 'retrieve' endpoint of the FlockInspectionRecordViewSet.

        It sends a GET request to the endpoint with a specific flock inspection record ID and verifies the response.

        """
        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        request = self.factory.get(detail_url)
        response = self.viewset_retrieve(request, pk=record.pk)
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update_record(self):
        """
        Test the 'update' endpoint of the FlockInspectionRecordViewSet.

        It sends a PUT request to the endpoint with the necessary data and verifies the response.

        """
        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        data = {
            'flock': self.flock.pk,
            'number_of_dead_birds': 3
        }

        request = self.factory.put(detail_url, data)
        response = self.viewset(request, pk=record.pk)
        record = FlockInspectionRecord.objects.get(pk=record.pk)
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete_record(self):
        """
        Test the 'destroy' endpoint of the FlockInspectionRecordViewSet.

        It sends a DELETE request to the endpoint with a specific flock inspection record ID and verifies the response.

        """
        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        request = self.factory.delete(detail_url)
        response = self.viewset(request, pk=record.pk)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(FlockInspectionRecord.objects.filter(pk=record.pk).exists())