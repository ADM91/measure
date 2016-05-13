__author__ = 'masslab'

from PyQt4 import QtGui, QtCore

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def populate_tree_widget(cls):
    # Get mass sets
    sets = cls.db.get_weight_sets()

    # get the mass names from every set and fill tree
    count = 0
    for set_name in sets:
        # Create top level set
        item_0 = QtGui.QTreeWidgetItem(cls.ui.weightTree)
        cls.ui.weightTree.topLevelItem(count).setText(0, _translate("MainWindow", set_name, None))
        item_0.setFlags(QtCore.Qt.ItemIsEnabled)

        # Get weight names
        weights = cls.db.get_weight_names(set_name)

        # Fill set with weights
        count2 = 0
        for n2 in weights:
            item_1 = QtGui.QTreeWidgetItem(item_0)
            cls.ui.weightTree.topLevelItem(count).child(count2).setText(0, _translate("MainWindow", n2, None))
            count2 += 1
        count += 1

    # Add external/customer weight section
    item_0 = QtGui.QTreeWidgetItem(cls.ui.weightTree)
    cls.ui.weightTree.topLevelItem(count).setText(0, _translate("MainWindow", "External", None))
    item_0.setFlags(QtCore.Qt.ItemIsEnabled)

    # Get customer names
    customers = cls.db.get_customer_names()

    count3 = 0
    for customer_name in customers:
        item_1 = QtGui.QTreeWidgetItem(item_0)
        cls.ui.weightTree.topLevelItem(count).child(count3).setText(0, _translate("MainWindow", customer_name, None))
        item_1.setFlags(QtCore.Qt.ItemIsEnabled)

        # Get customer weight names
        customer_weights = cls.db.get_customer_weight_names(customer_name)

        count4 = 0
        for n2 in customer_weights:
            item_2 = QtGui.QTreeWidgetItem(item_1)
            cls.ui.weightTree.topLevelItem(count).child(count3).child(count4).setText(0, _translate("MainWindow", "EXT|" + n2, None))
            count4 += 1

        count3 += 1
