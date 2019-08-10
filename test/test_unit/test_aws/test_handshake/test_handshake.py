from pytest import fail, raises
from pytest_mock import MockFixture
from mock import MagicMock
import composer.aws.handshake as h
import composer.aws.handshake.ssm as s
from typing import *

def test_handshake_cache():
    cache: Dict = MagicMock(spec=Dict)
    handshake: h.Handshake = h.Handshake(cache=cache)
    assert cache == handshake._cache
    assert handshake._ssm is None

def test_handshake_ssm():
    ssm: s.SecretManager = MagicMock(spec=s.SecretManager)
    handshake: h.Handshake = h.Handshake(ssm=ssm)
    assert ssm == handshake._ssm
    assert {} == handshake._cache

def test_ssm_and_cache_raises():
    with raises(AssertionError):
        ssm: s.SecretManager = MagicMock(spec=s.SecretManager)
        cache: Dict = MagicMock(spec=Dict)
        h.Handshake(ssm=ssm, cache=cache)

def test_neither_ssm_nor_cache_raises():
    with raises(AssertionError):
        h.Handshake()

def test_resolve(mocker: MockFixture):
    ssm: s.SecretManager = MagicMock(spec=s.SecretManager)
    handshake: h.Handshake = h.Handshake(ssm=ssm)
    resolve: MagicMock = mocker.patch.object(ssm, "resolve")
    resolve.return_value = "expected"
    actual = handshake._resolve("key to resolve")
    assert "expected" == actual

def _do_basic_get_test(mocker: MockFixture, expected: str, input: str, quote: bool):
    handshake: h.Handshake = h.Handshake(cache={})

    resolve = mocker.patch.object(handshake, "_resolve")
    resolve.return_value = input

    actual: str = handshake._get("key to resolve", quote=quote)
    assert actual == expected

def test_get_uncached(mocker: MockFixture):
    _do_basic_get_test(mocker, "expected", "expected", False)

def test_get_uncached_none(mocker: MockFixture):
    handshake: h.Handshake = h.Handshake(cache={})

    resolve = mocker.patch.object(handshake, "_resolve")
    resolve.return_value = None

    with raises(h.UnableToAccessParameter):
        handshake._get("key to resolve")

def test_get_cached():
    cache: Dict = {"key to resolve": "expected"}
    handshake: h.Handshake = h.Handshake(cache=cache)

    actual: str = handshake._get("key to resolve")
    assert "expected" == actual

def test_get_cached_none():
    cache: Dict = {"key to resolve": None}
    handshake: h.Handshake = h.Handshake(cache=cache)

    with raises(h.UnableToAccessParameter):
        handshake._get("key to resolve")

def test_get_quote_passthru(mocker: MockFixture):
    _do_basic_get_test(mocker, "expected", "expected", True)

def test_get_quote(mocker: MockFixture):
    _do_basic_get_test(mocker, "quote+this", "quote this", True)

def test_get_noquote(mocker: MockFixture):
    _do_basic_get_test(mocker, "quote this", "quote this", False)

def test_clone_forces(mocker: MockFixture):
    cache: Dict = MagicMock(spec=Dict)
    handshake: h.Handshake = h.Handshake(cache=cache)
    force: MagicMock = mocker.patch.object(handshake, "_force")
    handshake.clone()
    force.assert_called_once_with()

def test_clone_omits_ssm(mocker: MockFixture):
    cache: Dict = MagicMock(spec=Dict)
    handshake: h.Handshake = h.Handshake(cache=cache)
    mocker.patch.object(handshake, "_force")
    cloned: h.Handshake = handshake.clone()
    assert cloned._ssm is None


# noinspection PyUnresolvedReferences
def test_clone_twice_resolves_once(mocker: MockFixture):
    paths: Dict = { "parameter": "SSM path (relative to profile namespace)" }
    _paths: MagicMock = mocker.patch.object(h, "_paths")
    _paths.return_value = paths
    ssm: s.SecretManager = MagicMock(spec=s.SecretManager)
    handshake: h.Handshake = h.Handshake(ssm=ssm)
    ssm.resolve.return_value = "resolved parameter value"
    handshake.clone()
    handshake.clone()
    ssm.resolve.assert_called_once_with("SSM path (relative to profile namespace)")

# noinspection PyUnresolvedReferences
def test_force_resolves_as_needed(mocker: MockFixture):
    paths: Dict = {
        "parameter 1": "cached",
        "parameter 2": "uncached"
    }
    _paths: MagicMock = mocker.patch.object(h, "_paths")
    _paths.return_value = paths
    ssm: s.SecretManager = MagicMock(spec=s.SecretManager)
    handshake: h.Handshake = h.Handshake(ssm=ssm)
    handshake._cache["cached"] = "cached value"
    handshake.clone()
    ssm.resolve.assert_called_once_with("uncached")
