const containers = document.getElementsByClassName('single-product-container');
for (const container of containers) {
    container.addEventListener('click', () => {
        const target = container.querySelector('.link-to-product');
        target.click()
    })
};

