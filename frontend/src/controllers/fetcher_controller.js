import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static values = {
        url: {
            type: String,
            default: null
        },
        topic: {
            type: String,
            default: 'all'
        },
        noTopic: {
            type: Boolean,
            default: false
        }
    };

    static targets = ['renderer'];

    connect() {
        let element = this.rendererTarget;
        let url = this.urlValue;
        let emptyPage = false;
        let blockRequest = false;
        let topic = null;

        if (!this.noTopicValue) {
            topic = this.topicValue;
        }

        window.addEventListener('scroll', function () {
            let page = 1;

            let margin = window.scrollY + window.innerHeight - document.documentElement.scrollHeight >= -200;

            if (margin && !blockRequest && !emptyPage) {
                blockRequest = true;
                page += 1;
                let ws_url = null;

                if (topic)
                    ws_url = url + `?topic=${topic}&page=${page}`;
                else
                    ws_url = url + `?page=${page}`;

                const xhr = new XMLHttpRequest();
                xhr.open("GET", ws_url, true);

                xhr.onprogress = function (e) {
                    if (e.lengthComputable) {
                        let percent = (e.loaded / e.total) * 100;
                        console.log(`${percent}% loaded`);
                    }
                };

                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        if (xhr.responseText === '') {
                            emptyPage = true;
                        } else {
                            element.insertAdjacentHTML("beforeend", xhr.responseText);
                            blockRequest = true;
                        }
                    }
                };

                xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
                xhr.send();
            }
        });

        const scrollEvent = new Event("scroll");
        window.dispatchEvent(scrollEvent);
    }

    topicValueChanged(value, oldValue) {
        if (value !== oldValue) {
            let page = 1;
            let ws_url = this.urlValue + `?topic=${value}&page=${page}`;
            let element = this.rendererTarget;
            element.innerHTML = "";

            const xhr = new XMLHttpRequest();
            xhr.open("GET", ws_url, true);

            xhr.onprogress = function (e) {
                if (e.lengthComputable) {
                    let percent = (e.loaded / e.total) * 100;
                    console.log(`${percent}% loaded`);
                }
            };

            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    if (xhr.responseText !== '') {
                        element.insertAdjacentHTML("beforeend", xhr.responseText);
                    }
                }
            };
            xhr.send();
        }
    }


    /**
     *
     * @param {Event} e
     */
    filterByTopics(e) {
        this.topicValue = e.currentTarget.dataset.topic;
        for (let child of e.currentTarget.parentNode.children) {
            child.classList.remove('active');
        }
        e.currentTarget.classList.add("active");
    }
}