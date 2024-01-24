/**
  * @typedef {{found: number, data: {[commentId: number]: {name: string, img: string, price:string,  link: string}}}} productResponse
*/

class ProductFetcher {
  constructor() {
    this.fetchUrl = this.getFetchUrl();
  }

  getFetchUrl() {
    const a = document.getElementById("moreProductsUrl");
    const href = a.getAttribute("href");
    a.remove();
    return href
  }

  async requestData() {
    const response = await fetch(this.fetchUrl);
    return await response.json();
  }
}

class Manager {
  static fetchProducts = true;

  static async init() {
    if (!Manager.fetchProducts) {
      return;
    }
    const fetcher = new ProductFetcher();
    /**@type {productResponse} */
		const responseData = await fetcher.requestData();
    const targetDiv = document.getElementById('other-products');
    if (!!responseData.found) {
      for (const [productId, product] of Object.entries(responseData.data)) {
        const div = Manager.createProductDiv();
        div.append(Manager.setImg(product.img, product.name));
        div.append(Manager.setName(product.name));
        div.append(Manager.SetPriceBtn(product.price, product.link));
        targetDiv.append(div);
      }
      Manager.addListeners([...targetDiv.children])
      Manager.clearPlaceHolders();
      Manager.fetchProducts = false
    }

		
  }

  /**
   * 
   * @param {[HTMLElement]} children 
   */
  static addListeners(children) {
    children.forEach((child) => {
      child.addEventListener('click', () => {
        const link = child.querySelector('a');
        link.click();
      });
    })
  }

  static createProductDiv() {
    const div = document.createElement('div');
    div.setAttribute('class', 'max-sm:col-span-2 max-w-sm  mx-4 mb-4 p-4 md:p-6 md:col-span-1');
    return div;
  }

  static setImg(src, productName) {
    const imgContainer =document.createElement('div');
    imgContainer.setAttribute('class', 'p-4 flex justify-center');
    const img = document.createElement('img');
    img.setAttribute('src', src);
    img.setAttribute('alt', productName);
    img.setAttribute('class', 'w-auto h-32');
    img.setAttribute('loading', 'lazy');
    imgContainer.append(img);
    return imgContainer;
  }

  static setName(productName) {
    const h4 = document.createElement('h4');
    h4.setAttribute('class', 'pt-2 font-semibold text-lg');
    h4.innerText = productName;
    return h4;
  }

  static SetPriceBtn(price, link) {
    const mainDiv = document.createElement('div');
    mainDiv.setAttribute('class', 'grid grid-cols-2');

    const priceSpan = document.createElement('span');
    priceSpan.setAttribute('class', 'col-span-1 font-semibold flex items-end text-lg');
    priceSpan.innerHTML = `${price} €`;

    mainDiv.append(priceSpan);
    mainDiv.append(Manager.createBtn(link));
    return mainDiv;
  }

  static clearPlaceHolders() {
    const target = document.getElementById('card-placeholders');
    target.remove()
  }

  /**
   * 
   * @param {string| null} innerText 
   * @returns {HTMLElement}
   */
  static createSpanTag(innerText, addClss) {
    const span = document.createElement('span');
    span.setAttribute('class', `col-span-1 font-semibold ${addClss}`);
    span.innerHTML = innerText !== null ? innerText : ''
    return span;
  }

  static createBtn(link) {
    const span = document.createElement('span');
    span.setAttribute('class', 'col-span-1 font-semibold');

    const btn = document.createElement('button');
    btn.setAttribute('class', 'rounded-lg bg-blue-600 p-1 text-white hover:bg-blue-700');
    btn.innerHTML = `<a href=${link}>see product</a>`;
    span.append(btn);
    return span;
  }
  
}


setTimeout(() => {
	Manager.init();
}, 500)