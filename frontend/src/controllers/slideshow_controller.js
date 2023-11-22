import { Controller } from "@hotwired/stimulus";
import "../styles/blocks/slideshow.scss";

export default class extends Controller {
  static targets = ['slideWrapper', 'paginationNext', 'paginationPrevious'];

  connect() {
      const next = this.paginationNextTarget;
      const previous = this.paginationPreviousTarget;
      const slideWrapper = this.slideWrapperTarget;
      let isDraggle = false;

      slideWrapper.addEventListener("doubleclick", () => isDraggle = true);
      slideWrapper.addEventListener("mousemove", function (e) {
          if (!isDraggle) return;
          let element = e.currentTarget;

          element.classList.add("dragging");
          element.scrollLeft -= e.movementX;

          let maxScrollableWidth = element.scrollWidth - element.clientWidth;

          previous.style.display = element.scrollLeft <= 0 ? "none": "flex";
          next.style.display = maxScrollableWidth - element.scrollLeft <= 1 ? "none": "flex";
      });
      slideWrapper.addEventListener("mouseup", function() {
          isDraggle = false;
          slideWrapper.classList.remove("dragging");
      });

      slideWrapper.addEventListener("scroll", function(e) {
          let maxScrollableWidth = e.currentTarget.scrollWidth - e.currentTarget.clientWidth;

          previous.style.display = e.currentTarget.scrollLeft <= 0 ? "none": "flex";
          next.style.display = maxScrollableWidth - e.currentTarget.scrollLeft <= 1 ? "none": "flex";
      });
  }

  nextPaginationEvent() {
      this.slideWrapperTarget.scrollLeft += 340;
  }

  previousPaginationEvent() {
      this.slideWrapperTarget.scrollLeft -= 340;
  }
}