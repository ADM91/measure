__author__ = 'masslab'


# Name and software version
software_name = "MEASURE 0.2"

# This identifies the mass code path
masscode_path = r'Path'

# This identifies the base path the program will use to when prompting the user for input file directory
base_path = r'Path'

# Good balance response strings
good_responses = ['OK\r\n',
                  '\x11ready\r\n',
                  '\x13XON/XOFF handshake is enabled. \x11ready\r\n',
                  '\x13\x11ready\r\n']
# Bad response strings
error_responses = ['ES\r\n', ]

sleep_time = 0.2
long_command_timeout = 60
short_command_timeout = 10
max_timeouts = 3

# ---------------------Commands and statuses for balances control---------------------
AT106H = {'move': [['MOVE 1\r\n', 'MOVE 2\r\n', 'MOVE 3\r\n', 'MOVE 4\r\n'], ['Moving to position %s...', 'Movement complete', 'Error: failed to move to position %s']],
          'sink': [['SINK\r\n'], ['Sinking handler', 'Sink complete', 'Error: failed to sink handler']],
          'lift': [['LIFT\r\n'], ['Lifting handler', 'Lift complete', 'Error: failed to lift handler']],
          'beep': [['DB 1\r\n'], ['Beeping', 'Beep complete', 'Error: failed to beep']],
          'identify':   [['ID\r\n'], ['Identifying comparator', 'Id response:\n%s', 'Error: No balance response']],
          'resolution': [['RG F\r\n', 'RG C\r\n'], ['Setting balance resolution', 'Resolution set', 'Error: failed to set resolution%s']],
          'handshake on': [['HANDSHAKE_ON\r\n'], ['Turning handshake on', 'Handshake on', 'Error: failed to turn handshake on']],
          'open door': [['WI 0\r\n'], ['Opening door', 'Door open', 'Error: failed to open door']],
          'close door': [['WI 1\r\n'], ['Closing door', 'Door closed', 'Error: failed to close door']],
          'read': [['SI\r\n'], ['Integrating: %s s', 'Value: %s', 'Error: failed to read value']],
          'stab time':  'Stabilizing: %s s',
          'wait time': 'Executing wait time:\n%s left',
          'id': 68}
# -----------------------------------------------------------------------------------

comparator_matching = {68: AT106H}
