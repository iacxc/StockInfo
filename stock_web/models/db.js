
'use strict';

var settings = require('../settings');
var sqlite3 = require('sqlite3').verbose();
var util = require('util');


exports.get_codes = function(callback) {
    var codes = [];
    var db = new sqlite3.Database(settings.dbfile, function() {
        db.all('select code from code', function(err, rows) {
            if (err) {
                callback(err);
            }
            else {
                rows.forEach(function(row) {
                    codes.push(row.code);
                });
            }
            db.close();
            callback(codes);
        });
    });
}

exports.get_funds = function(limit, callback) {
    var querystr = util.format("select code, date, fund_in, fund_out, fund_net" +
                   ", fund_net / value as percent, fund_per" +
                   ", inc_p as inc_p" +
                   " from funds a "+
                   " where date in" +
                   "    (select date from funds" +
                   "     where code=a.code" +
                   "     order by date desc" +
                   "     limit %d)" +
                   " order by code, date", limit);
    var funds = {};
    var db = new sqlite3.Database(settings.dbfile, function() {
        db.all(querystr, function(err, rows) {
            if (err) {
                callback(err);
            }
            else {
                rows.forEach(function(row) {
                    if (funds[row.code]) {
                        funds[row.code].push(row);
                    }
                    else {
                        funds[row.code] = [row];
                    }
                });
                db.close();
                callback(null, funds);
            }
        });
    });
}
