template = """\
DROP FUNCTION get_one_{table_name}(id INTEGER);
CREATE OR REPLACE FUNCTION get_one_{table_name}(
  v_id INTEGER
)
RETURNS SETOF {table_name}
AS $$

BEGIN

  RETURN QUERY
  SELECT
    *
  FROM
    {table_name}
  WHERE
    {pk_name} = v_id
  LIMIT 1;

END;

$$ LANGUAGE plpgsql VOLATILE;
"""


def generate_code(dirpath, table_name, pk_name):
    if not isinstance(dirpath, str) or not isinstance(table_name, str) or not isinstance(pk_name, str):
        raise TypeError

    filename = "{dir}{table_name}_get_one.sql".format(dir=dirpath, table_name=table_name)

    with open(filename, mode='w') as f:
        f.write(template.format(table_name=table_name, pk_name=pk_name))
