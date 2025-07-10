# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT

import itertools

import pytest
import serial

from mfd_serial.serial import SerialConnection


class TestSerialConnection:
    class_under_test = SerialConnection

    @pytest.fixture()
    def serial_conn_clean(self):
        return self.class_under_test.__new__(self.class_under_test)

    @pytest.fixture()
    def serial_obj(self, mocker):
        serial.Serial = mocker.Mock()
        _serial = self.class_under_test(serial_port="/dev/ttyUSB0", baud=115200)
        return _serial

    def test_context_manager_calls_close(self, serial_conn_clean, mocker):
        serial_conn_clean.close = mocker.create_autospec(serial_conn_clean.close)

        with serial_conn_clean:
            pass

        serial_conn_clean.close.assert_called_once()

    def test_read(self, serial_obj):
        expected_str = "read_test"
        serial_obj._serial_connection.in_waiting = 5
        serial_obj._serial_connection.read.return_value = expected_str.encode()

        assert serial_obj.read() == expected_str

    def test_read_empty_buffer(self, serial_obj):
        serial_obj._serial_connection.in_waiting = 0

        assert serial_obj.read() == ""

    def test_read_until(self, serial_obj):
        pattern = "stop\n"
        serial_obj._serial_connection.readline.side_effect = [
            x.encode() for x in ["read_test\n", "read_until\n", f"{pattern}", "read_until\n"]
        ]

        data = serial_obj.read_until(pattern, 5)
        assert data.endswith(pattern)

    def test_read_until_timeout(self, serial_obj):
        serial_obj._serial_connection.readline.return_value = "read_test".encode()
        pattern = "stop"
        data = serial_obj.read_until(pattern, 0)
        assert pattern not in data

    def test_read_in_background(self, serial_obj):
        expected_str = "read_test\n"
        serial_obj._serial_connection.readline.side_effect = itertools.chain(
            [expected_str.encode()], itertools.repeat("")
        )
        serial_obj.read_in_background()
        assert serial_obj.get_result() == expected_str
