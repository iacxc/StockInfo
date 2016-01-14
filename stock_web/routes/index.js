var express = require('express');
var router = express.Router();
var url = require('url');
var util = require('util');

/* GET home page. */
router.get('/', function(req, res, next) {
    var url_parts = url.parse(req.url, true);
    var limit = url_parts.query['limit'] || 50;

    var db = require('../models/db');
    db.get_funds(limit, function(err, funds) {
        res.render('index', {
            title: 'Stock Fund',
            funds: funds,
        });
    });
});


module.exports = router;
