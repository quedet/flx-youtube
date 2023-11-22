import Sortable from "stimulus-sortable";

export default class extends Sortable {
    static targets = [...Sortable.targets, ...['item']];
    static values = {
        ...Sortable.values,
        ...{
            updateUrl: String,
        }
    };
    connect() {
        super.connect();
        this.linksOrder = {};
        this.linksUrl = this.updateUrlValue;
        this.linksOptions = {
            method: 'POST',
            mode: 'same-origin',
        };
    }

    async onUpdate({item: t, newIndex: a}) {
        this.itemTargets.forEach((item, index) => {
            this.linksOrder[item.dataset.id] = index;
        });

        this.linksOptions['body'] = JSON.stringify(this.linksOrder);
        fetch(this.linksUrl, this.linksOptions);

        return super.onUpdate({item: t, newIndex: a});
    }
}