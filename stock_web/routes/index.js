var express = require('express');
var router = express.Router();
var resources = require('../resources');

/* GET home page. */
router.get('/', function(req, res, next) {
    var limit = req.query['limit'] || 50;

    var db = require('../models/db');
    db.get_funds(limit, function(err, funds) {
        res.render('index', {
            title: 'Stock Fund',
            funds: funds,
            resources: resources,
        });
    });
});


module.exports = router;
