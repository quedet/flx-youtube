import { Controller } from "@hotwired/stimulus";
import { connectStreamSource, disconnectStreamSource } from "@hotwired/turbo";
import ReconnectingWebSocket from "reconnecting-websocket";
// import debounce from "../helpers";

export default class extends Controller {
    static targets = ['searchResults', 'SearchForm'];

    static values = {
        socketUrl: String,
        enablePreviewReload: {
            type: Boolean,
            default: true
        },
        searchQuery: String
    };

    connect() {
        const ws_url = this.socketUrlValue;
        this.source = new ReconnectingWebSocket((window.location.protocol === 'http:' ? 'ws': 'wss') + '://' + window.location.host + ws_url);
        connectStreamSource(this.source);
    }

    disconnect() {
        if (this.source) {
            disconnectStreamSource(this.source);
            this.source.close();
            this.source = null;
        }
    }

    /**
     *
     * @param {Event} event
     */
    searchRequestSubmit(event) {
        event.preventDefault();

        const form = new FormData(event.target);
        const query = form.get('query');
        const url = event.target.getAttribute('action') + '?query=' + query;
        const renderer = this.searchResultsTarget;


        if (query.trim() !== '') {
            window.history.pushState({}, '', window.location.origin + window.location.pathname + '?query=' + query);
            const xhr = new XMLHttpRequest();

            xhr.onprogress = (event) => {
                if (event.lengthComputable) {
                    let percent = (event.loaded / event.total) * 100;
                    console.log(percent);
                }
            };

            xhr.onreadystatechange = () => {
                if (xhr.readyState === xhr.DONE && xhr.status === 200) {
                    renderer.innerHTML = xhr.responseText;
                }
            };
            xhr.open('GET', url);
            xhr.send();
        }
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
     * Like Video
     * @param {Event} event
     * @return {void}
     */
    likeVideo(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'like video',
            data: {
                video_uid: dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Dislike Video
     * @param {Event} event
     * @return {void}
     */
    dislikeVideo(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'dislike video',
            data: {
                video_uid: dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Like Comment or Reply
     * @param {Event} event
     * @return {void}
     */
    likeComment(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'like comment',
            data: {
                id: dataset.id,
                model_name: dataset.model
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Dislike Comment or Reply
     * @param {Event} event
     * @return {void}
     */
    dislikeComment(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'dislike comment',
            data: {
                id: dataset.id,
                model_name: dataset.model
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     *
     * @param {Event} event
     */
    displayCommentForm(event) {
        const newData = {
            action: 'display comment form',
            data: {
                video_uid: event.target.dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }

    closeCommentForm(event) {
        const newData = {
            action: 'close comment form',
            data: {
                video_uid: event.target.dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Comment Video
     * @param {Event} event
     * @return {void}
     */
    commentVideo(event) {
        event.preventDefault();
        const form = new FormData(event.target);
        const newData = {
            action: 'comment video',
            data: {
                content: form.get('content'),
                video_uid: event.target.dataset.uid
            }
        };

        this.sendData(this.source, newData);

        document.getElementById("comment-form-renderer").innerHTML = `<div class="border-b w-full pb-2 cursor-pointer text-sm text-gray-600 border-gray-300" data-action="click->assets#displayCommentForm" data-uid="${newData.data.video_uid}">Add a comment</div>`;
    }

    /**
     * Comment Video
     * @param {Event} event
     * @return {void}
     */
    replyComment(event) {
        event.preventDefault();

        const form = new FormData(event.target);
        const newData = {
            action: 'reply comment',
            data: {
                content: form.get('content'),
                comment_id: event.target.dataset.id,
                model_name: event.target.dataset.model
            }
        };

        this.sendData(this.source, newData);

        document.getElementById("comment-form-renderer").innerHTML = `<div class="border-b w-full py-4 cursor-pointer" data-action="click->assets#displayCommentForm" data-uid="${newData.data.video_uid}">Click Here to comment</div>`;
    }

    /**
     *
     * @param {Event} event
     */
    displayCommentReplyForm(event) {
        event.currentTarget.setAttribute('disabled', true);
        event.currentTarget.classList.add('hidden');

        const newData = {
            action: 'display comment reply form',
            data: {
                id: event.currentTarget.dataset.id,
                model_name: event.currentTarget.dataset.model
            }
        };

        this.sendData(this.source, newData);
    }

    closeCommentReplyForm(event) {
        const dataset = event.currentTarget.dataset;
        const selector = `video-comment-${dataset.id}-close-button`;
        const closeButton = document.getElementById(selector);

        closeButton.removeAttribute('disabled');
        closeButton.classList.remove('hidden');

        const newData = {
            action: 'close comment reply form',
            data: {
                id: dataset.id,
                model_name: dataset.model
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * @param {Event} event
     */
    deleteComment(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'delete comment',
            data: {
                id: dataset.id,
                model_name: dataset.model,
            },
        };
        console.log(dataset);

        this.sendData(this.source, newData);
    }

    /**
     * Display Comment Edition Form
     * @param {Event} event
     */
    displayCommentEditionForm(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'display comment edition form',
            data: {
                id: dataset.id,
                model_name: dataset.model
            },
        };

        this.sendData(this.source, newData);
    }

    closeCommentEditionForm(event) {
        const dataset = event.currentTarget.dataset;

        const newData = {
            action: 'close comment edition form',
            data: {
                id: dataset.id,
                model_name: dataset.model
            },
        };

        console.log(newData);

        this.sendData(this.source, newData);
    }

    /**
     * @param {Event} event
     */
    editComment(event) {
        event.preventDefault();

        const dataset = event.currentTarget.dataset;
        const form = new FormData(event.target);

        const newData = {
            action: 'edit comment',
            data: {
                id: dataset.id,
                content: form.get('content'),
                model_name: dataset.model,
            },
        };

        this.sendData(this.source, newData);
    }

    /**
     *
     * @param {Event} event
     */
    onCommentInputChange = (event) => {
        if (typeof event.target.value === "undefined" || event.target.value.trim() === '') {
            document.getElementById('comment-submit-button').classList.remove("active");
            document.getElementById('comment-submit-button').setAttribute('disabled', 'true');
        } else {
            document.getElementById('comment-submit-button').classList.add("active");
            document.getElementById('comment-submit-button').removeAttribute('disabled');
        }
    };

    /**
     * Filter Comments By Popularity
     * @return {void}
     */
    filterTopComments(event) {
        event.preventDefault();

        const newData = {
            action: 'filter by top comments',
            data: {
                video_uid: event.target.dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Filter Comments By Newest
     * @param {Event} event
     * @return {void}
     */
    filterNewestFirst(event) {
        event.preventDefault();

        const newData = {
            action: 'filter by newest first',
            data: {
                video_uid: event.target.dataset.uid
            }
        };

        this.sendData(this.source, newData);
    }


    /**
     * Filter Videos By Topics
     * @param {Event} event
     * @return {void}
     */
    filterByTopics(event) {
        event.preventDefault();
        const newData = {
            action: 'filter by topics',
            data: {
                topic: event.target.dataset.topic
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     * Follow Channel
     * @param {Event} event
     * @return {void}
     */
    followChannel(event) {
        event.preventDefault();

        const newData = {
            action: 'follow channel',
            data: {
                channel_id: event.target.dataset.channel
            }
        };

        this.sendData(this.source, newData);
    }

    /**
     *
     * @param {Event} e
     */
    fetchRelatedTopics() {
        const xhr = new XMLHttpRequest();
        const url = `${window.location.protocol}//${window.location.host}${window.location.pathname}${window.location.search}`;

        xhr.open("GET", url, true);
        xhr.onprogress = function (e) {
            if (e.lengthComputable) {
                let percent = (e.loaded / e.total) * 100;
                console.log(percent);
            }
        };
        xhr.send();
    }

    /**
     *
     * @param {Event} event
     */
    onPreviewHover(event) {
        event.stopImmediatePropagation();

        const newData = {
            action: 'start preview',
            data: {
                video_uid: event.currentTarget.dataset.uid
            }
        };
        this.sendData(this.source, newData);

        this.enablePreviewReloadValue = false;
    }

    enablePreview(event) {
        if (this.enablePreviewReloadValue) {
            this.onPreviewHover(event);
        }
    }

    /**
     *
     * @param {Event} event
     */
    disablePreview(event) {
        event.preventDefault();
        this.enablePreviewReloadValue = true;

        const newData = {
            action: 'stop preview',
            data: {
                video_uid: event.currentTarget.dataset.uid
            }
        };
        this.sendData(this.source, newData);
    }
}