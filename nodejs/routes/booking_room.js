var db = require('./../pg_db_adapter');
var express = require('express');

module.exports = function(app) {
    var booking_roomsRouter = express.Router();

    booking_roomsRouter.route('')

        .get(function(request, response) {
            db.fetchListAndReturn('get_all_booking_room', [], response);
        })

        .post(function(request, response) {
            var body = request.body;
            var params = [
                body['id_booking'],
                body['id_room']
            ];
            db.fetchItemAndReturn('post_booking_room', params, response);
        });

    booking_roomsRouter.route('/:id')

        .get(function(request, response) {
            var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('get_one_booking_room', params, response);
        })

        .put(function(request, response) {
            var body = request.body;
            var params = [
                body['id'],
                body['id_booking'],
                body['id_room']
            ];
            db.fetchItemAndReturn('put_booking_room', params, response);
        })

        .delete(function(request, response) {
             var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('delete_booking_room', params, response);
        });

    app.use('/booking_rooms', booking_roomsRouter);
}
