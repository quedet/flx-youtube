import { Controller } from "@hotwired/stimulus";
import * as Cropper from "cropperjs";
import "cropperjs/dist/cropper.min.css";
import Cookie from "js-cookie";
import * as Turbo from '@hotwired/turbo';

export default class extends Controller {
    static targets = ['preview'];
    static values = {
        url: String,
        ratio: {
            default: 'square',
            type: String
        }
    };

    connect() {
        let ratio = this.ratioValue === 'square' ? 1 / 1 : 16 / 3;

        const img = this.previewTarget.querySelector('.preview-img');
        this.cropper = new Cropper(img, {
            aspectRatio: ratio,
            background: false,
            viewMode: 3,
            autoCropArea: 1
        });
    }

    sendRequest(event) {
        event.preventDefault();
        const csrftoken = Cookie.get('csrftoken');
        const crop = this.cropper.getData();

        const form = new FormData(this.element);
        form.append('cropX', crop.x);
        form.append('cropY', crop.y);
        form.append('cropWidth', crop.width);
        form.append('cropHeight', crop.height);
        form.append('type', form.get('original').type);

        const xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                Turbo.visit(this.response);
            }
        };
        xhr.open("POST", this.urlValue, true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
        xhr.send(form);
    }

    /**
     *
     * @param event
     */
    changeImage(event) {
        let file = event.target.files[0];
        if (file) {
            this.previousFile = file;
        } else {
            file = this.previousFile;
        }
        const reader = new FileReader();
        reader.readAsDataURL(file);
        const preview =  this.previewTarget;
        const cropper = this.cropper;
        reader.onloadend = function () {
            const img = preview.querySelector('.preview-img');
            img.setAttribute('src', reader.result);
            cropper.replace(reader.result);
        };
    }
}