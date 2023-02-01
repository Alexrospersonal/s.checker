let frontImageInput = document.querySelector('#front-image-button');
let backImageInput = document.querySelector('#back-image-button');


let frontImageContainer = document.getElementById('front-img');
let backImageContainer = document.getElementById('back-img');

frontImageInput.addEventListener('change', (e) => createImage(frontImageContainer, e));
backImageInput.addEventListener('change', (e) => createImage(backImageContainer, e));


const createImage = async (image_container, e) => {
    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
    let image = e.target.files[0];
    let formData = new FormData();

    formData.append('file', image);
    formData.append('csrfmiddlewaretoken', csrf_token)

    let newImage = await fetch('http://127.0.0.1:8000/conver-file/', {
        credentials: "include",
        method: "POST",
        mode: "same-origin",
        body: formData,

    }).then((response) => response.json()).catch(error => console.error(error));

    addImageToList(newImage, image_container);
}

function addImageToList(image, image_container) {

    clearImageContainer(image_container);
    let img = document.createElement('img');
    img.src = image['images'];
    img.width = 300;
    image_container.appendChild(img);
}

function clearImageContainer(image_container) {
    if (image_container.firstChild) {
        image_container.removeChild(image_container.firstChild)
    }
}

// function loading(image_container) {
//     let div = document.createElement('div');
//     div.setAttribute('id', 'loading');
//     let p_loading = document.createElement('p');
//     p_loading.innerText = 'Loading....';
//     div.appendChild(p_loading);
//     image_container.appendChild(div);
// }