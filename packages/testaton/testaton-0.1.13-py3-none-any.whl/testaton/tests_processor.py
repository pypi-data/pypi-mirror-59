from pyspark.sql import SparkSession
from pyspark.sql import functions as sf
from hamcrest import has_length, equal_to, greater_than_or_equal_to, less_than_or_equal_to, all_of
import time
import sqlalchemy as sql
import pandas as pd
import re  # used for parsing connection string
import os  # used for pulling username and password env variables for db

from .generate_sql import generate_uniqueness_sql, generate_fk_sql, generate_filter_sql, generate_field_sql, generate_fk_sql_joins, generate_data_load_check_sql, generate_dataset_size_sql
from .test_executor import run_in_db, run_in_spark
from .common_functions import score

import findspark
findspark.init()

verbose = True


class Connection:
    """An object to represent a connection to a dataset, e.g. JDBC string, file location, etc"""

    def __init__(self, connection_def):
        self.type = connection_def['type']
        if self.type == "JDBC connection":
            conn_string = connection_def['connection-string']
            # connection string format: $USER_NAME:$PASS_WORD
            reg = re.compile("(\$[A-Z_]*):(\$[A-Z_]*)")
            v = reg.search(conn_string)
            if v:
                (username, password) = v.groups()[0], v.groups()[1]
                conn_string = conn_string.replace(
                    username, os.environ[username[1:]])
                conn_string = conn_string.replace(
                    password, os.environ[password[1:]])
            self.connection_string = conn_string


class Dataset:
    """An object that defines a dataset upon which operations will be conducted"""

    def __init__(self, connection_dict, dataset_definition):
        self.type = dataset_definition['type']
        self.connection = connection_dict[dataset_definition['connection']]
        self.location = dataset_definition['location']
        self.table_name = dataset_definition['table-name']
        self.setup(dataset_definition)

    def validate(self):
        """Validates whether the dataset exists and can be accessed"""
        # TODO create code to validate
        pass

    def setup(self, dataset_definition):
        """Setups up the dataset into a table if it needs to be setup"""
        if self.type == 'db-query':
            # TODO this might need a refactor
            viewSql = "create or replace view " + self.table_name + " as " + \
                dataset_definition['query']
            engine = sql.create_engine(self.connection.connection_string)
            if viewSql.find(';') != -1:
                raise Exception(
                    "Semi-colons in sql statements are not supported")
            engine.execute(viewSql)

        if self.type[0:4] == 'file':
            spark = SparkSession \
                .builder \
                .master("local") \
                .appName("TestingApp") \
                .getOrCreate()
            if self.type == 'file-parquet':
                df = spark.read.parquet(self.location)
                df.createOrReplaceTempView(self.table_name)
            if self.type == 'file-csv':
                df = spark.read.format("csv").option(
                    "header", "true").load(self.location)
                df.createOrReplaceTempView(self.table_name)

    def destroy(self):
        """Destroys temporary created datasets that where setup"""
        # TODO implement


def get_execution_environment(dataset):
    if dataset.type[0:2] == 'db':
        return {'type': 'db', 'connection': dataset.connection}
    if dataset.type[0:4] == 'file':
        return {'type': 'file', 'connection': dataset.location}


