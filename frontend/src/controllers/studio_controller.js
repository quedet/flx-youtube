import { Controller } from "@hotwired/stimulus";
import { connectStreamSource, disconnectStreamSource } from "@hotwired/turbo";
import ReconnectingWebSocket from "reconnecting-websocket";
import Cookie from "js-cookie";

import * as TurboDrive from "@hotwired/turbo";
import debounce from "../helpers";

export default class extends Controller {
    static targets = ['VideoEditionForm', 'VideoEditionInputField',
        'VideoEditionSubmitButton', 'VideoEditionTopicsList', 'VideoEditionThumbnails'];

    static values = {
        socketUrl: String,
        uploadUrl: String,
    };

    connect() {
        const ws_url = this.socketUrlValue;
        this.source = new ReconnectingWebSocket((window.location.protocol === 'http:' ? 'ws': 'wss') + '://' + window.location.host + ws_url);
        connectStreamSource(this.source);

        if (this.hasVideoEditionThumbnailsTarget) {
            this.generateThumbnails();
        }

        if (this.hasVideoEditionFormTarget && this.VideoEditionFormTarget.dataset.autoSave) {
            if (this.VideoEditionInputFieldTargets) {
                this.VideoEditionInputFieldTargets.forEach(element => {
                   element.addEventListener("input", this.onDraftInputChange);
                });
            }
        }
    }

    disconnect() {
        if (this.source) {
            disconnectStreamSource(this.source);
            this.source.close();
            this.source = null;
        }

        if (this.VideoEditionInputFieldTargets) {
            this.VideoEditionInputFieldTargets.forEach(element => {
               element.removeEventListener("input", this.onDraftInputChange);
            });
        }
    }

    /**
     *
     * @param {Event} event
     */
    deletePlaylist(event) {
        event.preventDefault();
        const newData = {
            action: 'delete playlist',
            data: {
                playlist_id: event.currentTarget.dataset.id
            }
        };
        this.sendData(this.source, newData);

        TurboDrive.visit(window.location.href);
    }

    /**
     *
     * @param {Event} event
     */
    setTopicItem(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'set video topic',
            data: {
                video_id: dataset.videoId,
                topic_id: dataset.topicId,
                model_name: dataset.model
            }
        };

        this.sendData(this.source, newData);
    }

    setTopicToList(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'set topic to selected list',
            data: {
                video_id: dataset.videoId,
                topic_id: dataset.topicId,
                model_name: dataset.model
            }
        };

        const data = {
            action: 'set topic to video form',
            data: {
                video_id: dataset.videoId,
                topic_id: dataset.topicId,
                model_name: dataset.model
            }
        };

        setTimeout(() => {
            this.sendData(this.source, newData);
            this.sendData(this.source, data);
        }, 500);
    }

    removeTopicItem(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'remove video topic',
            data: {
                video_id: dataset.videoId,
                topic_id: dataset.topicId,
                model_name: dataset.model
            }
        };

        const data = {
            action: 'remove topic to video form',
            data: {
                video_id: dataset.videoId,
                topic_id: dataset.topicId,
                model_name: dataset.model
            }
        };

        this.sendData(this.source, newData);
        this.sendData(this.source, data);
    }

    /**
     * @param {Event} event
     */
    showLinkForm(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'show link form',
            data: {
                channel_id: dataset.channelId,
            }
        };
        this.sendData(this.source, newData);

        event.currentTarget.classList.add('hidden');
    }

    /**
     * @param {Event} event
     */
    CloseLinkForm(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'Close Link Form',
            data: {
                channel_id: dataset.channelId,
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * @param {Event} event
     */
    addLink(event) {
        event.preventDefault();
        const dataset = event.currentTarget.dataset;
        const form = new FormData(event.currentTarget);

        const newData = {
            action: 'add link',
            data: {
                channel_id: dataset.channelId,
                title: form.get('title'),
                url: form.get('url')
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * @param {Event} event
     */
    deleteLink(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'Show Link Form',
            data: {
                channel_id: dataset.channelId,
                link_id: dataset.linkId,
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * @param {WebSocket} websocket
     * @param {Object} data
     * @return {void}
     */
    sendData(websocket, data) {
        websocket.send(JSON.stringify(data));
    }


    /**
     *
     * @return {void}
     */
    videoContentChanged() {
        let target = this.VideoEditionFormTarget;
        const form = new FormData(target);

        const newData = {
            action: 'content changed',
            data: {
                id: target.dataset.videoId,
                title: form.get('title').trim(),
                description: form.get('description').trim(),
                topics: form.getAll('topics'),
                playlist: form.get('playlist')
            }
        };

        if (form.get('thumbnail').name !== '' && form.get('thumbnail').type.split('/')[0] === 'image') {
            newData.data['thumbnail'] = form.get('thumbnail').name;
        }

        this.sendData(this.source, newData);
    }


    generateThumbnails() {
        const xhr = new XMLHttpRequest();
        const element = this.VideoEditionThumbnailsTarget;
        const url = window.location.protocol + '//' + window.location.host + window.location.pathname + 'generate-thumbnails/';

        const csrftoken = Cookie.get('csrftoken');

        xhr.onprogress = (e) => {
          if (e.lengthComputable) {
              let percent = (e.loaded / e.total) * 100;
              console.log(percent);
          } else {
              console.log(`${e.type}: ${e.loaded} bytes transferred.`);
          }
        };

        xhr.onreadystatechange = function () {
          if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
              element.insertAdjacentHTML('beforeend', xhr.responseText);
          }
        };
        xhr.open('POST', url, true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
        xhr.send();
    }

    /**
     *
     */
    triggerSubmit() {
        this.VideoEditionFormTarget.requestSubmit();
    }

    onInputChange = debounce(() => {
        this.videoContentChanged();
    }, 500);

    onDraftInputChange = debounce(() => {
        this.triggerSubmit();
    }, 500);

    fetchRequest(event) {
        event.preventDefault();
        event.detail.fetchOptions.headers['Accept'] = 'text/vnd.turbo-stream.html';
        event.detail.resume();
    }

    /**
     *
     */
    enableFormSubmission() {
        this.VideoEditionSubmitButtonTarget.removeAttribute("disabled");
    }
}