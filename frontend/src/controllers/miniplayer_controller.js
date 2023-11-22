import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ['viewer', 'progress', 'controls', 'filled', 'timer', 'prefetch', 'mute'];
    static values = {
        mousedown: {
            type: Boolean,
            default: false,
        }
    };

    connect() {
        const video = this.viewerTarget;

        video.play();
        video.muted = true;
    }

    onmousedown(event) {
        event.preventDefault();
        this.mousedownValue = true;
    }

    onmouseup(event) {
        event.preventDefault();
        this.mousedownValue = false;
    }

    /**
     * Mute or Unmute Video
     * @param {Event} event
     */
    mute(event) {
        event.preventDefault();

        const video = this.viewerTarget;
        const muteButton = this.muteTarget;

        if (video.muted) {
            video.muted = false;
            muteButton.querySelector('.yt--muted-icon').classList.add('hidden');
            muteButton.querySelector('.yt--mute-icon').classList.remove('hidden');
        } else {
            video.muted = true;
            muteButton.querySelector('.yt--muted-icon').classList.remove('hidden');
            muteButton.querySelector('.yt--mute-icon').classList.add('hidden');
        }
    }

    /**
     *
     * @param {Event} event
     */
    prefetch(event) {
        event.preventDefault();

        if (this.mousedownValue) {
            const progress = this.progressTarget;
            const video = this.viewerTarget;

            const percent = (event.offsetX / progress.offsetWidth) * 100;
            this.filledTarget.style.flexBasis = `${percent}%`;
            let currentTime = percent * video.duration / 100;
            this.timerTarget.querySelector('.yt--timer--current-time').innerHTML = this.customTimeFormat(currentTime);
        }
    }

    /**
     *
     */
    progress() {
        if (!this.mousedownValue) {
            const video = this.viewerTarget;

            const percent = (video.currentTime / video.duration) * 100;
            this.filledTarget.style.flexBasis = `${percent}%`;

            this.timerTarget.querySelector('.yt--timer--current-time').innerHTML = this.customTimeFormat(video.currentTime);
        }
    }

    /**
     *
     * @param {Event} event
     */
    scrub(event) {
        event.preventDefault();

        const video = this.viewerTarget;
        const progress = this.progressTarget;

        video.currentTime = (event.offsetX / progress.offsetWidth) * video.duration;
    }

    /**
     *
     * @param seconds
     * @param guide
     * @return {string}
     */
    customTimeFormat(seconds, guide) {
        seconds = seconds < 0 ? 0 : seconds;
        let s = Math.floor(seconds % 60);
        let m = Math.floor(seconds / 60 % 60);
        let h = Math.floor(seconds / 3600);
        let gm = Math.floor(guide / 60 % 60);
        let gh = Math.floor(guide / 3600); // handle invalid times

        if (isNaN(seconds) || seconds === Infinity) {
            // '-' is false for all relational operators (e.g. <, >=) so this setting
            // will add the minimum number of fields specified by the guide
            h = m = s = '-';

            return h + ':' + s;
        } // Check if we need to show hours


        h = h > 0 || gh > 0 ? h + ':' : ''; // If hours are showing, we may need to add a leading zero.
        // Always show at least one digit of minutes.

        m = ((h || gm >= 10) && m < 10 ? '0' + m : m) + ':'; // Check if leading zero is need for seconds

        h = parseInt(h) < 10 ? '0' + h : h;
        s = parseInt(s) < 10 ? '0' + s : s;

        return h + m + s;
    }
}
