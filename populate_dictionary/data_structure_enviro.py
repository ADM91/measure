__author__ = 'masslab'


def data_structure_enviro(cls):
    """ Populate main_dict with instrument correction coefficients and uncertainties from known station """
    result = cls.db.enviro_instrument_data(cls.main_dict['station id'])

    # Store Data
    cls.main_dict['temperature coeff'] = str(format(result[3], ".7f")) \
                                                    + " " + str(format(result[4], ".7f")) \
                                                    + " " + str(format(result[5], ".7f"))
    cls.main_dict['pressure coeff'] = str(format(result[7], ".7f")) \
                                                 + " " + str(format(result[8], ".7f")) \
                                                 + " " + str(format(result[9], ".7f"))
    cls.main_dict['humidity coeff'] = str(format(result[11], ".7f")) \
                                                 + " " + str(format(result[12], ".7f")) \
                                                 + " " + str(format(result[13], ".7f"))
    cls.main_dict['temperature uncert'] = str(format(result[6], ".7f"))
    cls.main_dict['pressure uncert'] = str(format(result[10], ".7f"))
    cls.main_dict['humidity uncert'] = str(format(result[14], ".7f"))