import { Controller } from "@hotwired/stimulus";
import debounce from "../helpers/index";

export default class extends Controller {
    static targets = ['input'];

    connect() {
        if (this.inputTargets) {
            this.inputTargets.forEach(element => {
               element.addEventListener("input", this.onInputChange);
            });
        }
    }

    disconnect() {
        if (this.inputTargets) {
            this.inputTargets.forEach(element => {
               element.removeEventListener("input", this.onInputChange);
            });
        }
    }

    onInputChange = debounce(() => {
        this.loadRequest();
    }, 500);

    loadRequest() {
        this.element.requestSubmit();
    }

    fetchRequest(event) {
        event.preventDefault();
        event.detail.fetchOptions.headers['Accept'] = 'text/vnd.turbo-stream.html';
        event.detail.resume();
    }
}