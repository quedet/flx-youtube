import { Controller } from "@hotwired/stimulus";
import debounce from "../helpers/index";

export default class extends Controller {
    static targets = ['input'];

    connect() {
        if (this.hasInputTarget) {
            this.inputTarget.addEventListener("input", this.onInputChange);
        }
    }

    disconnect() {
        if (this.hasInputTarget) {
            this.inputTarget.removeEventListener("input", this.onInputChange);
        }
    }

    onInputChange = debounce(() => {
        this.loadResults();
    }, 500);

    loadResults() {
        this.element.requestSubmit();
    }

    fetchRequest(event) {
        event.preventDefault();
        event.detail.fetchOptions.headers['Accept'] = 'text/vnd.turbo-stream.html';
        event.detail.resume();
    }
}