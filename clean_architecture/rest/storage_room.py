import json

from clean_architecture.repositories import mem_repo as mr
from clean_architecture.use_cases import request_objects as ro, storageroom_use_case as uc
from clean_architecture.serializers import storageroom_serializer as ser
from clean_architecture.shared import response_object as res
from flask import Blueprint, Response, request

STATUS_CODES = {
    res.ResponseSuccess.SUCCESS: 200,
    res.ResponseFailure.RESOURCE_ERROR: 404,
    res.ResponseFailure.PARAMETERS_ERROR: 400,
    res.ResponseFailure.SYSTEM_ERROR: 500
}

blueprint = Blueprint('storageroom', __name__)

storageroom1 = {
    'code': 'f853578c-fc0f-4e65-81b8-566c5dffa35a',
    'size': 215,
    'price': 39,
    'longitude': '-0.09998975',
    'latitude': '51.75436293',
}

storageroom2 = {
    'code': 'fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a',
    'size': 405,
    'price': 66,
    'longitude': '0.18228006',
    'latitude': '51.74640997',
}

storageroom3 = {
    'code': '913694c6-435a-4366-ba0d-da5334a611b2',
    'size': 56,
    'price': 60,
    'longitude': '0.27891577',
    'latitude': '51.45994069',
}


@blueprint.route('/storagerooms', methods=['GET'])
def storageroom():
    qrystr_params = {
        'filters': {},
    }

    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            qrystr_params['filters'][arg.replace('filter_', '')] = values

    request_obj = ro.StorageRoomListRequestObject.from_dict(qrystr_params)
    repo = mr.MemRepo([
        storageroom1,
        storageroom2,
        storageroom3,
    ])
    use_case = uc.StorageRoomListUseCase(repo)
    response_obj = use_case.execute(request_obj)
    return Response(json.dumps(response_obj.value, cls=ser.StorageRoomEncoder),
                    mimetype='application/json',
                    status=STATUS_CODES[response_obj.type])
