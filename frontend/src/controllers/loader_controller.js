import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static values = {
        url: String,
        section: String,
        pagination: {
            default: false,
            type: Boolean
        },
        page: Number
    };

    static targets = ['renderer', 'form'];


    /**
     * @param {Event} event
     */
    requestPublish(event) {
        event.preventDefault();

        if (this.hasFormTarget) {
            this.formTarget.requestSubmit();
        }
    }

    changePageSection(event) {
        this.sectionValue = event.currentTarget.dataset.section;
        let currentUrl = this.urlValue + '?section=' + this.sectionValue;
        window.history.pushState({}, '', currentUrl);
    }

    changePageNumber(event) {
        this.pageValue = event.currentTarget.dataset.page;
        let currentUrl = this.urlValue + '?section=' + this.sectionValue + '&page=' + this.pageValue;
        window.history.pushState({}, '', currentUrl);
    }

    sectionValueChanged(value, oldValue) {
        this.pageValue = 1;

        if (value !== oldValue) {
            let url = this.urlValue + this.sectionValue + '/';

            // if (this.pageValue) {
            //     url += `?page=${this.pageValue}`;
            //     return false;
            // }

            const xhr = new XMLHttpRequest();
            let content = this.rendererTarget;

            xhr.open("GET", url, true);

            xhr.onload = function (e) {
                if (e.lengthComputable) {
                    let percent = (e.loaded / e.total) * 100;
                    console.log(percent);
                } else {
                    console.log(`${e.loaded} bytes`);
                }
            };

            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    if (xhr.responseText === '') {
                        content.innerHTML = "No Contents";
                    } else {
                        content.innerHTML = xhr.responseText;
                    }
                }
            };

            xhr.send();
        }
    }

    pageValueChanged(value, oldValue) {
        if (!this.paginationValue) {
            return false;
        }

        if(value !== oldValue) {
            let url = this.urlValue;

            if (this.hasSectionValue) {
                url += `${this.sectionValue}/`;
            }

            url += `?page=${value}`;

            const xhr = new XMLHttpRequest();
            let content = this.rendererTarget;

            xhr.open("GET", url, true);

            xhr.onload = function (e) {
                if (e.lengthComputable) {
                    let percent = (e.loaded / e.total) * 100;
                    console.log(percent);
                } else {
                    console.log(`${e.loaded} bytes`);
                }
            };

            xhr.onreadystatechange = function () {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    if (xhr.responseText === '') {
                        content.innerHTML = "No Contents";
                    } else {
                        content.innerHTML = xhr.responseText;
                    }
                }
            };

            xhr.send();
        }
    }
}
