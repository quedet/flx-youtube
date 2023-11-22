import { Modal } from "tailwindcss-stimulus-components";
import * as Turbo from '@hotwired/turbo';

export default class extends Modal {
    static targets = [...Modal.targets, ...['modalContent']];
    static values = {
        ...Modal.values,
        ...{
            url: String
        }
    };

    open(e) {
        this.loadContent();
        super.open(e);
    }

    close(e) {
        if (this.hasModalContentTarget) {
            const frame = this.modalContentTarget;
            frame.innerHTML = '';
        }
        super.close(e);
    }

    loadContent() {
        if (this.hasModalContentTarget && this.hasUrlValue) {
            const frame = this.modalContentTarget;

            let reloadFlag = false;
            if (frame.src === this.urlValue) {
                reloadFlag = true;
            }
            frame.src = this.urlValue;

            if (reloadFlag) {
                frame.reload();
            }
        }
    }

    async closeOnSuccessSubmit(event) {
        console.log("Clicked");
        if (event.detail.success) {
            const fetchResponse = event.detail.fetchResponse;
            console.log(fetchResponse);
            if(fetchResponse.succeeded && fetchResponse.redirected) {
                Turbo.visit(fetchResponse.location);
                this.close(event);
            } else {
                this.close(event);
            }
        }
    }
}