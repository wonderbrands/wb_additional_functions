
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
        show_zone_input: true,
        show_product_input: false,
        show_product_qty: false
    })

    setup() {
        onMounted(() => {
            this.state.app_state.done_waiting_server();
            this.state.app_state.waitZoneScan();
            this.state.render_components.appIsWaitingZone();
        })
    }

    async confirmQty(){ 
        this.state.log_writer.set_params(
            {
                state: "success",
                zone: this.state.zone.server_data.result.zone,
                scanned: this.state.product_searchbar.get_term(),
                product: this.state.product.server_data.result.product,
                counted: this.qtyInput.el.value
            }
        );
        await this.state.log_writer.write_log();
    }

    async _readZoneBarcode() {
        let zoneBarcode = this.state.zone_searchbar.disposeIfOneChar(this.barcodeZoneInput.el.value);
        this.state.zone.reset_scanned(zoneBarcode);
        if(!this.state.zone_searchbar.is_empty()){
            this.state.app_state.is_waiting_server()
            await this.state.zone.get_info_from_server();
            this.barcodeZoneInput.el.value = ""
            if (this.state.zone.server_data.result.status=="success") {
                this.state.app_state.done_waiting_server();
                this.state.render_components.appIsScanningSKU();
                this.state.show_zone_input = false;
                this.state.show_product_input = true;
            } else{
                this.state.log_writer.set_params(
                    {
                        state: "no_stock_location",
                        scanned: this.state.zone_searchbar.get_term()
                    }
                );
                await this.state.log_writer.write_log();
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
                this.state.app_state.done_waiting_server();
                this.state.show_product_input = false;
                this.state.show_product_qty = true;
                this.state.render_components.appIsInputingQty();
            } else {
                this.state.log_writer.set_params(
                    {
                        state: "product_not_exist",
                        zone: this.state.zone.server_data.result.zone,
                        scanned: this.state.product_searchbar.get_term(),
                    }
                );
                await this.state.log_writer.write_log();
            }
            
        } else {
            this.barcodeProductInput.el.value = "";
        }  
    }

    
}

CycleCount.template = "wb_cycle_count.CycleCountTemplate"

core.action_registry.add("wb_cycle_count.wb_cycle_count_scan", CycleCount);
