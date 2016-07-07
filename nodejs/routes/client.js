var db = require('./../pg_db_adapter');
var express = require('express');

module.exports = function(app) {
    var clientsRouter = express.Router();

    clientsRouter.route('')

        .get(function(request, response) {
            db.fetchListAndReturn('get_all_client', [], response);
        })

        .post(function(request, response) {
            var body = request.body;
            var params = [
                body['name'],
                body['surname'],
                body['dni']
            ];
            db.fetchItemAndReturn('post_client', params, response);
        });

    clientsRouter.route('/:id')

        .get(function(request, response) {
            var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('get_one_client', params, response);
        })

        .put(function(request, response) {
            var body = request.body;
            var params = [
                body['id'],
                body['name'],
                body['surname'],
                body['dni']
            ];
            db.fetchItemAndReturn('put_client', params, response);
        })

        .delete(function(request, response) {
             var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('delete_client', params, response);
        });

    app.use('/clients', clientsRouter);
}
