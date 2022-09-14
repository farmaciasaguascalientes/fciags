odoo.define('zublime_stock.SingletonListController', function (require) {
"use strict";

var core = require('web.core');
var SingletonListController = require('stock.SingletonListController');

var _t = core._t;

var SingletonListController = InventoryReportListController.extend({

    _confirmSave: function (id) {
        var newRecord = this.model.localData[id];
        var model = newRecord.model;
        var res_id = newRecord.res_id;

        var findSimilarRecords = function (record) {
            if ((record.groupedBy && record.groupedBy.length > 0) || record.data.length) {
                var recordsToReturn = [];
                for (var i in record.data) {
                    var foundRecords = findSimilarRecords(record.data[i]);
                    recordsToReturn = recordsToReturn.concat(foundRecords || []);
                }
                return recordsToReturn;
            } else {
                if (record.res_id === res_id && record.model === model) {
                    if (record.count === 0){
                        return [record];
                    }
                    else if (record.ref && record.ref.indexOf('virtual') !== -1) {
                        return [record];
                    }
                }
            }
        };
    },

return SingletonListController;

});
