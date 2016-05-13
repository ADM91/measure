__author__ = 'masslab'


def populate_design_menu(cls):
    design_names = cls.db.get_viable_designs(cls.main_dict['balance id'])
    cls.ui.designCombo.clear()
    cls.ui.designCombo.addItems(design_names)
