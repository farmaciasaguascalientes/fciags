odoo.define('pos_session_z_report_omax', function (require) {
    "use strict";

    const gui = require('point_of_sale.Gui');
    const models = require('point_of_sale.models');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const core = require('web.core');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    var QWeb = core.qweb;
        
    class PosCustomRepButton extends PosComponent {
        async onClick() {
            var self = this.env;
            var pos_session_id = self.pos.pos_session.id;
            self.pos.do_action(
                'pos_session_z_report_omax.action_report_session_z', {
                    additional_context: {active_ids: [pos_session_id]},
                });
        }
    }
    PosCustomRepButton.template = 'PosCustomRepButton';
    ProductScreen.addControlButton({
        component: PosCustomRepButton,
        condition: function () {
            return this.env.pos.config.omax_session_z_report
        },
    });
    Registries.Component.add(PosCustomRepButton);

    return PosCustomRepButton;
});
