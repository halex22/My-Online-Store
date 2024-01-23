/**
 * @typedef {Array<{className: string, value: string}>} ClassAndAttrs
 * @typedef {{found: number, data: {[commentId: number]: {name: string, date: string, rating: number, text: string}}}} jsonResponse
 */

/**
 *
 * @param {string} stringDate
 * @returns {string}
 */
function formatDate(stringDate) {
  const dateString = new Date(stringDate.replace(" ", "T"));
  const optns = {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: false,
  };
  const formatter = new Intl.DateTimeFormat("en-US", optns);
  return formatter.format(dateString);
}

class CommentFetcher {
  constructor() {
    this.fetchUrl = this.getFetchUrl();
  }

  getFetchUrl() {
    const productId = window.location.href.split("/").slice(-1);
    return "/store/fetch-comments/".concat(productId);
  }

  async requestData() {
    const response = await fetch(this.fetchUrl);
    return await response.json();
  }
}

class CommentManager {
  static fetchComments = true;
  static starSvg = document.getElementById("example-star");
  static async init() {
    if (!CommentManager.fetchComments) {
      return;
    }

    const commentFetcher = new CommentFetcher();

    /**@type {jsonResponse} */
    const responseData = await commentFetcher.requestData();
    const commentContainer = document.getElementById("comment-container");

    if (!!responseData.found) {
      for (const [commentId, comment] of Object.entries(responseData.data)) {
        const article = document.createElement("article");
        article.append(CommentManager.setImg(comment.name, comment.date));
        article.append(CommentManager.setRating(comment.rating));
        article.append(CommentManager.setText(comment.text));
        commentContainer.append(article);
      }
    } else {
    }
    CommentManager.starSvg.remove();
    CommentManager.fetchComments = false;
    CommentManager.clearPlaceHolders();
  }

  /**
   * methods that esambles the img part of the comment
   * @param {string} username
   * @param {string} date
   * @returns {HTMLElement}
   */
  static setImg(username, date) {
    const mainDiv = CommentManager.createDiv("flex items-center mb-4");

    const img = document.createElement("img");
    img.setAttribute("class", "w-10 h-10 me-4 rounded-full");
    img.setAttribute("src", "/media/defaults/default-avatar.webp");

    const innerDiv = CommentManager.createDiv("font-medium");

    const paragraph = document.createElement("p");
    paragraph.innerHTML = username;

    const time = document.createElement("time");
    time.setAttribute("datetime", date);
    time.setAttribute("class", "block text-sm text-gray-500");
    time.innerHTML = formatDate(date);

    for (const element of [paragraph, time]) {
      innerDiv.append(element);
    }

    for (const element of [img, innerDiv]) {
      mainDiv.append(element);
    }
    return mainDiv;
  }

  /**
   *
   * @param {number} startNumber
   * @returns {HTMLElement}
   */
  static setRating(startNumber) {
    const divClass = "flex items-center mb-1 space-x-1 rtl:space-x-reverse";
    const mainDiv = CommentManager.createDiv(divClass);
    const star = CommentManager.starSvg;
    star.classList.remove("hidden");
    for (let i = 0; i < startNumber; i++) {
      mainDiv.appendChild(star.cloneNode(true));
    }
    return mainDiv;
  }

  /**
   *
   * @param {string} text
   * @returns {HTMLElement}
   */
  static setText(text) {
    const paragraph = document.createElement("p");
    paragraph.setAttribute("class", "mb-2 text-gray-500");
    paragraph.innerHTML = text;
    return paragraph;
  }

  /**
   * Creates a base div and sets the class attr
   * @param {string} class_attr
   * @returns {HTMLElement}
   */
  static createDiv(class_attr) {
    const div = document.createElement("div");
    div.setAttribute("class", class_attr);
    return div;
  }

  static clearPlaceHolders() {
    const placeHolders = document.querySelectorAll(".comment-placeholder");
    for (const item of [...placeHolders]) {
      item.remove();
    }
  }
}

const target = document.getElementById("comment-container");
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      CommentManager.init();
    };
  });
});

observer.observe(target);
