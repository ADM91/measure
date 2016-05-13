__author__ = 'masslab'

from data_structure_addon_weights import data_structure_addon_weights
from data_structure_cog import data_structure_cog
from data_structure_vectors import data_structure_vectors
from data_structure_enviro import data_structure_enviro
from data_structure_weights import data_structure_weights


def populate_dictionary(cls):
    """ Takes information filled out by the user and populates main_dict. """
    data_structure_enviro(cls)
    data_structure_vectors(cls)
    data_structure_weights(cls)
    data_structure_addon_weights(cls)
    data_structure_cog(cls)
