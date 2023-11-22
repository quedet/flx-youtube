import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static values = {
        url: String,
        page: Number,
        lazy: {
            default: true,
            type: Boolean
        }
    };

    static targets = ['renderer'];


    changePageNumber(event) {
        this.pageValue = event.currentTarget.dataset.page;
        this.lazyValue = false;

        if (event.currentTarget.dataset.page !== '1')
            event.currentTarget.remove();
    }

    pageValueChanged(value, oldValue) {
        if (this.lazyValue) {
            return false;
        }
        if(value !== oldValue) {
            let url = this.urlValue + `?page=${value}`;

            const xhr = new XMLHttpRequest();
            let content = this.rendererTarget;

            xhr.open("GET", url, true);

            // xhr.onload = function (e) {
            //     if (e.lengthComputable) {
            //         let percent = (e.loaded / e.total) * 100;
            //         const loader = `<div id="loader" style="height: 2px; width: ${percent}%; background:#0000ff;" class="animate-pulse">${percent}</div>`;
            //
            //         if(value === 1)
            //             content.innerHTML = loader;
            //         else
            //             content.insertAdjacentHTML('beforeend', loader);
            //
            //     } else {
            //         console.log(`${e.loaded} bytes`);
            //     }
            // };

            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    if (xhr.responseText === '') {
                        content.innerHTML = "No Contents";
                    } else {
                        if(value === 1) {
                            content.innerHTML = xhr.responseText;
                        } else {
                            content.insertAdjacentHTML('beforeend', xhr.responseText);
                        }
                    }
                }
            };

            xhr.send();
        }
    }

    load() {
        let url = this.urlValue;

        const xhr = new XMLHttpRequest();
        let content = this.rendererTarget;

        xhr.open("GET", url, true);

        // xhr.onload = function (e) {
        //     if (e.lengthComputable) {
        //         let percent = (e.loaded / e.total) * 100;
        //         console.log(percent);
        //     } else {
        //         console.log(`${e.loaded} bytes`);
        //     }
        // };

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                if (xhr.responseText === '') {
                    content.innerHTML = "No Contents";
                } else {
                    content.insertAdjacentHTML('beforeend', xhr.responseText);
                }
            }
        };

        xhr.send();
    }
}
