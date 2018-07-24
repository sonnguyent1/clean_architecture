import pytest
from unittest import mock

from clean_architecture.domain import models
from clean_architecture.use_cases import storageroom_use_case as uc
from clean_architecture.use_cases import request_objects as req
from clean_architecture.shared import response_object as  res


@pytest.fixture
def domain_storagerooms():
    storageroom_1 = models.StorageRoom(
        code='f853578c-fc0f-4e65-81b8-566c5dffa35a',
        size=215,
        price=39,
        longitude='-0.09998975',
        latitude='51.75436293',
    )

    storageroom_2 = models.StorageRoom(
        code='fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
        size=405,
        price=66,
        longitude='0.18228006',
        latitude='51.74640997',
    )

    storageroom_3 = models.StorageRoom(
        code='913694c6-435a-4366-ba0d-da5334a611b2',
        size=56,
        price=60,
        longitude='0.27891577',
        latitude='51.45994069',
    )

    storageroom_4 = models.StorageRoom(
        code='eed76e77-55c1-41ce-985d-ca49bf6c0585',
        size=93,
        price=48,
        longitude='0.33894476',
        latitude='51.39916678',
    )

    return [storageroom_1, storageroom_2, storageroom_3, storageroom_4]


def test_storageroom_list_without_parameters(domain_storagerooms):
    repo = mock.Mock()
    repo.list.return_value = domain_storagerooms

    storageroom_list_use_case = uc.StorageRoomListUseCase(repo)
    request_object = req.StorageRoomListRequestObject.from_dict({})

    response_object = storageroom_list_use_case.execute(request_object)

    assert bool(response_object) is True
    repo.list.assert_called_with(filters=None)

    assert response_object.value == domain_storagerooms


def test_storageroom_list_with_filters(domain_storagerooms):
    repo = mock.Mock()
    repo.list.return_value = domain_storagerooms

    user_case = uc.StorageRoomListUseCase(repo)
    qry_filter = {'a': 5}
    request_obj = req.StorageRoomListRequestObject.from_dict({'filters': qry_filter})
    response_obj = user_case.execute(request_obj)

    assert bool(response_obj) is True
    repo.list.assert_called_with(filters=qry_filter)
    assert response_obj.value == domain_storagerooms


def test_storageroom_list_handles_generic_error():
    repo = mock.Mock()
    repo.list.side_effect = Exception('Just an error message')

    storageroom_list_use_case = uc.StorageRoomListUseCase(repo)
    request_object = req.StorageRoomListRequestObject.from_dict({})

    response_object = storageroom_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.SYSTEM_ERROR,
        'message': "Exception: Just an error message"
    }


def test_storageroom_list_handles_bad_request():
    repo = mock.Mock()

    storageroom_list_use_case = uc.StorageRoomListUseCase(repo)
    request_object = req.StorageRoomListRequestObject.from_dict({'filters': 5})

    response_object = storageroom_list_use_case.execute(request_object)

    assert bool(response_object) is False
    assert response_object.value == {
        'type': res.ResponseFailure.PARAMETERS_ERROR,
        'message': "filters: Is not iterable"
    }
