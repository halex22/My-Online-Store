/**
 * @typedef {{found: bool , number: number}} cartJsonResponse
 */
class CartFetcher {

    constructor () {
        this.url = '/store/fetch-cart-products'
    }

    async getData() {
        const response = await fetch(this.url);
        return await response.json();
    }
}

class CartNumber {

    static target = document.getElementById('cart-number');

    static async init() {
        const fetcher = new CartFetcher();

        /**@type {cartJsonResponse} */
        const response = await fetcher.getData();
        console.log(response);
        if (!!response.found) {
            CartNumber.setCart(response.number);
        } else {
            return
        }
    }

    static setCart(number) {
        CartNumber.target.classList.remove('sr-only')
        CartNumber.target.innerText = number
    }
}

CartNumber.init();