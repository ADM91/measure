__author__ = 'masslab'


def data_structure_cog(cls):
    """ Populate main_dict with differences in mass centers of gravity detected in user interface"""
    n = len(cls.main_dict['design matrix'][0])
    cls.main_dict['cg differences'] = [0]*n
    for i in range(n):
        cog = str(cls.ui.weightTable.cellWidget(i, 2).text())
        if cog:
            print 'got a cog difference.'
            cls.main_dict['cg differences'][i] = cog
