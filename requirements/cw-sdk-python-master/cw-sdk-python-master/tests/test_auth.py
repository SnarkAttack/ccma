import os
from unittest.mock import patch, mock_open
from unittest import mock
import pytest


import cryptowatch
from cryptowatch.auth import read_config
from cryptowatch import rest_endpoint


def test_stream_auth_api_key_missing():
    # No API key set, should raise an exception
    with pytest.raises(cryptowatch.errors.APIKeyError):
        cryptowatch.api_key = ""
        cryptowatch.stream.subscriptions = ["markets:*:trades"]
        cryptowatch.stream.connect()


def test_allowance_not_mandatory_field(requests_mock):
    # 1st request has no allowance key
    requests_mock.get(
        "{}/markets/{}/{}/ohlc".format(rest_endpoint, "binance", "btcusdt"),
        status_code=200,
        text="""{
          "result": {
				"86400": [[1381190400,123.610000,123.610000,123.610000,123.610000,0.100000,0.0],
                          [1381276800,123.610000,124.190000,123.900000,124.180000,3.991600,0.0]]
			}
          }""",
    )
    candles = cryptowatch.markets.get("BINANCE:BTCUSDT", ohlc=True)
    assert candles._allowance == None
    # 2nd request has an allowance key
    requests_mock.get(
        "{}/markets/{}/{}/ohlc".format(rest_endpoint, "binance", "btcusdt"),
        status_code=200,
        text="""{
          "result": {
				"86400": [[1381190400,123.610000,123.610000,123.610000,123.610000,0.100000,0.0],
                          [1381276800,123.610000,124.190000,123.900000,124.180000,3.991600,0.0]]
			},
           "allowance": {"cost":4239786,"remaining":3862293338,"remainingPaid":0,
                         "upgrade":"Upgrade for a higher allowance, starting at $15/month for 16 seconds/hour. https://cryptowat.ch/pricing"}
          }""",
    )
    candles = cryptowatch.markets.get("BINANCE:BTCUSDT", ohlc=True)
    assert candles._allowance != None
    assert candles._allowance.cost != None
    assert candles._allowance.upgrade != None
    assert candles._allowance.remaining_paid != None
    assert candles._allowance.remaining != None
    # 3rd request has an allowance key but no remainingPaid
    requests_mock.get(
        "{}/markets/{}/{}/ohlc".format(rest_endpoint, "binance", "btcusdt"),
        status_code=200,
        text="""{
          "result": {
				"86400": [[1381190400,123.610000,123.610000,123.610000,123.610000,0.100000,0.0],
                          [1381276800,123.610000,124.190000,123.900000,124.180000,3.991600,0.0]]
			},
           "allowance": {"cost":4239786,"remaining":3862293338,
                         "upgrade":"Upgrade for a higher allowance, starting at $15/month for 16 seconds/hour. https://cryptowat.ch/pricing"}
          }""",
    )
    candles = cryptowatch.markets.get("BINANCE:BTCUSDT", ohlc=True)
    assert candles._allowance.remaining_paid == 0
    assert candles._allowance != None
    assert candles._allowance.cost != None
    assert candles._allowance.upgrade != None
    assert candles._allowance.remaining != None


def test_open_config_file(mocker):
    # Mock open()
    with patch("cryptowatch.auth.open", mock_open()) as config:
        # Mock os.environ.get()
        with mock.patch.dict("os.environ", {"HOME": "/sweet/home"}):
            # This should open() the credential file
            read_config()
            # Forge credential file path
            user_home_dir = os.environ.get("HOME")
            filepath = "{}/.cw/credentials.yml".format(user_home_dir)
            # Check it was well open()'ed
            config.assert_called_once_with(filepath, "r")
