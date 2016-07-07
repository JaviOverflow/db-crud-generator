template = """\
CREATE OR REPLACE FUNCTION delete_{table_name} (
  v_{pk_name} {pk_type}
)
RETURNS INTEGER
AS $$

DECLARE

BEGIN

  DELETE FROM {table_name} WHERE {pk_name} = v_{pk_name};

  RETURN CASE FOUND WHEN TRUE THEN 1 ELSE 0 END;

END;

$$ LANGUAGE plpgsql VOLATILE COST 100;
"""


def generate_code(dirpath, pk_name, pk_type, table_name):
    if not isinstance(dirpath, str) or not isinstance(pk_name, str) or not isinstance(pk_type, str) or \
            not isinstance(table_name, str):
        raise TypeError

    with open("{dir}{table_name}_delete.sql".format(dir=dirpath, table_name=table_name), 'w') as f:
        f.write(template.format(table_name=table_name, pk_name=pk_name, pk_type=pk_type))
