template="""\
var pgp      = require('pg-promise')({});
var database = pgp(process.env.DATABASE);

function fetchDataAndReturn(func, params, response, isList) {
    database.func(func, params)
        .then(function (data) {
            response.json((isList) ? data : data[0]);
        })
        .catch(function (error) {
            response.json(error);
        });
}

module.exports = {
    fetchListAndReturn: function (func, params, response) {
        fetchDataAndReturn(func, params, response, true);
    },
    fetchItemAndReturn: function (func, params, response) {
        fetchDataAndReturn(func, params, response, false);
    }
}
"""

def generate_code(dirpath):
    if not isinstance(dirpath, str):
        raise TypeError

    filename = "{dir}pg_db_adapter.js".format(dir=dirpath)

    with open(filename, mode='w') as f:
        f.write(template)
