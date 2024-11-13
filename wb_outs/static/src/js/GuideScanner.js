
/** @odoo-module **/

/*const { Component, xml } = owl;

odoo.define('wb_outs.wb_outs_scan_guide', function (require) {
    "use strict";

    const core = require('web.core');
    const QWeb = core.qweb;

    class GuideScanner extends Component {
        static template = xml`<h1>Guide Scanner</h1>`
        setup() {
            console.log(QWeb.templates)
            console.log("AAAAAA");
        }
    }


    return GuideScanner;
});
*/
import core from 'web.core';

const { Component } = owl;
class GuideScanner extends Component {
    setup() {
        console.log("AAAAAA");
    }
}

GuideScanner.template = "wb_outs.GuideScannerTemplate"

core.action_registry.add("wb_outs.wb_outs_scan_guide", GuideScanner);
