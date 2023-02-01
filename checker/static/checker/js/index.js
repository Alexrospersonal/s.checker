const btn = document.getElementById("button-swith-form");


btn.addEventListener('click', ()=> {
    const form = document.getElementById("filter-form");
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'flex';
        form.style.flexWrap = 'wrap';
        form.style.alignItems = 'flex-end';
        btn.style.marginBottom = '15px';
    }
    else {
        form.style.display = 'none';
        btn.style.marginBottom = '0px';
    }
});

document.addEventListener('change', function (e) {
    const id = e.target.id;
    if (id.includes('size-selector')) {
        change_size(id);
    }
})

function change_size(id) {
    let selector = document.getElementById(id);
    let id_number = id.match(/\d+/)[0];
    let pSizeText = document.getElementById(`size-text-${id_number}`);
    let item = selector.selectedIndex;
    let sizes = pSizeText.innerText.split('x');
    if (item === 1) {
        pSizeText.innerHTML = `${sizes[0] / 10}<span>x</span>${sizes[1] / 10}`;
    }
    if (item === 0) {
        pSizeText.innerHTML = `${sizes[0] * 10}x${sizes[1 ]* 10}`;
    }

}
