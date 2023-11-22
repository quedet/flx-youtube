import { Controller } from "@hotwired/stimulus";
import Cookie from "js-cookie";
import * as TurboDrive from "@hotwired/turbo";

export default class extends Controller {
    static targets = ['loading', 'form', 'loadingProgress'];
    static values = {
        uploadUrl: String,
    };

    /**
     *
     * @param {Event} event
     */
    uploadVideo(event) {
        event.preventDefault();
        const csrftoken = Cookie.get('csrftoken');
        const file = event.target.files[0];
        const loadingWrapper = this.loadingTarget;
        const loadingProgress = this.loadingProgressTarget;
        const formRenderer = this.formTarget;

        if (file.type.split('/')[0] === 'video') {
            const form = new FormData();
            form.append('source', file);
            form.append('title', file.name.replace(/\.[^/.]+$/, ""));
            form.append('type', file.type);

            let url = this.uploadUrlValue;
            const xhr = new XMLHttpRequest();
            loadingWrapper.classList.remove('hidden');
            formRenderer.classList.add('hidden');

            xhr.upload.onprogress = function (e) {
                let percent_complete = (e.loaded / e.total) * 100;
                loadingProgress.style.height = percent_complete + '%';
                let percent = Math.ceil(percent_complete);
                loadingWrapper.querySelector('#progress-percent').innerHTML = `${percent}%`;

                if (percent === 100) {
                    setTimeout(() => {
                        loadingWrapper.querySelector('#progress-message').innerHTML = 'Video is processing. Please wait.';
                    }, 3000);

                    setTimeout(() => {
                        loadingWrapper.querySelector('#progress-message').innerHTML = "Almost done. Won't last long.";
                    }, 10000);
                }
            };
            xhr.open("POST", url, true);
            xhr.onreadystatechange = function () {
                console.log(xhr.readyState);

                if (xhr.readyState === XMLHttpRequest.DONE) {
                    formRenderer.reset();

                    if (xhr.status === 200) {
                        loadingWrapper.innerHTML = 'Redirecting...';
                        TurboDrive.visit(`${xhr.responseURL}${xhr.response}/`);
                    } else {
                        loadingWrapper.classList.add('hidden');
                        formRenderer.classList.remove('hidden');
                    }
                }
            };
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
            xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
            xhr.send(form);
        }
    }
}