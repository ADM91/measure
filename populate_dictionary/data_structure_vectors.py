__author__ = 'masslab'


def data_structure_vectors(cls):
    """ Populate main_dict with role vectors detected in user interface"""
    n = len(cls.main_dict['design matrix'][0])
    cls.main_dict['restraint vec'] = [0]*n
    cls.main_dict['check vec'] = [0]*n
    cls.main_dict['report vec'] = [0]*n
    for i in range(n):
        if cls.ui.weightTable.cellWidget(i, 1).currentText() == "Restraint":
            cls.main_dict['restraint vec'][i] = 1
        elif cls.ui.weightTable.cellWidget(i, 1).currentText() == "Check":
            cls.main_dict['check vec'][i] = 1
        else:
            cls.main_dict['report vec'][i] = 1
