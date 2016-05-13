__author__ = 'masslab'


def populate_balance_menu(cls):
    balance_strings = cls.db.get_balance_names()
    cls.ui.balNameCombo.addItems(balance_strings)
