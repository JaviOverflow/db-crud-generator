template = """\
CREATE OR REPLACE FUNCTION put_{table_name}(
  v_{pk_name} {pk_type},
{pmb_fields}
) RETURNS INTEGER
AS $$

  BEGIN

    UPDATE
      {table_name}
    SET
{update_set_items}
    WHERE
      {table_name}.{pk_name} = v_{pk_name};

    RETURN CASE
       WHEN FOUND THEN 1
                  ELSE 0
       END;

  END;

$$ LANGUAGE plpgsql;
"""


# update set item form :
#      <r_platforms = platforms,
#      r_initial_speed = initial_speed,
#      r_acceleration = acceleration,
#      r_direction = direction,
#      r_level_order = level_order>

def generate_code(dirpath, table_name, pk_name, pk_type, fields_name, fields_type):
    if not isinstance(dirpath, str) or not isinstance(pk_name, str) or not isinstance(pk_type, str) or \
            not isinstance(table_name, str) or not isinstance(fields_name, list) or not isinstance(fields_type, list):
        raise TypeError

    pmb_fields = ""
    for field, type in zip(fields_name, fields_type):
        pmb_fields += "  v_{field} {type},\n".format(field=field, type=type)
    pmb_fields = pmb_fields[:-2]

    update_set_items = ""
    for field in fields_name:
        update_set_items += "      {field} = v_{field},\n".format(field=field)
    update_set_items = update_set_items[:-2]

    with open("{dir}{table_name}_put.sql".format(dir=dirpath, table_name=table_name), 'w') as f:
        f.write(template.format(table_name=table_name, pk_name=pk_name, pk_type=pk_type,
                                pmb_fields=pmb_fields, update_set_items=update_set_items))
