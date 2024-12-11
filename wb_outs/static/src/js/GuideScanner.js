
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
    constructor(status, response, code=null) {
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
        this.makeLoadingScreenInvisible();
    }

    waitResponse(message, status) {
        this.waiting_response = true;
        this.makeLoadingScreenVisible(message, status);
    }

    finishWaitResponse() {
        this.waiting_response = false;
        this.makeLoadingScreenInvisible();
    }

    displayMessage(message, status) {
        this.displaying_message = true;
        this.makeLoadingScreenVisible(message, status);
    }

    finishDisplayMessage(){
        this.displaying_message = false;
        this.makeLoadingScreenInvisible();
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

    getLoadingScreen() {
        return $("#loading")
    }

    makeLoadingScreenVisible(message, status) {
        this.getLoadingScreen().removeClass("none");
        this.makeDisplayMessageComponent(message, status).appendTo(this.getLoadingScreen());
    }
    
    makeLoadingScreenInvisible() {
        this.getLoadingScreen().addClass("none");
        this.getLoadingScreen().empty();
    }

    makeDisplayMessageComponent(message, status){
        let parentDiv = $("<div>").addClass("mod");
        switch (status) {
            case "waiting":
                parentDiv.addClass("waiting");
                $("<div>").addClass("loader").appendTo(parentDiv);
                break;
            case "error":
                parentDiv.addClass("error-message");
                let error_message_div_img = $("<div>").appendTo(parentDiv);
                let error_svg_str = `<svg width="250px" height="250px" viewBox="0 0 1024 1024"><path fill="#FFFFFF" d="M512 64a448 448 0 1 1 0 896 448 448 0 0 1 0-896zm0 192a58.432 58.432 0 0 0-58.24 63.744l23.36 256.384a35.072 35.072 0 0 0 69.76 0l23.296-256.384A58.432 58.432 0 0 0 512 256zm0 512a51.2 51.2 0 1 0 0-102.4 51.2 51.2 0 0 0 0 102.4z"/></svg>`;
                $(error_svg_str).appendTo(error_message_div_img);
                break;
            case "ok":
                parentDiv.addClass("ok-message");
                let ok_message_div_img = $("<div>").appendTo(parentDiv);
                let ok_message_div_img_svg_str = `<svg width="250px" height="250px" viewBox="0 0 24 24" fill="none"><path fill="white" fill-rule="evenodd" clip-rule="evenodd" d="M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12ZM16.0303 8.96967C16.3232 9.26256 16.3232 9.73744 16.0303 10.0303L11.0303 15.0303C10.7374 15.3232 10.2626 15.3232 9.96967 15.0303L7.96967 13.0303C7.67678 12.7374 7.67678 12.2626 7.96967 11.9697C8.26256 11.6768 8.73744 11.6768 9.03033 11.9697L10.5 13.4393L12.7348 11.2045L14.9697 8.96967C15.2626 8.67678 15.7374 8.67678 16.0303 8.96967Z"/></svg>`;
                $(ok_message_div_img_svg_str).appendTo(ok_message_div_img);
                break;
            default:
                break;
        }
        $("<h3>").text(message).appendTo(parentDiv);

        return parentDiv;
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
            this.state.app_state.makeLoadingScreenVisible(
                "Esperando respuesta del servidor...",
                "waiting"
            );   
            this.state.app_state.finishedInit();
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
            this.state.data_response = await response.json();
            this.state.response = new Response(
                this.state.data_response.result.status,
                this.state.data_response.result,
                this.state.data_response.code ? this.state.data_response.code : null
            );
        } catch (error) {
            console.error("Error calling the controller:", error);
            this.state.app_state.displayMessage(
                `Error al buscar el pedido, contacta al equipo de desarrollo ${error}`,
                "error"
            );
            setTimeout(() => {
                this.state.app_state.finishDisplayMessage();
            }, 1500);
           
        }
    }

    async _readBarcode() {
        let barcode = this.barcodeInput.el.value;
        this.barcodeInput.el.value = "";
        if (barcode.length > 1) {
            this.state.app_state.waitResponse(
                "Esperando respuesta del servidor...",
                "waiting"
            );
            await this._call_sale_order(barcode);
            this.state.app_state.finishWaitResponse();

            this.state.app_state.displayMessage(
                `${this.state.response.message} ${barcode}`,
                this.state.response.isSuccess() ? "ok" : "error"
            );
            setTimeout(() => {
                this.state.app_state.finishDisplayMessage();
            }, 1500);

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
    
}

GuideScanner.template = "wb_outs.GuideScannerTemplate"

core.action_registry.add("wb_outs.wb_outs_scan_guide", GuideScanner);
