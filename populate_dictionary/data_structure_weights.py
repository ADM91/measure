__author__ = 'masslab'

import numpy as np


def data_structure_weights(cls):
    """ Populate main_dict with weight metadata detected in user interface"""
    n = len(cls.main_dict['design matrix'][0])
    cls.main_dict['weight history id'] = [None]*n
    cls.main_dict['weight internal'] = [None]*n
    cls.main_dict['weight info'] = [None]*n
    cls.main_dict['weight type b'] = [None]*n
    cls.main_dict['weight between'] = [None]*n
    cls.main_dict['weight density uncert'] = [None]*n

    for i in range(n):
        weight_str = str(cls.ui.weightTable.item(i, 0).text())

        # External/Customer weights
        if len(weight_str.split("|")) == 3:
            weight_id = weight_str.split("|")[1]
            weight_name = weight_str.split("|")[2].lstrip()
            result = cls.db.external_weight_data(weight_id)
            nominal = str(format(result[1], ".1f"))
            density = str(format(result[2], ".6f"))
            coeff_exp = str(format(result[4], ".6f"))
            accepted = "0.00000"
            units = str(result[5])
            cls.main_dict['weight history id'][i] = str(result[0])
            cls.main_dict['weight internal'][i] = 0
            cls.main_dict['weight info'][i] = [weight_name + " "*(16-len(weight_name)) + "\t" + nominal + "\t" + density + "\t" + coeff_exp + "\t" + accepted]
            cls.main_dict['weight type b'][i] = None
            cls.main_dict['weight between'][i] = None
            cls.main_dict['weight density uncert'][i] = str(format(result[3], ".6f"))

        # Internal weights
        else:
            weight_id = weight_str.split("|")[0]
            weight_name = weight_str.split("|")[1].lstrip()
            result = cls.db.internal_weight_data(weight_id)
            nominal = str(format(result[1], ".1f"))
            density = str(format(result[2], ".6f"))
            coeff_exp = str(format(result[4], ".6f"))
            accepted = str(format(result[5], ".5f"))
            units = str(result[8])
            cls.main_dict['weight history id'][i] = str(result[0])
            cls.main_dict['weight internal'][i] = 1
            cls.main_dict['weight info'][i] = [weight_name + " "*(16-len(weight_name)) + "\t" + nominal + "\t" + density + "\t" + coeff_exp + "\t" + accepted]
            cls.main_dict['weight type b'][i] = str(format(result[6], ".6f"))
            cls.main_dict['weight between'][i] = str(format(result[7], ".6f"))
            cls.main_dict['weight density uncert'][i] = str(format(result[3], ".6f"))

    restraint_type_b = []
    check_between = []
    for i in range(n):
        if cls.main_dict['restraint vec'][i]:
            restraint_type_b.append(float(cls.main_dict['weight type b'][i]))
            check_between.append(0)
        elif cls.main_dict['check vec'][i]:
            restraint_type_b.append(0)
            check_between.append(float(cls.main_dict['weight between'][i]))
        else:
            restraint_type_b.append(0)
            check_between.append(0)

    restraint_type_b = np.sqrt(np.sum(np.square(restraint_type_b)))
    check_between = np.sqrt(np.sum(np.square(check_between)))

    # Store weight uncertainty stats
    cls.main_dict['restraint type b'] = str(format(restraint_type_b, '.5f'))
    cls.main_dict['check between'] = str(format(check_between, '.5f'))
    if units == 'M':
        cls.main_dict['units'] = 'METRIC'
    elif units == 'E':
        cls.main_dict['units'] = 'ENGLISH'
    else:
        pass
