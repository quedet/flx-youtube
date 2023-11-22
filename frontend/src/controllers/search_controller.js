import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = ['results'];
    static values = {
        query: String,
        url: String,
    };

    queryValueChanged(query, oldVal) {
        console.log(query, oldVal);
    }
}