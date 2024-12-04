
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

class ScanLogs {
    constructor() {
        this._logs = [];
    }

     addLog(log) {
        if (this._logs.length >= 5) {
            this._logs.pop();
        }
        this._logs.unshift(log);
    }

    get logs() {
        return this._logs;
    }
}

class Response {
    constructor(status, response) {
        this._status = status;
        if (status === "error") {
            this._message = response.error_description;    
        } 
        else if (status === "success") {
            this._message = response.description;
            this.so = response.so
        }
    }

    get status() {
        return this._status;
    }

    get message() {
        return this._message;
    }

    set status(value) {
        this._status = value;
    }

    set message(value) {
        this._message = value;
    }

    isError() {
        return this._status === "error";
    }

    isSuccess() {
        return this._status === "success";
    }
}

class AppState {
    constructor() {
        this.waiting_init = true;
        this.waiting_response = false;
        this.displaying_message = false;
    }

    finishedInit() {
        this.waiting_init = false;
    }

    waitResponse() {
        this.waiting_response = true;
    }

    finishWaitResponse() {
        this.waiting_response = false;
    }

    displayMessage(){
        this.displaying_message = true;
    }

    finishDisplayMessage(){
        this.displaying_message = false;
    }

    isAppWaitingInit() {
        return this.waiting_init;
    }

    isAppWaitingResponse() {
        return this.waiting_response;
    }

    isAppDisplayingMessage() {
        return this.displaying_message;
    }

    showModal() {
        return this.isAppWaitingInit() || this.isAppWaitingResponse() || this.isAppDisplayingMessage();
    }

    isAppWaiting(){
        return this.isAppWaitingInit() || this.isAppWaitingResponse();
    }
}

class GuideScanner extends Component {

    barcodeInput = useRef('barcode');
    container = useRef('container');
    state = useState({
        log: new ScanLogs(),
        data_response: null,
        app_state: new AppState(),
        response: null
    })
    setup() {
        onMounted(() => {
            this.state.app_state.finishedInit();
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

            this.state.data_response = await response.json();
            this.state.app_state.displayMessage();
            this.state.app_state.waitResponse();
            this.state.response = new Response(
                this.state.data_response.result.status,
                this.state.data_response.result
            );
            this.state.app_state.finishWaitResponse()
        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    async _readBarcode() {
        let barcode = this.barcodeInput.el.value;
        this.barcodeInput.el.value = "";
        if (barcode.length > 1) {
            this.state.app_state.waitResponse();
            await this._call_sale_order(barcode);
            setTimeout(() => {
                this.state.app_state.finishDisplayMessage();
            }, 1500);
        }
        if (this.state.response.isSuccess()) {
            const date = new Date();
            const timestamp = date.toLocaleString();
            this.state.log.addLog(
                new ScanLog(
                    timestamp, 
                    barcode, 
                    this.state.response.isSuccess()
                )
            );
        }
    }
    
}

GuideScanner.template = "wb_outs.GuideScannerTemplate"

core.action_registry.add("wb_outs.wb_outs_scan_guide", GuideScanner);
