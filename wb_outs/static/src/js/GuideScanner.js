
/** @odoo-module **/

import core from 'web.core';

const { Component } = owl;
const { useRef, useState, onMounted } = owl.hooks;

class GuideScanner extends Component {

    barcodeInput = useRef('barcode');
    container = useRef('container');
    state = useState({ modal: false });
    setup() {
        onMounted(() => {
            this.focus_input();
        })
    }

    focus_input() {
        if (!this.state.modal){
            this.barcodeInput.el.focus()
        }
    }

    _readBarcode() {
        let barcode = this.barcodeInput.el.value;
        this.barcodeInput.el.value = "";
        console.log(barcode);
    }
    
    _manageCarrier(){
        this.state.modal = true
    }
}

GuideScanner.template = "wb_outs.GuideScannerTemplate"

core.action_registry.add("wb_outs.wb_outs_scan_guide", GuideScanner);
