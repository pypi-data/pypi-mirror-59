import pandas as pd
import sqlalchemy as sql
import time


def run_in_db(testSql, connection_string):
    engine = sql.create_engine(connection_string)

    result = pd.read_sql_query(testSql, engine)
    return result


def run_in_spark(testSql, config):
    import findspark
    findspark.init()
    from pyspark.sql import SparkSession

    spark = SparkSession \
        .builder \
        .master(config['master']) \
        .appName(config['app-name']) \
        .getOrCreate()
    result = spark.sql(testSql)
    return result.toPandas()
