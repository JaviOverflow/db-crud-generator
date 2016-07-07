from parser.syntax_analyzer import SyntaxAnalyzer
from parser.lexical_analyzer import LexicalAnalyzer
import os

TABLES_DIRPATH = "/Users/Mac/MY_DOCUMENTS/GEIN/4.1/Turismo/Practica/database/tables/"
STORED_PROCEDURES_DIRPATH = '/Users/Mac/MY_DOCUMENTS/GEIN/4.1/Turismo/Practica/database/functions/generated/'
NODEJS_DIRPATH = '/Users/Mac/MY_DOCUMENTS/GEIN/4.1/Turismo/Practica/webapp/server/'

def clean_sql(sql_file):
    if not isinstance(sql_file, file):
        raise TypeError

    sql = ""
    for line in sql_file.readlines():
        if not (line.startswith('DROP') or \
                        line.startswith('  ,CONSTRAINT') or \
                        line.startswith('  ,CHECK') or \
                        line.startswith('  ,PRIMARY') or \
                        line.startswith('  ,UNIQUE') or \
                        line.startswith('  ,FOREIGN')):
            sql += line
    return sql


def sql_files_at_dir(dirpath):
    if not isinstance(dirpath, str):
        raise TypeError
    for f in os.listdir(dirpath):
        if f.endswith('.sql'):
            yield "{}{}".format(TABLES_DIRPATH, f)


def main():

    for sql_filepath in sql_files_at_dir(TABLES_DIRPATH):
        with open(sql_filepath, "r") as sql_file:
            sql = clean_sql(sql_file)
            print(sql)

            lex = LexicalAnalyzer()
            lex.input(sql)
            for token in lex:
                print(token)

            yacc = SyntaxAnalyzer(pg_functions_dirpath=STORED_PROCEDURES_DIRPATH, nodejs_dirpath=NODEJS_DIRPATH)
            yacc.parse(sql, lexer=lex)

if __name__ == "__main__":
    main()
