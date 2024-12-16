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
        this.set_substate(stage);    
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
}

class Zone{
    constructor(scanned){
        this.scanned = scanned;
        this.server_data = null;
        this.get_info_from_server().then();
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
        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    get_scanned(){
        return this.scanned;
    }

    reset_scanned(scanned){
        this.scanned = scanned;
        this.get_info_from_server().then();
    }
}

class Product{
    constructor(scanned){
        this.scanned = scanned;
        this.server_data = null;
        this.get_info_from_server().then();
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
        } catch (error) {
            console.error("Error calling the controller:", error);
        }
    }

    get_scanned(){
        return this.scanned;
    }

    reset_scanned(scanned){
        this.scanned = scanned;
        this.get_info_from_server().then();
    }

    get_counted(){
        return this.counted;
    }

    set_counted(counted){
        this.counted = counted;
    }

    async send_counted(){
        try {
            // Make a fetch request to your controller
            const response = await fetch("/count_product", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest", // Indicates an AJAX request
                },
                body: JSON.stringify({
                    product: this.scanned,
                    counted: this.counted,
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