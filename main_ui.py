__author__ = 'masslab'

import sys
from threading import Thread
from Queue import Queue
from PyQt4 import QtGui, uic
from database_orm import DatabaseORM
from utility.run_masscode_queue import run_masscode_queue
from utility.config import base_path
from utility.show_dictionary import pretty
from utility.config import software_name
from sub_ui.comparator_ui import ComparatorUi
from sub_ui.error_message import ErrorMessage
from sub_ui.login import LoginUi
from populate_ui import PopulateUI
from populate_dictionary import populate_dictionary


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MainUI:
    """ Provides functionality for the main user interface

    The main functionality available in this user interface is balance, weighing design, and weight selection for
    a potential mass calibration.  Additional functionality includes "masscode" input file processing,
    "masscode" output file parsing and graphing, and mass station manipulation.

    The user interface object structure is loaded from the QT Designer xml file 'main.ui' using the PyQt4.uic module.
    MainUI creates an instance of the DatabaseORM class, which is used to fetch data from the calibration database.
    Information on the database populates various menus in the user interface and ultimately stores the
    mass calibration data for easy manipulation.  The DatabaseORM instance is passed to the comparator sub-ui

    The dictionary main_dict collects all metadata necessary to process a mass calibration.  This dictionary
    is passed to the comparator sub-ui.

    Args:
       window(QtGui object):  the parent object which the user interface inherits
    """

    # Initialize main dictionary
    main_dict = {'design id': None,
                 'design name': '',
                 'design matrix': [],
                 'balance id': None,
                 'balance name': None,
                 'balance std dev': None,
                 'balance port': None,
                 'balance serial settings': [],
                 'station id': None,
                 'thermometer id': None,
                 'temperature coeff': None,
                 'temperature uncert': None,
                 'barometer id': None,
                 'pressure coeff': None,
                 'pressure uncert': None,
                 'hygrometer id': None,
                 'humidity coeff': None,
                 'humidity uncert': None,
                 'restraint vec': [],
                 'check vec': [],
                 'report vec': [],
                 'next restraint vec': [],
                 'addon info': [],
                 'addon history id': [],
                 'weight info': [],
                 'weight history id': [],
                 'weight internal': [],
                 'weight type b': [],
                 'weight between': [],
                 'weight density uncert': [],
                 'cg differences': [],
                 'restraint type b': None,
                 'check between': None,
                 'units': None}

    def __init__(self, window):
        window.setWindowIcon(QtGui.QIcon('Masses.png'))
        window.setWindowTitle(software_name)
        self.ui = uic.loadUi('main.ui', window)

        # Instantiate the database object relational mapping with login()
        self.db = None
        self.login()

        # Populate the menus within the main UI via the database
        self.populate_ui = PopulateUI(self)

        self.input_file_queue = Queue()

        # Temporary testing config
        self.ui.balNameCombo.setCurrentIndex(2)

        # Activate the event handlers
        self.handler_connector()

        # Display the main UI
        window.show()

    def handler_connector(self):
        """ Activate event detection"""
        self.ui.balNameCombo.activated.connect(self.activate_balance)
        self.ui.designCombo.activated.connect(self.activate_design)
        self.ui.inputButton.clicked.connect(self.click_input)
        self.ui.masscodeButton.clicked.connect(self.click_masscode)
        self.ui.configBalButton.clicked.connect(self.click_config_bal)
        app.aboutToQuit.connect(self.exit_function)

    def widget_handler(self, arg):
        """ Enable or disable widgets in main ui as specified in list arg"""
        self.ui.balNameCombo.setEnabled(arg[0])
        self.ui.designCombo.setEnabled(arg[1])
        self.ui.weightTable.setEnabled(arg[2])
        self.ui.configBalButton.setEnabled(arg[3])
        self.ui.masscodeButton.setEnabled(arg[4])

    def login(self):
        """ Prompt user for database credentials """
        while True:
            # Execute login user interface
            credentials = LoginUi()
            credentials.exec_()
            usr = str(credentials.textName.text())
            pwd = str(credentials.textPass.text())

            try:
                # Try instantiating database object with given credentials
                self.db = DatabaseORM(usr, pwd)
                return
            except Exception as e:
                print e
                print "Incorrect username or password"
                error_message = ErrorMessage("Incorrect username or password")
                error_message.exec_()

    def click_config_bal(self):
        """ Populate main_dict with selected items and call the comparator user interface """
        # Populate and show main dictionary
        populate_dictionary(self)
        pretty(self.main_dict)

        # TEMPORARY CODE, saves main dictionary for debugging purposes
        # ---------------------------------------------------------
        # with open('SubUIs/main_dict.json', 'w+') as fp:
        #     json.dump(self.main_dict, fp)
        # ---------------------------------------------------------

        # Initializes the balance ui class stored in the balance dict under the balance id in the main dict
        ComparatorUi(self.main_dict, self.db)

    def activate_balance(self):
        """ Newly selected balance is used to populate main_dict and weighing design menu """
        # Reset the design combo box and weight table
        self.ui.designCombo.clear()
        self.ui.weightTable.setRowCount(0)
        self.main_dict['balance id'] = int(self.ui.balNameCombo.currentText().split(" | ")[0])
        self.main_dict['balance serial settings'] = list(self.db.get_serial_settings(self.main_dict['balance id']))
        [name, std] = self.db.balance_data(self.main_dict['balance id'])
        self.main_dict['balance name'] = name
        self.main_dict['balance std dev'] = float(std)

        # Populate design menu with designs compatible with selected balance
        self.populate_ui.design_menu(self)

        # Find the station id using the balance id and set the station combo
        [self.main_dict['station id'],
         self.main_dict['thermometer id'],
         self.main_dict['barometer id'],
         self.main_dict['hygrometer id']] = self.db.station_id(self.main_dict['balance id'])
        self.update_environment_table()

    def update_environment_table(self):
        """ Fetch latest environment data from database and display in environment table """
        t_row = self.db.latest_thermometer_data(self.main_dict['thermometer id'])
        p_row = self.db.latest_barometer_data(self.main_dict['barometer id'])
        h_row = self.db.latest_hygrometer_data(self.main_dict['hygrometer id'])

        for index_1, instrument in enumerate([t_row, p_row, h_row]):
            for index_2, field in enumerate(instrument):
                item = QtGui.QTableWidgetItem()
                item.setText(str(field))
                self.ui.enviroTable.setItem(index_1, index_2, item)
        self.ui.enviroTable.resizeColumnsToContents()

    def activate_design(self):
        """ Populate main_dict with selected design and initialize the weight table with appropriate number of rows """
        # Transfer the design info into the dictionary
        [self.main_dict['design id'],
         self.main_dict['design name'],
         array] = self.db.design_data(int(self.ui.designCombo.currentText().split("|")[0]))

        # Display design name in the status browser
        self.ui.statusBrowser.clear()
        self.ui.statusBrowser.append('Design: ' + self.main_dict['design name'])

        # Collect design into array and display in status browser
        self.main_dict['design matrix'] = []
        for row in array.split(' ; '):
            self.main_dict['design matrix'].append([int(a) for a in row.split(' ')])
            self.ui.statusBrowser.append(row)

        # Populate the weight table based on chosen design
        self.populate_ui.table_widget(self)

    def click_input(self):
        """ Prompt user to select input files to be added to the input file list """
        file_dialog = QtGui.QFileDialog()
        file_names = QtGui.QFileDialog.getOpenFileNames(file_dialog, "Select masscode input files", base_path, "*.ntxt")
        self.ui.inputList.addItems(file_names)
        self.ui.masscodeButton.setEnabled(True)

    def click_masscode(self):
        """ Push input files in ui.inputList through the masscode (multi-threaded) """
        self.ui.masscodeButton.setEnabled(False)
        self.ui.statusBrowser.clear()
        for n in range(self.ui.inputList.count()):
            print self.ui.inputList.item(n).text()
            self.input_file_queue.put(str(self.ui.inputList.item(n).text()))
        for n in range(5):
            masscode_t = Thread(target=run_masscode_queue, args=(self,))
            masscode_t.start()
        self.ui.statusBrowser.append("Task complete!")

    @staticmethod
    def exit_function():
        app.quit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    main_window = QtGui.QMainWindow()
    main_ui = MainUI(main_window)
    sys.exit(app.exec_())
