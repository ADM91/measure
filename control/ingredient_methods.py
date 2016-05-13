__author__ = 'masslab'

import time
import re
import numpy as np
from decimal import Decimal
from utility.config import good_responses


def parse(string):
    return float(re.findall(r'[-.\d]+', string)[0])


def emit_status(signal, status, arg):
    try:
        signal.emit(status % arg)
    except TypeError:
        signal.emit(status)


def wait_time(signal, message, time_hours):
    """ Display wait time remaining in ui status browser by emitting signal """
    time_seconds = int(float(time_hours)*3600)
    for seconds in range(time_seconds, 0, -1):
        # Break seconds into hours minutes and seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        # Update status
        message_string = '%s hrs, %s min, %s sec' % (str(hours), str(minutes), str(seconds))
        emit_status(signal, message, message_string)
        # Wait a second
        time.sleep(0.95)
    emit_status(signal, '', [])


def stab_time(signal, message, time_seconds):
    """ Display stabilization time remaining in ui status browser by emitting signal """
    for seconds in range(time_seconds, 0, -1):
        # Update status
        emit_status(signal, message, str(seconds))
        # Wait a second
        time.sleep(1)
    signal.emit('')


def short_command(signal, conn, command, status_string, string_arg='', timeout=60):
    """ Send specified command (expects a balance response)to balance through "conn" and emit status signal """
    print "Command: " + command.strip('\r\n')
    emit_status(signal, status_string[0], string_arg)
    conn.open()
    # Wait until nothing can be read at the balance port
    while not timeout and conn.readlines():
        time.sleep(1)
        timeout -= 1
    # Write the command to the balance port and wait for response
    while timeout:
        time.sleep(1)
        conn.write(command)
        resp = conn.readlines()
        print resp
        print 'timeout: %s' % timeout
        if resp:
            if resp[0] in good_responses:
                conn.close()
                emit_status(signal, status_string[1], string_arg)
                return
        timeout -= 1
    conn.close()
    emit_status(signal, status_string[2], string_arg)
    return


def short_command_no_resp(signal, conn, command, status_string, string_arg='', timeout=5):
    """ Send specified command (expects no response) to balance through "conn" and emit status signal """
    print "Command: " + command.strip('\r\n')
    emit_status(signal, status_string[0], string_arg)
    conn.open()
    # Wait until nothing can be read at the balance port
    while not timeout and conn.readlines():
        time.sleep(1)
        timeout -= 1
    # Write the command to the balance port and wait for response
    conn.write(command)
    time.sleep(3)
    conn.close()
    emit_status(signal, status_string[1], string_arg)
    return


def read_value_repeatedly(signal, conn, command, status_string, int_time, timeout=60):
    """ Take balance signal reading through "conn" and return an average value """
    print "Command: " + command.strip('\r\n')
    conn.open()
    # Wait until nothing can be read at the balance port
    while not timeout and conn.readlines():
        time.sleep(1)
        timeout -= 1

    readings = []
    while int_time:
        # Ask comparator to start sending values
        conn.write(command)
        emit_status(signal, status_string[0], int_time)
        time.sleep(0.1)
        int_time -= 1
        reading = conn.readlines()
        if reading:
            print reading
            readings.append(parse(reading[0]))

    conn.close()
    print readings
    dec = abs(Decimal(str(readings[0])).as_tuple().exponent)
    value = format(np.mean(readings), '0.%sf' % str(dec + 1))
    print value
    emit_status(signal, status_string[1], value)
    return value


def long_command(signal, conn, command, status_string, string_arg='', timeout=60):
    """ Send specified command (expects delayed response) to balance through "conn" and emit status signal """
    print "Command: " + command.strip('\r\n')
    emit_status(signal, status_string[0], string_arg)
    conn.open()
    # Wait until nothing can be read at the balance port
    while not timeout and conn.readlines():
        time.sleep(1)
        timeout -= 1
    # Write the command to the balance port and wait for response
    while timeout:
        time.sleep(1)
        conn.write(command)
        resp = conn.readlines()
        if resp:
            print any([True for a in good_responses if a in resp[0]])
            if any([True for a in good_responses if a in resp[0]]):
                conn.close()
                emit_status(signal, status_string[1], string_arg)
                return
        print 'timeout: %s' % timeout
        timeout -= 1
    conn.close()
    emit_status(signal, status_string[2], string_arg)
    return


def id_command(signal, conn, command, status_string, timeout=60):
    """ Send id command to balance through "conn" and emit a special status signal """
    print "Command: " + command.strip('\r\n')
    signal.emit(status_string[0])
    conn.open()
    # Wait until nothing can be read at the balance port
    while not timeout and conn.readlines():
        time.sleep(1)
        timeout -= 1
    # Write the command to the balance port and wait for response
    while timeout:
        time.sleep(1)
        conn.write(command)
        resp = conn.readlines()
        if resp:
            conn.close()
            signal.emit(status_string[1] % ''.join(resp))
            return
        timeout -= 1
    conn.close()
    signal.emit(status_string[2])
    return
