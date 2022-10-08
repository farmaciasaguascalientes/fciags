/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';
import { _t } from 'web.core';


patch(BarcodePickingModel.prototype, 'sale_pos_multi_barcodes_app', {
    async processBarcode(barcode) {
            var result = await this.rpc('/sale_pos_multi_barcodes_app/get_specific_barcode_data_barcode',
            {
            barcode: barcode,
            });
            barcode = result
            this.actionMutex.exec(() => this._processBarcode(barcode));
    }
});