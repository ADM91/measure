__author__ = 'masslab'

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text
from sqlalchemy.sql import select, text
from config import db_usr, db_pwd, db_host_server, db_schema




# class User(DatabaseORM):
#     __table__ = user
#     id = Column('id', Integer, primary_key=True)
#     username = Column('username', Text)
#     password = Column('password', Text)



class DatabaseORM:
    """ Establish object relational mapping to mass calibration database.

    Instantiated in MainUI. Methods of this class execute individual database
    queries and return data in the format specified on the database.
    All database interaction takes place here.

    """
    def __init__(self):
        # Generate engine and session class for calibrations_v2 schema
        self.engine = create_engine("mysql://%s:%s@%s/%s" % (db_usr, db_pwd, db_host_server, db_schema), echo=False)

        # Reflect the database schema to a python object
        meta = MetaData()
        self.meta = meta.reflect(bind=self.engine)

        # Siphon out individual tables from database to python objects
        # Tables: Equipment
        self.balances = Table("balances", meta)
        self.barometers = Table("barometers", meta)
        self.hygrometers = Table("hygrometers", meta)
        self.thermometers = Table("thermometers", meta)
        self.stations = Table("stations", meta)

        # Tables: Environmental Data
        self.barometers_data = Table("barometers_data", meta)
        self.hygrometers_data = Table("hygrometers_data", meta)
        self.thermometers_data = Table("thermometers_data", meta)

        # Tables: Weights
        self.weights_external = Table("weights_external", meta)
        self.weights_internal = Table("weights_internal", meta)
        self.weights_internal_history = Table("weights_internal_history", meta)
        self.weights_internal_combos = Table("weights_internal_combos", meta)

        # Tables: Data Processing
        self.cal_data = Table("cal_data", meta)
        self.cal_lot = Table("cal_lot", meta)
        self.cal_series = Table("cal_series", meta)
        self.cal_weight_map = Table("cal_weight_map", meta)

        # Table: Designs
        self.designs = Table('designs', meta)
        self.designs_compatibility = Table('designs_compatibility', meta)

        # Table: User
        self.user = Table('user', meta)

    def check_user_password(self, usr, pwd):
        """ Return id if user and password exist

        Returns:
          user id
        """
        sql = text('SELECT id FROM user'
                   ' WHERE (user.username = "%s" and user.password = "%s")' % (usr, pwd))
        return self.engine.execute(sql).fetchall()

    def design_data(self, design_id):
        """ Return information about weighing design.

        Returns:
            (id(long), name(str), design(str))
        """
        sql = select([self.designs.c.id,
                      self.designs.c.name,
                      self.designs.c.design]).\
            where(self.designs.c.id == design_id)
        return self.engine.execute(sql).fetchall()[0]

    def balance_data(self, balance_id):
        """ Return balance metadata.

        Returns:
            (name(str), std dev(float))
        """
        sql = select([self.balances.c.name,
                      self.balances.c.within]).\
            where(self.balances.c.id == balance_id)
        return self.engine.execute(sql).fetchall()[0]

    def enviro_instrument_data(self, station_id):
        """ Return metadata from environmental instruments at station.

        Returns:
            instrument ids, correction coefficients and uncertainties
        """
        sql = select([self.stations.c.thermometer_id,
                      self.stations.c.barometer_id,
                      self.stations.c.hygrometer_id,
                      self.thermometers.c.coeff_a,
                      self.thermometers.c.coeff_b,
                      self.thermometers.c.coeff_c,
                      self.thermometers.c.uncertainty,
                      self.barometers.c.coeff_a,
                      self.barometers.c.coeff_b,
                      self.barometers.c.coeff_c,
                      self.barometers.c.uncertainty,
                      self.hygrometers.c.coeff_a,
                      self.hygrometers.c.coeff_b,
                      self.hygrometers.c.coeff_c,
                      self.hygrometers.c.uncertainty]).\
            select_from(self.stations.join(self.thermometers).join(self.barometers).join(self.hygrometers)).\
            where(self.stations.c.id == station_id)
        return self.engine.execute(sql).fetchall()[0]

    def external_weight_data(self, weight_id):
        """ Return metadata from weight in 'weight_external' table.

        Returns:
            weight id, nominal, density, density uncertainty, volumetric coeff of expansion, unit(imperial/metric)
        """
        sql = select([self.weights_external.c.id,
                      self.weights_external.c.nominal,
                      self.weights_external.c.density,
                      self.weights_external.c.density_uncert,
                      self.weights_external.c.volumetric_exp,
                      self.weights_external.c.units]).\
            where(self.weights_external.c.id == weight_id)
        return self.engine.execute(sql).fetchall()[0]

    def internal_weight_data(self, weight_id):
        """ Return metadata from weight in 'weight_internal_history' table.

        Note:
            This accesses the data from the weight history table, not the regular 'weight_internal'.  This ensures
            that the information at the time of weight selection is used (the most recent history id is selected).
            The weight metadata can be changed between selection and the calling of this method.

        Returns:
            weight id, nominal, density, density uncertainty, volumetric coeff of expansion, accepted value,
            type B uncertainty, between uncertainty, unit(imperial/metric)
        """
        sql = select([self.weights_internal_history.c.id,
                      self.weights_internal_history.c.nominal,
                      self.weights_internal_history.c.density,
                      self.weights_internal_history.c.density_uncert,
                      self.weights_internal_history.c.volumetric_exp,
                      self.weights_internal_history.c.accepted,
                      self.weights_internal_history.c.typeb_uncert,
                      self.weights_internal_history.c.between_uncert,
                      self.weights_internal_history.c.units]).\
            where(self.weights_internal_history.c.weight_id == weight_id).\
            order_by(self.weights_internal_history.c.id)
        return self.engine.execute(sql).fetchall()[-1]

    def addon_weight_data(self, addon_id):
        """ Return metadata of "add on" weights from 'weight_internal_history' table.

        Note:
            This accesses the data from the weight history table, not the regular 'weight_internal'.  This ensures
            that the information at the time of weight selection is used (the most recent history id is selected).
            The weight metadata can be changed between selection and the calling of this method.

        Returns:
            weight id, volumetric coeff of expansion, nominal, accepted value, density
        """
        sql = select([self.weights_internal_history.c.id,
                      self.weights_internal_history.c.volumetric_exp,
                      self.weights_internal_history.c.nominal,
                      self.weights_internal_history.c.accepted,
                      self.weights_internal_history.c.density]).\
            where(self.weights_internal_history.c.weight_id == addon_id).\
            order_by(self.weights_internal_history.c.id)
        return self.engine.execute(sql).fetchall()[-1]

    def station_id(self, balance_id):
        """ Return the station identifier given a selected balance.

        Note:
            This queries the 'stations' table and returns the row corresponding to the given balance id.
            If the balance id is not in the 'stations' table, this method returns a list of Nones

        Returns:
            station id, thermometer id, barometer id, hygrometer id
            or list(None, None, None, none) if balance is not assigned to a station
        """
        sql = select([self.stations.c.id,
                      self.stations.c.thermometer_id,
                      self.stations.c.barometer_id,
                      self.stations.c.hygrometer_id]).\
            where(self.stations.c.balance_id == balance_id)
        try:
            return self.engine.execute(sql).fetchall()[0]
        except IndexError:
            return [None, None, None, None]

    def instrument_ids(self, s_id):
        """ Return instrument ids corresponding to the station selected

        Returns:
            thermometer id, barometer id, hygrometer id
        """
        sql = select([self.stations.c.thermometer_id,
                      self.stations.c.barometer_id,
                      self.stations.c.hygrometer_id]).\
            where(self.stations.c.id == s_id)
        return self.engine.execute(sql).fetchall()[0]

    def latest_thermometer_data(self, t_id):
        """ Return latest value from selected thermometer

        Returns:
            temperature, timestamp, room, model, serial, probe
        """
        sql = text('SELECT a.temperature, '
                   'a.timestamp, '
                   'b.room, '
                   'b.model, '
                   'b.serial, '
                   'b.probe '
                   'FROM thermometers_data a, thermometers b '
                   'WHERE (a.thermometer_id = b.id and thermometer_id = %s) '
                   'ORDER BY timestamp desc '
                   'LIMIT 1;' % t_id)
        return self.engine.execute(sql).fetchall()[0]

    def latest_barometer_data(self, p_id):
        """ Return latest value from selected barometer

        Returns:
            pressure, timestamp, room, model, serial
        """
        sql = text('SELECT a.pressure, '
                   'a.timestamp, '
                   'b.room, '
                   'b.model, '
                   'b.serial '
                   'FROM barometers_data a, barometers b '
                   'WHERE (a.barometer_id = b.id and barometer_id = %s) '
                   'ORDER BY timestamp desc '
                   'LIMIT 1;' % p_id)
        return self.engine.execute(sql).fetchall()[0]

    def latest_hygrometer_data(self, h_id):
        """ Return latest value from selected hygrometer

        Returns:
            humidity, timestamp, room, model, serial
        """
        sql = text('SELECT a.humidity, '
                   'a.timestamp, '
                   'b.room, '
                   'b.model, '
                   'b.serial '
                   'FROM hygrometers_data a, hygrometers b '
                   'WHERE (a.hygrometer_id = b.id and hygrometer_id = %s) '
                   'ORDER BY timestamp desc '
                   'LIMIT 1;' % h_id)
        return self.engine.execute(sql).fetchall()[0]

    def get_serial_settings(self, balance_id):
        """ Return balance serial settings

        Returns:
            baudrate, parity, bytesize, stopbits, timeout
        """
        sql = select([self.balances.c.baudrate,
                      self.balances.c.parity,
                      self.balances.c.bytesize,
                      self.balances.c.stopbits,
                      self.balances.c.timeout]).\
            where(self.balances.c.id == balance_id)
        return self.engine.execute(sql).fetchall()[0]

    def get_weight_sets(self):
        """ Return list of mass sets (str) """
        sql = select([self.weights_internal.c.weight_set]).distinct().order_by(self.weights_internal.c.weight_set)
        return [r[0] for r in self.engine.execute(sql)]

    def get_weight_names(self, set_name):
        """ Return list of mass names (str) """
        sql = select([self.weights_internal.c.id,
                      self.weights_internal.c.weight_name]).\
            where(self.weights_internal.c.weight_set == set_name).\
            order_by(self.weights_internal.c.nominal.desc(),
                     self.weights_internal.c.weight_name)
        return [str(r[0]) + "|  " + r[1] for r in self.engine.execute(sql)]

    def get_customer_names(self):
        """ Return list of customer names (str) """
        sql = select([self.weights_external.c.customer_name]).\
            distinct().\
            order_by(self.weights_external.c.customer_name)
        return [r[0] for r in self.engine.execute(sql)]

    def get_customer_weight_names(self, customer):
        """ Return list of customer weight names (str) """
        sql = select([self.weights_external.c.id, self.weights_external.c.weight_name]).\
            where(self.weights_external.c.customer_name == customer).\
            order_by(self.weights_external.c.nominal.desc(), self.weights_external.c.weight_name)
        return [str(r[0]) + "|  " + r[1] for r in self.engine.execute(sql)]

    def get_balance_names(self):
        """ Return list of balance ids, names of form: "id | balance" """
        sql = select([self.balances.c.id,
                      self.balances.c.name]).\
            where(self.stations.c.balance_id == self.balances.c.id).\
            order_by(self.balances.c.id)
        return [str(r[0]) + " | " + r[1] for r in self.engine.execute(sql)]

    def get_viable_designs(self, balance_id):
        """ Return list of viable weighing designs based on the selected balance """
        # Get the balance type and number of positions from the balance id
        sql = select([self.balances.c.type,
                      self.balances.c.positions]).\
            where(self.balances.c.id == balance_id)
        bal_type, positions = self.engine.execute(sql).fetchall()[0]

        # Sql to be executed finds the name of designs that match the balance type and position count
        sql = text('SELECT a.id, a.name FROM designs a, designs_compatibility b '
                   'where a.id = b.design_id '
                   'and b.type = "%s" '
                   'and a.positions <= %s' % (str(bal_type), str(positions)))
        return [str(r[0]) + ' | ' + r[1] for r in self.engine.execute(sql)]
