import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ['radio'];

    connect() {
        console.log(this.radioTargets);
    }

    check(e) {
        let target = e.currentTarget;
        let parent = target.parentNode;

        this.radioTargets.forEach(element => {
            element.parentNode.classList.remove("checked");
        });

        if (target.checked) {
            parent.classList.add("checked");
        }
    }
}