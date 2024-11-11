/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class GuideScanner extends Component {
    static template = "wb_outs.GuideScannerTemplate";

    constructor() {
        super(...arguments); 
        this.message = "Welcome to Guide Scanning!";
        console.log(this.message);
    }
}

registry.category("actions").add("action_client_wb_outs_scan_guide", GuideScanner);

export default GuideScanner;
