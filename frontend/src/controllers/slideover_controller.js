import { Slideover } from "tailwindcss-stimulus-components";

export default class extends Slideover {
    static targets = [...Slideover.targets];
    static values = {
        ...Slideover.values,
    };

    toggle(e) {
        super.toggle(e);
        document.body.classList.toggle("overflow-hidden");
    }

    hide(e) {
        super.hide(e);
    }

    show(e) {
        super.show(e);
    }
}