__author__ = 'masslab'

from ingredient_methods import wait_time, short_command, short_command_no_resp, long_command, stab_time,\
    read_value_repeatedly


class RecipeMaker:
    """ Generate a list of methods that will take the mass balance through a calibration

    Args:
        status_signal (pyqtSignal): pyqtSignal object declared in "ComparatorUi"
        conn (serial): Serial connection object
        main_dict (dictionary):  Relevant calibration metadata
        settings_dict (dictionary): Specific balance and run settings from balance settings ui
        instruction_dict (dictionary):  Balance commands and statuses from config file
    """
    def __init__(self, status_signal, conn, main_dict, settings_dict, instruction_dict):
        self.ss = status_signal
        self.c = conn
        self.m_d = main_dict
        self.s_d = settings_dict
        self.i_d = instruction_dict
        self.m = []
        self.a = []
        self.data_d = {}
        self.make_recipe()

    def make_recipe(self):
        self._startup()
        self._set_resolution()
        self._centering()
        self._wait()
        self._pre_runs()
        self._runs()

    def _startup(self):
        # Startup
        self.m.append(short_command)
        self.a.append([self.ss, self.c, self.i_d['handshake on'][0][0], self.i_d['handshake on'][1]])
        self.m.append(short_command_no_resp)
        self.a.append([self.ss, self.c, self.i_d['beep'][0][0], self.i_d['beep'][1]])
        self.m.append(short_command_no_resp)
        self.a.append([self.ss, self.c, self.i_d['open door'][0][0], self.i_d['open door'][1]])
        self.m.append(short_command_no_resp)
        self.a.append([self.ss, self.c, self.i_d['close door'][0][0], self.i_d['close door'][1]])

    def _set_resolution(self):
        # Set comparator resolution
        n = self.s_d['resolution']
        self.m.append(short_command_no_resp)
        self.a.append([self.ss, self.c, self.i_d['resolution'][0][n], self.i_d['resolution'][1], str(n)])

    def _move_to(self, pos):
        # Move carousel to given position
        self.m.append(long_command)
        self.a.append([self.ss, self.c, self.i_d['lift'][0][0], self.i_d['lift'][1]])
        self.m.append(long_command)
        self.a.append([self.ss, self.c, self.i_d['move'][0][pos - 1], self.i_d['move'][1], str(pos)])

    def _sink_stabilize(self, sec):
        # Sink carousel and execute stabilization time
        self.m.append(long_command)
        self.a.append([self.ss, self.c, self.i_d['sink'][0][0], self.i_d['sink'][1]])
        self.m.append(stab_time)
        self.a.append([self.ss, self.i_d['stab time'], sec])

    def _read_value(self):
        int_time = int(self.s_d['int time'])
        self.m.append(read_value_repeatedly)
        self.a.append([self.ss, self.c, self.i_d['read'][0][0], self.i_d['read'][1], int_time])

    def _centering(self):
        # Centering
        n = int(self.s_d['centerings'])
        for i in range(n):
            for ii in range(4):
                self._move_to(ii+1)
                self._sink_stabilize(5)
            self._move_to(1)

    def _wait(self):
        # Wait time
        n = self.s_d['wait time']
        self.m.append(wait_time)
        self.a.append([self.ss, self.i_d['wait time'], n])

    def _pre_runs(self):
        # Pre runs
        n = int(self.s_d['pre runs'])
        design = self.m_d['design matrix']
        for i in range(n):
            for row in design:
                p1 = [a for a, b in enumerate(row) if b == 1][0] + 1
                p2 = [a for a, b in enumerate(row) if b == -1][0] + 1
                self._move_to(p1)
                self._sink_stabilize(5)
                self._move_to(p2)
                self._sink_stabilize(5)
                self._move_to(p2)
                self._sink_stabilize(5)
                self._move_to(p1)
                self._sink_stabilize(5)

    def _runs(self):
        # Runs
        n = int(self.s_d['runs'])
        design = self.m_d['design matrix']
        stab = int(self.s_d['stab time'])
        for i in range(n):
            self.data_d['run %02.0f' % (i+1)] = {}
            for index, row in enumerate(design):
                self.data_d['run %02.0f' % (i+1)]['observation %02.0f' % (index+1)] = {}
                self.data_d['run %02.0f' % (i+1)]['observation %02.0f' % (index+1)]['1-A1'] = []
                self.data_d['run %02.0f' % (i+1)]['observation %02.0f' % (index+1)]['2-B1'] = []
                self.data_d['run %02.0f' % (i+1)]['observation %02.0f' % (index+1)]['3-B2'] = []
                self.data_d['run %02.0f' % (i+1)]['observation %02.0f' % (index+1)]['4-A2'] = []
                p1 = [a for a, b in enumerate(row) if b == 1][0] + 1
                p2 = [a for a, b in enumerate(row) if b == -1][0] + 1
                self._move_to(p1)
                self._sink_stabilize(stab)
                self._read_value()
                self._move_to(p2)
                self._sink_stabilize(stab)
                self._read_value()
                self._move_to(p2)
                self._sink_stabilize(stab)
                self._read_value()
                self._move_to(p1)
                self._sink_stabilize(stab)
                self._read_value()
