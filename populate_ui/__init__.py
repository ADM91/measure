__author__ = 'masslab'

from object_settings import object_settings
from populate_tree_widget import populate_tree_widget
from populate_balance_menu import populate_balance_menu
from populate_design_menu import populate_design_menu
from populate_table_widget import populate_table_widget


class PopulateUI:

    def __init__(self, main):
        object_settings(main)
        populate_tree_widget(main)
        populate_balance_menu(main)

    def design_menu(self, main):
        populate_design_menu(main)

    def table_widget(self, main):
        populate_table_widget(main)
