# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT

# Put here only the dependencies required to run the module.
# Development and test requirements should go to the corresponding files.
"""serial example"""

from mfd_serial import SerialConnection

serial = SerialConnection(serial_port="/dev/ttyUSB0", baud=115200)

read_data = serial.read()

# when you want to run some test and wait for special log from serial
log = serial.read_until("LOG END", timeout=50)

# remember to close connection or use context manager

serial.close()

with SerialConnection(serial_port="/dev/ttyUSB0", baud=115200) as serial:
    data = serial.read()

# when you want collect all logs from serial during your test
serial = SerialConnection(serial_port="/dev/ttyUSB0", baud=115200)
serial.read_in_background()

# do some your stuff
# collect your logs at the end, get_results will also close your connection
serial_log = serial.get_result()
print(serial_log)
