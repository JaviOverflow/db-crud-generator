var db = require('./../pg_db_adapter');
var express = require('express');

module.exports = function(app) {
    var bookingsRouter = express.Router();

    bookingsRouter.route('')

        .get(function(request, response) {
            db.fetchListAndReturn('get_all_booking', [], response);
        })

        .post(function(request, response) {
            var body = request.body;
            var params = [
                body['client_id'],
                body['booking_room_id'],
                body['adult_amount'],
                body['kid_amount'],
                body['start_date'],
                body['end_date']
            ];
            db.fetchItemAndReturn('post_booking', params, response);
        });

    bookingsRouter.route('/:id')

        .get(function(request, response) {
            var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('get_one_booking', params, response);
        })

        .put(function(request, response) {
            var body = request.body;
            var params = [
                body['id'],
                body['client_id'],
                body['booking_room_id'],
                body['adult_amount'],
                body['kid_amount'],
                body['start_date'],
                body['end_date']
            ];
            db.fetchItemAndReturn('put_booking', params, response);
        })

        .delete(function(request, response) {
             var params = [
                request.params.id
            ];
            db.fetchItemAndReturn('delete_booking', params, response);
        });

    app.use('/bookings', bookingsRouter);
}
