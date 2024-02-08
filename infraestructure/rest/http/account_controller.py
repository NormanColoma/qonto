from flask import Blueprint, request, Response, json
from application.process_transfers.process_transfers import ProcessTransfers
from application.process_transfers.process_transfers_command import ProcessTransfersCommand
from container import obj_graph
from domain.account.account_not_found_error import AccountNotFoundError
from infraestructure.rest.http.validator.rest_validators import validate_request_body

account_controller = Blueprint('account_controller', __name__)

post_request_contract = {
    'type': 'object',
    'properties': {
        'organization_iban': {'type': 'string'},
        'credit_transfers': {'type': 'array'},
    },
    'required': ['organization_iban', 'credit_transfers']
}


@account_controller.route('/accounts/transfers', methods=["PATCH"])
@validate_request_body(request, request_contract=post_request_contract)
def do_transfers_from_account():
    try:
        body = request.get_json()
        process_transfers = obj_graph.provide(ProcessTransfers)

        command = ProcessTransfersCommand(body['organization_iban'], body['credit_transfers'])
        process_transfers.execute(command)
        return Response(status=201, mimetype='application/json')
    except Exception as e:
        if isinstance(e, AccountNotFoundError):
            return Response(status=404, response=json.dumps({'message': e.message}), mimetype='application/json')
        raise e
