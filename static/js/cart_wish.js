const containers = document.getElementsByClassName('single-product-container');
for (const container of containers) {
    container.addEventListener('click', () => {
        const target = container.querySelector('.link-to-product');
        target.click()
    })
};

const btn = document.getElementById('cart-btn');
btn.addEventListener('click',  () => {
    const form = document.getElementById('cart-form');
    form.submit();
});

const wishBtn = document.getElementById('wish-btn');
wishBtn.addEventListener('click', () => {
    const form = document.getElementById('wish-form');
    form.submit();
});

const rateBtns = document.querySelectorAll('.rate-btn');
rateBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        btn.querySelector('a').click()
    })
} )