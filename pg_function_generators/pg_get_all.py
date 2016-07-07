template = """\
DROP FUNCTION get_all_{table_name}();
CREATE OR REPLACE FUNCTION get_all_{table_name}()
RETURNS SETOF {table_name}
AS $$

BEGIN

  RETURN QUERY
  SELECT
    *
  FROM
    {table_name};

END;

$$ LANGUAGE plpgsql VOLATILE;
"""


def generate_code(dirpath, table_name):
    if not isinstance(dirpath, str):
        raise TypeError

    filename = "{dir}{table_name}_get_all.sql".format(dir=dirpath, table_name=table_name)

    with open(filename, mode='w') as f:
        f.write(template.format(table_name=table_name))
