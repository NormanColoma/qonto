import pytest

from app import app
from domain.account.account_not_found_error import AccountNotFoundError
from domain.common.application_error import ApplicationError


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


def test_should_return_BAD_REQUEST_when_organization_iban_field_is_missing(client):
    result = client.patch('/accounts/transfers', json={})
    assert result.status_code == 400
    assert result.json == {
        'message': "Field 'organization_iban' is a required property"
    }


def test_should_return_BAD_REQUEST_when_credit_transfers_field_is_missing(client):
    result = client.patch('/accounts/transfers', json={"organization_iban": 'iban'})
    assert result.status_code == 400
    assert result.json == {
        'message': "Field 'credit_transfers' is a required property"
    }


def test_should_return_BAD_REQUEST_when_transfers_field_is_not_array(client):
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": 'iban', "credit_transfers": 'not-array'})
    assert result.status_code == 400
    assert result.json == {
        'message': "Field 'credit_transfers' has no correct format"
    }


def test_should_return_BAD_REQUEST_when_organization_iban_is_not_string(client):
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": 123, "credit_transfers": []})
    assert result.status_code == 400
    assert result.json == {
        'message': "Field 'organization_iban' has no correct format"
    }


def test_should_return_NOT_FOUND_when_account_not_found(client, mocker):
    mocker.patch('application.process_transfers.process_transfers.ProcessTransfers.execute',
                 side_effect=AccountNotFoundError("error"))
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": "iban", "credit_transfers": []})
    assert result.status_code == 404
    assert result.json == {'message': "error"}


def test_should_return_UNPROCESSABLE_ENTITY_when_there_is_application_error(client, mocker):
    mocker.patch('application.process_transfers.process_transfers.ProcessTransfers.execute',
                 side_effect=ApplicationError("error"))
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": "iban", "credit_transfers": []})
    assert result.status_code == 422
    assert result.json == {'message': "error"}


def test_should_return_SERVER_ERROR_when_there_is_server_error(client, mocker):
    mocker.patch('application.process_transfers.process_transfers.ProcessTransfers.execute',
                 side_effect=Exception)
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": "iban", "credit_transfers": []})
    assert result.status_code == 500
    assert result.json == {'message': "Internal server error"}


def test_should_return_NO_CONTENT_when_transfers_done(client, mocker):
    mocker.patch('application.process_transfers.process_transfers.ProcessTransfers.execute')
    result = client.patch('/accounts/transfers',
                          json={"organization_iban": "iban", "credit_transfers": []})
    assert result.status_code == 204
