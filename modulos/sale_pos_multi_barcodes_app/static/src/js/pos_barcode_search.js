odoo.define('sale_pos_multi_barcodes_app.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var core = require('web.core');
	var gui = require('point_of_sale.Gui');
	var QWeb = core.qweb;
	const ProductsWidget = require('point_of_sale.ProductsWidget');
	const Registries = require('point_of_sale.Registries');
	// var rpc = require('web.rpc');
	var _t = core._t;

	var list_product = [];

	models.load_models({
		model: 'product.multi.barcode',
		fields: ['multi_barcode','product_tmpl_id','product_id','product_product'],
		loaded: function(self, barcode){
			self.barcode = barcode;
			list_product.push(self.db.product_by_id);
		},
	});

	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		initialize: function (session, attributes) {
			var product_model = _.find(this.models, function(model){ return model.model === 'product.product'; });
			return _super_posmodel.initialize.call(this, session, attributes);
		},

		scan_product: function(parsed_code){
			var selectedOrder = this.get_order();
			var self = this;
			var product = this.db.get_product_by_barcode(parsed_code.base_code);
			var barcode = self.barcode;
			var product_ids = [];
			var qty;
			if (barcode){
				for (var i = 0; i < barcode.length; i++){
					if (parsed_code.base_code == barcode[i].multi_barcode){
						if (barcode[i].product_tmpl_id){
							product_ids.push(barcode[i].product_product[0])
						}
						else{
							product_ids.push(barcode[i].product_id[0]);	
						}
						product = self.db.get_product_by_id(product_ids);
					}
				}
			}				
			if(!product){
				return false;
			}
			if(parsed_code.type === 'price'){
				selectedOrder.add_product(product, {price:parsed_code.value});
			}else if(parsed_code.type === 'weight'){
				selectedOrder.add_product(product, {quantity:parsed_code.value, merge:false});
			}else if(parsed_code.type === 'discount'){
				selectedOrder.add_product(product, {discount:parsed_code.value, merge:false});
			}else{
				selectedOrder.add_product(product);
			}
			return true;
		},
	});

	const PosProductsWidget = (ProductsWidget) =>
		class extends ProductsWidget {
			constructor() {
				super(...arguments);
			}

			get productsToDisplay() {
				if (this.searchWord !== '') {
					let products;
					let qty;
					let new_barcode = [];
					var all_barcode = this.env.pos.barcode;
					let product_list = this.env.pos.db.search_product_in_category(
						this.selectedCategoryId,
						this.searchWord
					);
					for (var i = 0; i < list_product.length; i++){
						for (var k in list_product[i]){
							for (var j = 0; j < all_barcode.length; j++){
								if (all_barcode[j].product_tmpl_id){
									if (list_product[i][k]['id'] == all_barcode[j].product_product[0]){
										new_barcode.push(all_barcode[j])
									}
								}else{
									if (list_product[i][k]['id'] == all_barcode[j].product_id[0]){
										new_barcode.push(all_barcode[j])
									}
								}
							}
						}
					}
					if (new_barcode){
						for (var i = 0; i < new_barcode.length; i++){
							var Quantity = this.searchWord;
							var max = new_barcode[i].multi_barcode;
							if(max.toLowerCase().indexOf(Quantity.toLowerCase()) >= 0){
								if (new_barcode[i].product_tmpl_id){
									product_list.push(this.env.pos.db.get_product_by_id(new_barcode[i].product_product[0]))
								}
								else{
									product_list.push(this.env.pos.db.get_product_by_id(new_barcode[i].product_id[0]));
								}
							}
							else{
								qty = max;
							}
						}
					}
					return product_list
				} else {
					return this.env.pos.db.get_product_by_category(this.selectedCategoryId);
				}
			}
		}

	Registries.Component.extend(ProductsWidget, PosProductsWidget);

	return PosProductsWidget;
});
