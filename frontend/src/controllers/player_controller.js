import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = ['viewer', 'progress', 'controls', 'filled', 'timer', 'prefetch', 'mute', 'playButton', 'volume', 'volumeFilled'];
    static values = {
        mousedown: {
            type: Boolean,
            default: false,
        },
        volumedown: {
            type: Boolean,
            default: false,
        }
    };

    connect() {
        const video = this.viewerTarget;
        video.play();
        video.volume = 0.25;
    }

    /**
     *
     * @param {Event} event
     */
    play(event) {
        event.preventDefault();
        const video = this.viewerTarget;
        const playBtn = this.playButtonTarget;

        if (!video.paused) {
            video.pause();
            playBtn.querySelector('svg.yt--play-icon.yt--played').classList.add('hidden');
            playBtn.querySelector('svg.yt--play-icon.yt--paused').classList.remove('hidden');
        } else {
            video.play();
            playBtn.querySelector('svg.yt--play-icon.yt--played').classList.remove('hidden');
            playBtn.querySelector('svg.yt--play-icon.yt--paused').classList.add('hidden');
        }
    }

    onmousedown(event) {
        event.preventDefault();
        this.mousedownValue = true;
    }

    onmouseup(event) {
        event.preventDefault();
        this.mousedownValue = false;
    }

    // disconnect() {
    //     const video = this.viewerTarget;
    //
    //     if (!video.paused) {
    //         video.pause();
    //     }
    // }

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

    volume(event) {
        if (this.volumedownValue) {
            const volume = this.volumeTarget;
            const video = this.viewerTarget;
            const muteButton = this.muteTarget;

            const percent = (event.offsetX / volume.offsetWidth) * 100;
            this.volumeFilledTarget.style.flexBasis = `${percent}%`;
            const volume_percent = event.offsetX / volume.offsetWidth;
            video.volume = volume_percent;

            if (volume_percent === 0) {
                video.muted = true;
                muteButton.querySelector('.yt--muted-icon').classList.remove('hidden');
                muteButton.querySelector('.yt--mute-icon').classList.add('hidden');
            } else {
                video.muted = false;
                muteButton.querySelector('.yt--muted-icon').classList.add('hidden');
                muteButton.querySelector('.yt--mute-icon').classList.remove('hidden');
            }
        }
    }

    volumemousedown(event) {
        event.preventDefault();
        this.volumedownValue = true;
    }

    volumemouseup(event) {
        event.preventDefault();
        this.volumedownValue = false;
    }

    /**
     *
     */
    progress() {
        if (!this.mousedownValue) {
            const video = this.viewerTarget;
            const playBtn = this.playButtonTarget;

            const percent = (video.currentTime / video.duration) * 100;
            this.filledTarget.style.flexBasis = `${percent}%`;

            this.timerTarget.querySelector('.yt--timer--current-time').innerHTML = this.customTimeFormat(video.currentTime);

            if (video.ended) {
                console.log('ended');

                playBtn.querySelector('svg.yt--play-icon.yt--played').classList.add('hidden');
                playBtn.querySelector('svg.yt--play-icon.yt--paused').classList.remove('hidden');
            }
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
