import ply.yacc as yacc
import os
from tokens import tokens

from pg_function_generators import pg_get_one, pg_get_all, pg_post, pg_put, pg_delete
from nodejs_generator import routes, pg_db_adapter


class Data:
    table_name = ""
    pk_name = ""
    pk_type = ""
    fields_name = []
    fields_type = []


def SyntaxAnalyzer(pg_functions_dirpath, nodejs_dirpath):
    def p_create_table(p):
        """table : init_mark table_pmb LPAREN columns RPAREN"""

        nodejs_routes_dirpath = nodejs_dirpath + "generated_routes/"
        if not os.path.exists(nodejs_routes_dirpath):
            os.mkdir(nodejs_routes_dirpath)

        generate_pg_functions(pg_functions_dirpath)

        generate_nodejs_routes(nodejs_routes_dirpath)
        generate_pg_db_adapter()

    def generate_pg_functions(pg_functions_dirpath):
        pg_get_one.generate_code(pg_functions_dirpath,
                                 table_name=Data.table_name,
                                 pk_name=Data.pk_name)
        pg_get_all.generate_code(pg_functions_dirpath,
                                 table_name=Data.table_name)
        pg_post.generate_code(pg_functions_dirpath,
                              table_name=Data.table_name,
                              pk_name=Data.pk_name,
                              fields_name=Data.fields_name,
                              fields_type=Data.fields_type)
        pg_put.generate_code(pg_functions_dirpath,
                             table_name=Data.table_name,
                             pk_name=Data.pk_name,
                             pk_type=Data.pk_type,
                             fields_name=Data.fields_name,
                             fields_type=Data.fields_type)
        pg_delete.generate_code(pg_functions_dirpath,
                                table_name=Data.table_name,
                                pk_name=Data.pk_name,
                                pk_type=Data.pk_type)

    def generate_nodejs_routes(nodejs_routes_dirpath):
        routes.generate_code(nodejs_routes_dirpath,
                             table_name=Data.table_name,
                             pk_name=Data.pk_name,
                             fields_name=Data.fields_name)

    def generate_pg_db_adapter():
        pg_db_adapter.generate_code(nodejs_dirpath)

    def p_init_mark(p):
        """init_mark :"""
        Data.table_name = ""
        Data.pk_name = ""
        Data.pk_type = ""
        Data.fields_name = []
        Data.fields_type = []

    def p_table_preamble(p):
        'table_pmb : CREATE TABLE ID'
        Data.table_name = p[3]
        print("Table {}.".format(p[3]))

    def p_columns_empty(p):
        """columns : ID DATATYPE """
        Data.pk_name = p[1]
        Data.pk_type = p[2] if not 'SERIAL' else 'INTEGER'
        print("{} is {}".format(p[1], p[2]))

    def p_columns_recursive(p):
        """columns : columns COMMA ID DATATYPE """
        Data.fields_name += [p[3]]
        Data.fields_type += [p[4]]
        print("{} is {}".format(p[3], p[4]))

    # Error rule for syntax errors
    def p_error(p):
        print("Syntax error in input!")

    return yacc.yacc()
