
/** @odoo-module **/

import core from 'web.core';



const { Component } = owl;
const { useRef, useState, onMounted } = owl.hooks;


class ScanLog {
    constructor(timestamp, code, status) {
        this._timestamp = timestamp; // Use private-like naming for properties
        this._code = code;
        this._status = status;
    }

    // Getter and setter for timestamp
    get timestamp() {
        return this._timestamp;
    }

    set timestamp(value) {
        this._timestamp = value;
    }

    // Getter and setter for code
    get code() {
        return this._code;
    }

    set code(value) {
        this._code = value;
    }

    // Getter and setter for status
    get status() {
        return this._status;
    }

    set status(value) {
        this._status = value;
    }
}

class GuideScanner extends Component {

    barcodeInput = useRef('barcode');
    container = useRef('container');
    state = useState({
        log: []
    })
    setup() {
        onMounted(() => {
            this.focus_input();
        })
    }

    focus_input() {
        this.barcodeInput.el.focus()
        
    }

    async _call_sale_order(so) {
        try {
            // Make a fetch request to your controller
            const response = await fetch("/check_so", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest", // Indicates an AJAX request
                },
                body: JSON.stringify({
                    so: so,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Response from controller:", data);
        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    async _readBarcode() {
        let barcode = this.barcodeInput.el.value;
        this.barcodeInput.el.value = "";
        if (barcode.length > 1) {
            await this._call_sale_order(barcode);
        }
    }
    
}

GuideScanner.template = "wb_outs.GuideScannerTemplate"

core.action_registry.add("wb_outs.wb_outs_scan_guide", GuideScanner);
