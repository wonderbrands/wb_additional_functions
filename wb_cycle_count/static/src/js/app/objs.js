class SearchBar{
    constructor(term){
        this.term = term;
    }
    
    get_term(){
        return this.term;
    }

    set_term(term){
        this.term = term;
    }

    clear_term(){
        this.term = "";
    }

    is_empty(){
        return this.term == "";
    }

    disposeIfOneChar(term){
        this.set_term(term)
        if(this.term.length == 1){
            this.clear_term();
        } 
        return this.term;
    }
}

class AppState{
    constructor(){
        this.current_state = "waiting_server";
        this.substate = null;
        this.message_displayed = null;
    }

    set_state(state){
        this.current_state = state;
    }

    get_state(){
        return this.current_state;
    }

    is_waiting_server(){
        return this.current_state == "waiting_server";
    }

    done_waiting_server(stage = null){
        this.current_state = "available";
    }

    get_substate(){
        return this.substate;
    }

    set_substate(state){
        this.substate = state;
    }

    get_message_displayed(){
        return this.message_displayed;
    }

    set_message_displayed(message){
        this.message_displayed = message;
    }

    pop_error(error){
        console.error(error);
        this.set_state("error");
        this.set_message_displayed(error);
    }

    waitZoneScan(){
        this.set_state("available");
        this.set_substate("waiting_zone");
    }
}

class Zone{
    constructor(scanned){
        this.scanned = scanned;
        this.server_data = null;
    }

    async get_info_from_server(){
        try {
            // Make a fetch request to your controller
            const response = await fetch("/check_zone", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest", // Indicates an AJAX request
                },
                body: JSON.stringify({
                    zone: this.scanned,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            this.server_data = await response.json();
            

        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    get_scanned(){
        return this.scanned;
    }

    reset_scanned(scanned){
        this.scanned = scanned;
    }
}

class Product{
    constructor(scanned){
        this.scanned = scanned;
        this.server_data = null;
    }

    async get_info_from_server(){
        try {
            // Make a fetch request to your controller
            const response = await fetch("/check_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest", // Indicates an AJAX request
                },
                body: JSON.stringify({
                    product: this.scanned,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            this.server_data = await response.json();
            

        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    get_scanned(){
        return this.scanned;
    }

    reset_scanned(scanned){
        this.scanned = scanned;
    }

    get_counted(){
        return this.counted;
    }

    set_counted(counted){
        this.counted = counted;
    }
}

class WriteLog{
    constructor(state, zone=null, product=null, counted=null, scanned=null){
        this.state = state;
        this.zone = zone;
        this.product = product;
        this.counted = counted;    
        this.scanned = scanned;
    }

    get_scanned(){
        return this.scanned;
    }

    set_scanned(scanned){
        this.scanned = scanned;
    }
    get_state(){
        return this.state;
    }

    get_zone(){
        return this.zone;
    }

    get_product(){
        return this.product;
    }

    get_counted(){
        return this.counted;
    }

    set_state(state){
        this.state = state;
    }

    set_zone(zone){
        this.zone = zone;
    }

    set_product(product){
        this.product = product;
    }

    set_counted(counted){
        this.counted = counted;
    }

    set_params({state = null, zone = null, product = null, counted = null, scanned = null} = {}){
        this.state = state;
        this.zone = zone;
        this.product = product;
        this.counted = counted;
        this.scanned = scanned;
    }

    async write_log(){
        try {
            // Make a fetch request to your controller
            const response = await fetch("/write_count_log", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest", // Indicates an AJAX request
                },
                body: JSON.stringify({
                    state: this.state ? this.state : null,
                    zone: this.zone ? this.zone : null,
                    product: this.product ? this.product : null,
                    scanned: this.scanned ? this.scanned : null,
                    qty: this.counted ? this.counted : null
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }
}

class RenderComponents {
    constructor(){
        
    }

    getRoot(){
        return $("#root")    
    }

    appIsWaitingZone(){
        let root = this.getRoot();
        root.empty();
        root.append("<h1> ¡Bienvenido! </h1>");
        root.append("<h2> Ya puedes empezar a intoducir zonas del almacen. </h2>");
    }

    appIsScanningSKU(){
        let root = this.getRoot();
        root.empty();
        root.append("<h2> Ahora, escanea un sku </h2>");
    }

    appIsInputingQty(){
        let root = this.getRoot();
        root.append("<h2> Introduce la cantidad de estos productos que tienes en inventario en esta zona</h2>");
    }
}