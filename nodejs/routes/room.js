var db = require('./../pg_db_adapter');
var express = require('express');

module.exports = function(app) {
    var roomsRouter = express.Router();

    roomsRouter.route('')

        .get(function(request, response) {
            db.fetchListAndReturn('get_all_room', [], response);
        })

        .post(function(request, response) {
            var body = request.body;
            var params = [
                body['code'],
                body['description'],
                body['amount'],
                body['adult_capacity'],
                body['kid_capacity'],
                body['adult_price'],
                body['kid_price']
            ];
            db.fetchItemAndReturn('post_room', params, response);
        });

    roomsRouter.route('/:id')

        .get(function(request, response) {
            var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('get_one_room', params, response);
        })

        .put(function(request, response) {
            var body = request.body;
            var params = [
                body['id'],
                body['code'],
                body['description'],
                body['amount'],
                body['adult_capacity'],
                body['kid_capacity'],
                body['adult_price'],
                body['kid_price']
            ];
            db.fetchItemAndReturn('put_room', params, response);
        })

        .delete(function(request, response) {
             var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('delete_room', params, response);
        });

    app.use('/rooms', roomsRouter);
}
