import logging
import pyhs2
from app import app


class HiveQuery(object):
    def __init__(self, **hive_cfg):
        self.args = self.create_hive_config(**hive_cfg)
        self.columns = []
        try:
            self.conn = pyhs2.connect(**self.args)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logging.error("Could not get a cursor. Reason:\n %s", e)

    def create_hive_config(self, **hive_cfg):
        hs2_conn_str = {}
        try:
            if 'database' in hive_cfg:
                hs2_conn_str['database'] = hive_cfg['database']
            else:
                hs2_conn_str['database'] = app.config['HIVE_DB']
            hs2_conn_str['host'] = app.config['HIVE_HOST']
            hs2_conn_str['port'] = app.config['HIVE_PORT']
            hs2_conn_str['authMechanism'] = app.config['HIVE_AUTH']
            hs2_conn_str['user'] = app.config['HIVE_USER']
            hs2_conn_str['password'] = app.config['HIVE_PASS']
        except Exception as e:
            logging.error("Could not set config parameter %s", e)
        return hs2_conn_str

    def getdb(self):
        return self.cursor.getDatabases()

    def query_exec(self, query):
        self.cursor.execute(query)
        schema = self.cursor.getSchema()
        if not self.columns:
            self.columns = [col['columnName'] for col in schema]
        while True:
            results = self.cursor.fetchSet()
            if not results:
                break
            for result in results:
                yield result
