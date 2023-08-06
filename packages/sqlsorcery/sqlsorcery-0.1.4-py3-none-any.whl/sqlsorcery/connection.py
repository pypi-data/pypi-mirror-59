"""
.. module:: sqlsorcery
    :synopsis: module for simplifying SQL connections and CRUD actions

.. moduleauthor:: DC Hess <dc.hess@gmail.com>
"""

import pandas as pd
from sqlalchemy import create_engine, delete, inspect, update
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text as sa_text


class Connection:
    """Base class for sql connections containing shared class methods.

    .. note::
        This parent class is not meant to be called publicly and should
        only be used for inheritance in the specific connection types.
    """

    def get_columns(self, table):
        """Returns the column definitions for a given table.

        :param table: The name of the table to inspect. Do not include the schema prefix.
        :type table: string

        :return: A list of column definition dictionaries
        :rtype: list
        """
        inspector = inspect(self.engine)
        return inspector.get_columns(table, schema=self.schema)

    def get_view_definition(self, view):
        """Returns the view definition (DDL) for a given SQL view.

        :param view: The name fo the view to inspect. Do not include the schema prefix.
        :type view: string

        :return: Multi-line string of the view definition text
        :rtype: string
        """
        inspector = inspect(self.engine)
        return inspector.get_view_definition(view, schema=self.schema)

    def delete(self, tablename):
        """Deletes all records in a given table. Does not reset identity columns.

        :param tablename: Name of the table to delete records for
        :type tablename: string
        """
        metadata = MetaData()
        table = Table(
            tablename,
            metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=self.schema,
        )
        self.engine.execute(delete(table))

    def truncate(self, tablename):
        """Truncates a given table. Faster than a delete and reseeds identity values.

        .. note::
            **Security Warning**: This command leverages interpolated strings and
            as such is vulnerable to SQL-injection. Do not use in conjunction with
            arbitrary user input. Instead, use .delete()

        :param tablename: Name of the table to truncate
        :type tablename: string
        """
        sql_str = f"TRUNCATE TABLE {self.schema}.{tablename}"
        command = sa_text(sql_str).execution_options(autocommit=True)
        self.engine.execute(command)

    def exec_sproc(self, stored_procedure):
        """Executes a stored procedure

        .. note::
            **Security Warning**: This command leverages interpolated strings and
            as such is vulnerable to SQL-injection. Do not use in conjunction with
            arbitrary user input.

        :param stored_procedure: The name of the stored procedure to be executed.
        :type stored_procedure: string

        :return: Stored procedure results
        :rtype: `SQLAlchemy.ResultProxy <https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.ResultProxy>`_
        """
        sql_str = f"EXEC {self.schema}.{stored_procedure}"
        command = sa_text(sql_str)
        return self.engine.execute(command)

    def exec_cmd(self, command):
        """Executes an arbitrary sql command on the database.

        .. note::
            **Security Warning**: This command is vulnerable to SQL-injection.
            Do not use in conjunction with arbitrary user input.

        :param command: The SQL command to be executed
        :type command: string
        """
        return self.engine.execute(command)

    def exec_cmd_from_file(self, filename):
        """Executes an arbitrary sql command provided from a .sql file.

        :param filename: Path to .sql file containing a query
        :type filename: string

        :return: Resulting dataset from query
        :rtype: `Pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
        """
        sql_statement = self._read_sql_file(filename)
        return self.engine.execute(sql_statement)

    def table(self, tablename):
        """Returns a SQLAlchemy table object for further manipulation such as updates.

        :param tablename: Name of the table to return
        :type tablename: string

        :return: A table
        :rtype: `SQLAlchemy.Table <https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table>`_
        """
        metadata = MetaData()
        table = Table(
            tablename,
            metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=self.schema,
        )
        return table

    def _read_sql_file(self, filename):
        """Reads a sql file into a sql query string"""
        with open(filename) as f:
            return f.read()

    def query(self, sql_query, params=None):
        """Executes the given sql query


        :param sql_query: SQL query string
        :type sql_query: string
        :param params: list or dict of parameters to pass to sql query
        :type params: list or dict

        .. note::
            See `PEP249 <https://www.python.org/dev/peps/pep-0249/>`_ for possible paramstyles.

        :return: Resulting dataset from query
        :rtype: `Pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
        """
        df = pd.read_sql_query(sql_query, self.engine, params=params)
        return df

    def query_from_file(self, filename):
        """Executes the given sql query from a provided sql file

        :param filename: Path to .sql file containing a query
        :type filename: string

        :return: Resulting dataset from query
        :rtype: `Pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
        """
        sql_statement = self._read_sql_file(filename)
        df = pd.read_sql_query(sql_statement, self.engine)
        return df

    def insert_into(self, table, df, if_exists="append"):
        """Inserts the data in a pandas dataframe into a specified sql table

        :param table: Name of sql table to insert data into
        :type table: string

        :param df: DataFrame to be inserted
        :type df: `Pandas.DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_

        :param if_exists: How to behave if the table already exists.
            Possible options: *fail*, *append*, *replace*.
            Default = *append*
        :type if_exists: string

        :return: None
        """
        df.to_sql(
            table, self.engine, schema=self.schema, if_exists=if_exists, index=False
        )
