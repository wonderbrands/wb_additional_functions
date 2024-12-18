
/** @odoo-module **/

import core from 'web.core';

const { Component } = owl;
const { useRef, useState, onMounted } = owl.hooks;

class CycleCount extends Component {
    barcodeZoneInput = useRef('zonebarcode');
    barcodeProductInput = useRef('productbarcode');
    qtyInput = useRef('qty');

    state = useState({
        app_state: new AppState(),
        zone: new Zone(),
        product: new Product(),
        render_components: new RenderComponents(),
        zone_searchbar: new SearchBar(),
        product_searchbar: new SearchBar(),
        log_writer: new WriteLog(),
        active_input: null
    })

    setup() {
        onMounted(() => {
            this.state.app_state.done_waiting_server();
            this.state.app_state.waitZoneScan();
            this.state.render_components.appIsWaitingZone();
            this.barcodeZoneInput.el.focus();
            this.active_input = this.barcodeZoneInput;
        })
    }

    focus_active(){
        this.active_input.el.focus();
    }

    qtyIsUnsignedInteger(){
        this.qtyInput.el.value = this.qtyInput.el.value.replace(/[^0-9]/g, '');
    }

    async confirmQty(){ 
        if (this.qtyInput.el.value == "" || this.qtyInput.el.value == "0") {
            this.state.render_components.displayModal(
                "error",
                "No has introducido ninguna cantidad",
                null,
                null,
                null,   
                null,
                1700
            );   
        } else {
            localStorage.setItem("activeProductBarcode", false);
            this.state.render_components.displayModal(
            "confirmation",
            `¿Deseas introducir 
            ${this.qtyInput.el.value} de 
            "${this.state.product.server_data.result.name}"
            a la zona ${this.state.zone.server_data.result.name}?`,
            true,
            this.qtyInput,
            {
                state: "success",
                zone: this.state.zone.server_data.result.zone,
                scanned: this.state.product_searchbar.get_term(),
                product: this.state.product.server_data.result.product,
                counted: this.qtyInput.el.value
            },
            this.state.log_writer
        );

        this.barcodeProductInput.el.value = "";
        this.qtyInput.el.value = "";

        }
        if (!localStorage.getItem("activeProductBarcode")) {
            this.barcodeProductInput.el.classList.remove("invisible")
            this.active_input = this.barcodeProductInput
        } else {
            this.active_input = this.qtyInput
        }

        this.active_input.el.focus();
        
    }

    async zoneBarcodeSuccess(){
        this.state.app_state.done_waiting_server();
        this.state.render_components.appIsScanningSKU();
        this.barcodeZoneInput.el.className += " invisible"
        this.barcodeProductInput.el.classList.remove("invisible")
        this.barcodeProductInput.el.focus();
        this.active_input = this.barcodeProductInput
        this.state.render_components.insertZone(
            this.state.zone.server_data.result.name,
            [
                this.barcodeZoneInput,
                this.barcodeProductInput,
                this.qtyInput,
            ]
        );
    }

    async productBarcodeSuccess(){
        this.state.app_state.done_waiting_server();
        this.state.render_components.appIsInputingQty();
        this.barcodeProductInput.el.className += " invisible"
        this.qtyInput.el.classList.remove("invisible")
        $("#count_button").removeClass("invisible")
        this.qtyInput.el.focus();
        this.active_input = this.qtyInput
        this.state.render_components.insertProduct(
            this.state.product.server_data.result.name,
            this.state.product.server_data.result.SKU,
            this.state.product.server_data.result.barcode,
            [
                this.barcodeProductInput,
                this.qtyInput,
            ]
        );
    }

    async _readZoneBarcode() {
        let zoneBarcode = this.state.zone_searchbar.disposeIfOneChar(this.barcodeZoneInput.el.value);
        this.state.zone.reset_scanned(zoneBarcode);
        if(!this.state.zone_searchbar.is_empty()){
            this.state.app_state.is_waiting_server()
            await this.state.zone.get_info_from_server();
            this.barcodeZoneInput.el.value = ""
            if (this.state.zone.server_data.result.status=="success") {
                await this.zoneBarcodeSuccess();
            } else{
                this.state.render_components.displayModal(
                    "error",
                    `No se ha encontrado la ubicación:  ${this.state.zone_searchbar.get_term()}`,
                    null,
                    null,
                    null,
                    null,
                    1700
                )
                this.state.log_writer.set_params(
                    {
                        state: "no_stock_location",
                        scanned: this.state.zone_searchbar.get_term()
                    }
                );
                await this.state.log_writer.write_log();
                this.barcodeZoneInput.el.value = ""
            }
        } else {
            this.barcodeZoneInput.el.value = "";
        }  
    }   
    
    async _readProductBarcode() {
        let productBarcode = this.state.product_searchbar.disposeIfOneChar(this.barcodeProductInput.el.value);
        this.state.product.reset_scanned(productBarcode);
        if(!this.state.product_searchbar.is_empty()){
            this.state.app_state.is_waiting_server()
            await this.state.product.get_info_from_server();
            if (this.state.product.server_data.result.status=="success") {
                await this.productBarcodeSuccess();
            } else {
                this.state.render_components.displayModal(
                    "error",
                    `No se ha encontrado el producto:  ${this.state.product_searchbar.get_term()}`,
                    null,
                    null,
                    null,
                    null,
                    1700
                )
                this.state.log_writer.set_params(
                    {
                        state: "product_not_exist",
                        zone: this.state.zone.server_data.result.zone,
                        scanned: this.state.product_searchbar.get_term(),
                    }
                );
                await this.state.log_writer.write_log();
                this.barcodeProductInput.el.value = ""
            }
            
        } else {
            this.barcodeProductInput.el.value = "";
        }  
    }

    
}

CycleCount.template = "wb_cycle_count.CycleCountTemplate"

core.action_registry.add("wb_cycle_count.wb_cycle_count_scan", CycleCount);
