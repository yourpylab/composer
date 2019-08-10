from pytest import fail, raises
import composer.aws.handshake.ssm as s
from pytest_mock import MockFixture
from mock import MagicMock
from typing import *
from botocore.exceptions import ClientError

def _ssm(mocker: MockFixture) -> Tuple:
    ssm_func: MagicMock = mocker.patch.object(s, "_ssm")
    ssm: MagicMock = MagicMock()
    ssm_func.return_value = ssm
    manager: s.SecretManager = s.SecretManager("MyProfile")
    return manager, ssm

def test_full():
    expected = "/Open990/MyProfile/MyValue"
    actual = s._full("MyProfile", "MyValue")
    assert actual == expected

def test_lookup_returns_from_ssm(mocker: MockFixture):
    manager, ssm = _ssm(mocker)
    ssm.get_parameter.return_value = {"Parameter": {"Value": "expected"}}
    actual: str = manager._lookup("MyProfile", "MyValue")
    assert "expected" == actual

def test_lookup_ssm_call(mocker: MockFixture):
    manager, ssm = _ssm(mocker)
    get_parameter: MagicMock = MagicMock()
    ssm.get_parameter = get_parameter
    manager._lookup("MyProfile", "MyValue")
    ssm.get_parameter.assert_called_once_with(Name="/Open990/MyProfile/MyValue", WithDecryption=True)

def _blow_up(code: str):
    def blow_up_function(*args, **kwargs):
        response = {
            "Error": {
                "Code": code
            }
        }
        raise ClientError(response, "get_parameter")

    return blow_up_function

def test_lookup_access_denied(mocker: MockFixture):
    manager, ssm = _ssm(mocker)
    get_parameter: MagicMock = MagicMock()
    ssm.get_parameter = get_parameter
    ssm.get_parameter.side_effect = _blow_up("AccessDeniedException")
    actual: str = manager._lookup("MyProfile", "MyValue")
    assert actual is None

def test_lookup_other_boto_error(mocker: MockFixture):
    manager, ssm = _ssm(mocker)
    get_parameter: MagicMock = MagicMock()
    ssm.get_parameter = get_parameter
    ssm.get_parameter.side_effect = _blow_up("MyFavoriteError")
    with raises(ClientError):
        manager._lookup("MyProfile", "MyValue")

class MyCustomException(Exception):
    pass

def test_lookup_other_exception(mocker: MockFixture):
    manager, ssm = _ssm(mocker)
    get_parameter: MagicMock = MagicMock()
    ssm.get_parameter = get_parameter

    def raise_exception(*args, **kwargs):
        raise MyCustomException

    ssm.get_parameter.side_effect = raise_exception
    with raises(MyCustomException):
        manager._lookup("MyProfile", "MyValue")

def _setup_resolve_test(mocker: MockFixture, valuesDict: Dict):
    manager, ssm = _ssm(mocker)

    def _get_parameter(Name: str=None, WithDecryption: bool=False):
        assert WithDecryption
        return valuesDict[Name]

    get_parameter: MagicMock = MagicMock()
    get_parameter.side_effect = _get_parameter
    ssm.get_parameter = get_parameter
    return manager, ssm

def test_resolve(mocker: MockFixture):
    valuesDict: Dict = {
        "/Open990/MyProfile/MyValue": {"Parameter": {"Value": "expected"}}
    }
    manager, ssm = _setup_resolve_test(mocker, valuesDict)
    actual = manager.resolve("MyValue")
    assert "expected" == actual

def test_resolve_default(mocker: MockFixture):
    valuesDict: Dict = {
        "/Open990/MyProfile/MyValue": {"Parameter": {"Value": None}},
        "/Open990/_default/MyValue": {"Parameter": {"Value": "expected"}}
    }

    manager, ssm = _setup_resolve_test(mocker, valuesDict)
    actual = manager.resolve("MyValue")
    assert "expected" == actual

def test_resolve_none(mocker: MockFixture):
    valuesDict: Dict = {
        "/Open990/MyProfile/MyValue": {"Parameter": {"Value": None}},
        "/Open990/_default/MyValue": {"Parameter": {"Value": None}}
    }
    manager, ssm = _setup_resolve_test(mocker, valuesDict)
    actual = manager.resolve("MyValue")
    assert actual is None