class Test:
    """Defines a single test to be executed"""

    def __init__(self, dataset_dict, test_definition, spark_config, dtest_obj):
        self.description = test_definition['description']
        self.type = test_definition['test_type']
        self.severity = test_definition['severity'] if 'severity' in test_definition else "Warn"
        self.definition = test_definition
        self.spark_config = spark_config
        self.dtest = dtest_obj
        self.test_def = test_definition
        # Disable a test by setting the disabled field to True
        self.disabled = test_definition['disabled'] if 'disabled' in test_definition else False
        self.sql = ""
        if self.type == 'unique':
            self.dataset = [dataset_dict[test_definition['dataset']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_uniqueness_sql(dataset_dict, test_definition)

        if self.type == 'foreign_key':
            self.dataset = [dataset_dict[test_definition['parent_dataset']],
                            dataset_dict[test_definition['child_dataset']]]
            if len(set([get_execution_environment(d)['type'] for d in self.dataset])) > 1:
                print(
                    "Operation across multiple types of datasets not currently supported")
                exit(-1)
            else:
                self.execution_env = get_execution_environment(self.dataset[0])
            ## self.sql = generate_fk_sql(dataset_dict, test_definition)
            self.sql = generate_fk_sql_joins(dataset_dict, test_definition)

        if self.type == 'data_load_check':
            self.dataset = [dataset_dict[test_definition['dataset']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_data_load_check_sql(
                dataset_dict, test_definition)

        if self.type == 'filter':
            self.dataset = [dataset_dict[test_definition['dataset']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_filter_sql(dataset_dict, test_definition)

        if self.type == 'field_accuracy':
            self.dataset = [dataset_dict[test_definition['dataset']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_field_sql(dataset_dict, test_definition)

        if self.type == "dataset_size":
            self.dataset = [dataset_dict[test_definition['dataset']]]
            self.execution_env = get_execution_environment(self.dataset[0])
            self.sql = generate_dataset_size_sql(dataset_dict, test_definition)

        self.validate_test()

    def validate_test(self):
        """Validates that the test does not contain anything stupid"""
        if self.sql.find(';') != -1:
            raise Exception("Semi-colons in sql statements are not supported")

    # Executes a test against a database
    def execute_db(self):
        if verbose:
            print("Test: " + self.description + " SQL: ")
            print(self.sql)
        # print(self.execution_env['connection'])
        return run_in_db(self.sql, self.execution_env['connection'].connection_string)

    # Execute a test in spark against a file
    def execute_file(self):
        return run_in_spark(self.sql, self.spark_config)

    def print_test_result(self, description, result_string):
        print("==============================================")
        print(description + "   ======>      " + result_string)
        print("==============================================")

    def process_result(self, test_type, result, duration):
        """Asserts the result of the test"""
        if test_type == 'unique':
            # TODO incorporate this with DTest - and inject duration
            # Idea: could these conditions be also defined as part of the test
            if len(result) == 0:
                self.print_test_result(self.description, "PASSED")
            else:
                self.print_test_result(self.description, "FAILED")
            self.dtest.assert_that(result, has_length(0), self.description)

        # minus filter
        # if test_type == 'foreign_key' or test_type == 'filter':
        #     if result['result_count'][0] == 0:
        #         print("Test: " + self.description + ";  PASSED")
        #     else:
        #         print("Test: " + self.description + ";  FAILED")
        #     self.dtest.assert_that(result['result_count'][0],
        #                            equal_to(0), self.description)

        if test_type == 'filter':
            if result['result_count'][0] == 0:
                self.print_test_result(self.description, "PASSED")
            else:
                self.print_test_result(self.description, "FAILED")
            self.dtest.assert_that(result['result_count'][0],
                                   equal_to(0), self.description)

        if test_type == 'data_load_check':
            # TODO incorporate this with DTest - and inject duration
            # Idea: could these conditions be also defined as part of the test
            if len(result) == 0:
                self.print_test_result(self.description, "PASSED")
            else:
                self.print_test_result(self.description, "FAILED")
            self.dtest.assert_that(result, has_length(0), self.description)

        # join filter
        if test_type == 'foreign_key':
            if result['result_count'][0] == 0:
                self.print_test_result(self.description, "PASSED")
            else:
                self.print_test_result(self.description, "FAILED")
            # print(pd.DataFrame(data=[result]).to_dict(orient='records'))
            # TODO
            # self.dtest.add_result(pd.DataFrame(
            #      data=[result]).to_dict(orient='records'), self.description)
            self.dtest.assert_that(result['result_count'][0],
                                   equal_to(0), self.description)

        if test_type == 'field_accuracy':
            # ensure that the variable values are integers
            result.iloc[:, 0] = result.iloc[:, 0].astype('float')
            result.iloc[:, 1] = result.iloc[:, 1].astype('float')
            ans = score(result.iloc[:, 0].values, result.iloc[:, 1].values)
            self.dtest.add_result(pd.DataFrame(
                data=[ans]).to_dict(orient='records'), self.description)

        if test_type == 'dataset_size':
            # makes sure that the dataset size is within a certain parameter
            rowCount = result.iloc[0, 0]
            min_val = int(self.test_def["min_value"])
            max_val = int(self.test_def["max_value"])
            if(rowCount >= min_val and rowCount <= max_val):
                self.print_test_result(self.description, "PASSED")
            else:
                self.print_test_result(self.description, "FAILED")
            self.dtest.assert_that(rowCount, all_of(greater_than_or_equal_to(
                min_val), less_than_or_equal_to(max_val)), self.description)

    def execute(self):
        if not self.disabled:
            start_time = time.time()
            if self.execution_env['type'] == 'db':
                result = self.execute_db()
            if self.execution_env['type'] == 'file':
                result = self.execute_file()
            end_time = time.time()
            duration = end_time - start_time
            self.process_result(self.type, result, duration)


def process_connections(connection_definition):
    connections = {}
    for k in connection_definition.keys():
        connections[k] = Connection(connection_definition[k])
    return connections


def process_datasets(connection_dict, dataset_definition):
    datasets = {}
    for d_key in dataset_definition.keys():
        datasets[d_key] = Dataset(connection_dict, dataset_definition[d_key])
    return datasets


def process_tests(dataset_dict, tests_definition, spark_config, dtest_obj):
    tests = {}
    for t_key in tests_definition.keys():
        tests[t_key] = Test(
            dataset_dict, tests_definition[t_key], spark_config, dtest_obj)
    return tests
