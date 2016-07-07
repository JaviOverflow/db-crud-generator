template = """\
var db = require('./../pg_db_adapter');
var express = require('express');

module.exports = function(parentRouter) {{
    var {table_name}sRouter = express.Router();

    {table_name}sRouter.route('')

        .get(function(request, response) {{
            db.fetchListAndReturn('get_all_{table_name}', [], response);
        }})

        .post(function(request, response) {{
            var body = request.body;
            var params = [
{post_put_params}
            ];
            db.fetchItemAndReturn('post_{table_name}', params, response);
        }});

    {table_name}sRouter.route('/:id')

        .get(function(request, response) {{
            var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('get_one_{table_name}', params, response);
        }})

        .put(function(request, response) {{
            var body = request.body;
            var params = [
                body['{pk_name}'],
{post_put_params}
            ];
            db.fetchItemAndReturn('put_{table_name}', params, response);
        }})

        .delete(function(request, response) {{
             var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('delete_{table_name}', params, response);
        }});

    parentRouter.use('/{table_name}s', {table_name}sRouter);
}}
"""

# post put params form :
#                body['field1'],
#                body['field2'],
#                body['field3'],
#                body['field4']

def generate_code(dirpath, table_name, pk_name, fields_name):
    if not isinstance(dirpath, str) or not isinstance(table_name, str) or not isinstance(pk_name, str) \
            or not isinstance(fields_name, list):
        raise TypeError

    post_put_params = ""
    for field in fields_name:
        post_put_params += "                body['{field}'],\n".format(field=field)
    post_put_params = post_put_params[:-2]

    filename = "{dir}/{table_name}.js".format(dir=dirpath, table_name=table_name)

    with open(filename, mode='w') as f:
        f.write(template.format(table_name=table_name, pk_name=pk_name, post_put_params=post_put_params))
