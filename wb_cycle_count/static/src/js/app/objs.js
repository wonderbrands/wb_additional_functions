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

    displayModal(type, message, active_input = null, confirmation = null, data_confirmation=null, log=null, timeout = null){
        let container = $(".app-container");
        let modal = $("<div class='modal'></div>");
        let subscreen = $("<div class='subscreen'></div>");
        modal.append(subscreen);
        subscreen.append(`<h1>${message}</h1>`);
        switch(type){
            case "confirmation":
                subscreen.addClass("confirmation");
                subscreen.append("<button id='confirm'>Confirmar</button>");
                subscreen.append("<button id='cancel'>Cancelar</button>");
                break;

            case "error":
                subscreen.addClass("error");
                break;
        }

        if(confirmation){
            let button = modal.find("#confirm");
            button.on("click", () => {
                log.set_params(data_confirmation);
                log.write_log();
                modal.remove();
                this.countedQty();
            });
            button.on("click", () => {
                modal.remove();
                
            })

            modal.find("#cancel").on("click", () => {
                modal.remove();
                active = true
            })

        }

        container.append(modal);
        if(timeout){
            setTimeout(() => {
                modal.remove();
            }, timeout);
        }
    }

    appIsWaitingZone(){
        let root = this.getRoot();
        root.empty();
        root.append("<h1> ¡Bienvenido! </h1>");
        root.append("<h2> Ya puedes empezar a escanear.</h2>");
        root.append("<h3 id='instruction1'> Por favor, escanea una de zonas del almacen. </h3>");
    }

    appIsScanningSKU(){
        let root = this.getRoot();
        root.append("<h3 id='instruction2'> Ahora, escanea el código de barras de un producto. </h2>");
        $('#instruction1').addClass('passed');
    }

    appIsInputingQty(){
        let root = this.getRoot();
        root.append("<h3 id='instruction3'> Introduce la cantidad de producto que tienes en inventario para esta zona</h3>");
        $('#instruction2').addClass('passed');
    }

    countedQty(){
        $('#instruction2').removeClass('passed');
        $("#instruction3").addClass('invisible');
        $("#qty").addClass('invisible');
        $("#count_button").addClass('invisible');

    }

    getInformationZone(){
        return $("#info")
    }

    insertZone(zone, inputs){
        let info = this.getInformationZone();
        let zonediv =  $("<div id='zone' class='zone_container'></div>")
        zonediv.append(`<h2>Ubicación: ${zone}</h2>`)
        zonediv.append(`<button id='reset_zone'>Cambiar de ubicación</button>`)
        info.append(zonediv);
        $("#reset_zone").on("click", () => {
            info.children().remove()
            $('#instruction1').removeClass('passed');
            $('#instruction1').removeClass('invisible');
            $('#instruction2').remove();
            $("#instruction3").remove();
            $("#qty").addClass('invisible');
            $("#count_button").addClass('invisible');
            inputs.forEach(input => {
                input.el.value = "";
                input.el.className+=(" invisible");
            });
            inputs[0].el.classList.remove("invisible");
            inputs[0].el.focus();
        })
    }

    insertProduct(product, sku, barcode, inputs){
        let info = this.getInformationZone();
        let productdiv =  $("<div id='product' class='product_container'></div>")
        let productinfodiv = $("<div id='product_info' class='product_info'></div>")
        productinfodiv.append(`<h2>Producto: ${product}</h2>`)
        productinfodiv.append(`<h2>SKU: ${sku}</h2>`)
        productinfodiv.append(`<h2>Codigo de barras: ${barcode}</h2>`)
        productdiv.append(productinfodiv)
        productdiv.append(`<button id='reset_product'>Cambiar de producto</button>`)
        info.append(productdiv);

        $("#reset_product").on("click", () => {
            productdiv.remove()
            $('#instruction2').removeClass('passed');
            $('#instruction2').removeClass('invisible');
            $('#instruction3').remove()
            $("#qty").addClass('invisible');
            $("#count_button").addClass('invisible');
            inputs.forEach(input => {
                input.el.value = "";
                input.el.className+=(" invisible");
            });
            inputs[0].el.classList.remove("invisible");
            inputs[0].el.focus();
        })
    }
}