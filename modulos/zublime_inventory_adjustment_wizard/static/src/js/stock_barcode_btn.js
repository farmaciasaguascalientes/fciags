odoo.define('zublime_stock.InventoryReportListControllerBarcode', function (require) {
    "use strict";

var ListController = require('web.ListController');
const viewRegistry = require('web.view_registry');
var InventoryReportListView = require('stock.InventoryReportListView');
var SingletonListRenderer = require('stock.SingletonListRenderer');
var InventoryReportListController = require('stock.InventoryReportListController');
var SingletonListController = require('stock.SingletonListController');
var StockSingletonListView = require('stock.SingletonListView')

var SingletonListControllerStock = SingletonListController.extend({
    init: function (parent, model, renderer, params) {
        this.context = renderer.state.getContext();
        return this._super.apply(this, arguments);
    },
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

        var handle = this.model.get(this.handle);
        var similarRecords = findSimilarRecords(handle);

        if (similarRecords.length > 1) {
            console.log(similarRecords)
            this._onOpenWizardStock(similarRecords);
            this.reload();
            return Promise.reject();
        }
        else {
            return this._super.apply(this, arguments);
        }
    },


    _onOpenWizardStock: function (similarRecords) {
        this.do_action({
            name: 'Cantidades Contadas',
            res_model: 'message.stock.barcode',
            views: [[false, 'form']],
            target: 'new',
            type: 'ir.actions.act_window',
            context:similarRecords,
        });
    },
});

var SingletonListView = StockSingletonListView.extend({
    config: _.extend({}, StockSingletonListView.prototype.config, {
        Controller: SingletonListControllerStock,
    }),
});

viewRegistry.add('singleton_list', SingletonListView);

return SingletonListView;
});
