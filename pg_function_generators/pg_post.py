template = """\
CREATE OR REPLACE FUNCTION post_{table_name}(
{pmb_fields}
) RETURNS SETOF {table_name}
AS $$

  DECLARE

    new_row_id INTEGER;

  BEGIN

    INSERT INTO {table_name} ({pk_name}{insert_fields})
              VALUES (DEFAULT{insert_values})
              RETURNING {pk_name} INTO new_row_id;

    RETURN QUERY
    SELECT *
    FROM {table_name}
    WHERE {table_name}.{pk_name} = new_row_id;

  END;

$$ LANGUAGE plpgsql;
"""


# pmb fields form :
#  <platforms TEXT,
#  initial_speed NUMERIC,
#  acceleration NUMERIC,
#  direction INTEGER>
# insert fields form : <, r_platforms, r_initial_speed, r_acceleration, r_direction, r_level_order>
# insert values form : <, platforms, initial_speed, acceleration, direction, highest_road_order()>

def generate_code(dirpath, table_name, pk_name, fields_name, fields_type):
    if not isinstance(dirpath, str) or not isinstance(pk_name, str) or \
            not isinstance(fields_name, list) or not isinstance(fields_type, list):
        raise TypeError

    pmb_fields = ""
    for field, type in zip(fields_name, fields_type):
        pmb_fields += "  v_{field} {type},\n".format(field=field, type=type)
    pmb_fields = pmb_fields[:-2]

    insert_fields = ""
    for field in fields_name:
        insert_fields += ", {field}".format(field=field)

    insert_values = ""
    for field in fields_name:
        insert_values += ", v_{field}".format(field=field)

    with open("{dir}{table_name}_post.sql".format(dir=dirpath, table_name=table_name), 'w') as f:
        f.write(template.format(table_name=table_name, pmb_fields=pmb_fields, pk_name=pk_name,
                                insert_fields=insert_fields, insert_values=insert_values))
