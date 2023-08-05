from nada_dataprofilering.sql_script_generator.generic_functions import *
from nada_dataprofilering.sql_script_generator.util_functions import *


def num_rows(schema_name, table_name, column_name):

    return basic_function_and_update(schema_name,
                                     table_name,
                                     column_name,
                                     'count',
                                     'integer',
                                     'num_rows')


def num_nulls(schema_name, table_name, column_name):

    return count_value_function_and_update(schema_name,
                                           table_name,
                                           column_name,
                                           'NULL',
                                           'num_nulls')


def count_distinct(schema_name, table_name, column_name):
    declare_string = declare_variables([{'name': 'answer', 'data_type': 'integer'}])

    select_into_string = f"select count(distinct {column_name}) into " + into(schema_name, table_name, 'answer')

    update_string = update_nada_profilering(schema_name, table_name, column_name, 'num_unique', 'answer')

    sql_string = declare_string + begin_and_end(select_into_string + update_string)

    return sql_string


def num_nulls_pct(schema_name, table_name, column_name):
    declare_string = declare_variables([{'name': 'null_percent', 'data_type': 'number'},
                                        {'name': 'antall_nulls', 'data_type': 'integer'},
                                        {'name': 'antall_rader', 'data_type': 'integer'}])

    select_into_rows_string = standard_select(column_name, 'count') + into(schema_name, table_name, 'antall_rader')
    select_into_nulls_string = count_value_select(column_name, 'NULL') + into(schema_name, table_name, 'antall_nulls')
    computing_pct_string = "null_percent := antall_nulls / antall_rader;\n"

    update_string = update_nada_profilering(schema_name, table_name, column_name, 'pct_nulls', 'null_percent')

    sql_string = declare_string + begin_and_end(
        select_into_nulls_string + select_into_rows_string + computing_pct_string + update_string)

    return sql_string


def num_unique_pct(schema_name, table_name, column_name):
    declare_string = declare_variables([{'name': 'unique_percent', 'data_type': 'number'},
                                        {'name': 'antall_unique', 'data_type': 'integer'},
                                        {'name': 'antall_rader', 'data_type': 'integer'}])

    select_into_rows_string = standard_select(column_name, 'count') + into(schema_name, table_name, 'antall_rader')
    select_into_nulls_string = f"select count(distinct {column_name}) " + into(
        schema_name, table_name, 'antall_unique')

    computing_pct_string = "unique_percent := antall_unique / antall_rader;\n"

    update_string = update_nada_profilering(schema_name, table_name, column_name, 'pct_unique', 'unique_percent')

    sql_string = declare_string + begin_and_end(
        select_into_nulls_string + select_into_rows_string + computing_pct_string + update_string)

    return sql_string
