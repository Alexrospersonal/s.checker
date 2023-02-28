// let frontImageInput = document.querySelector('#front-image-button');
// let backImageInput = document.querySelector('#back-image-button');


// let frontImageContainer = document.getElementById('front-img');
// let backImageContainer = document.getElementById('back-img');

let addImageButtonsContainer = document.querySelector('.add-image-buttons-container');

let imageContainer = document.querySelector('.load-image');

let imageGalery = document.querySelector('#galery');


// frontImageInput.addEventListener('change', (e) => createImage(frontImageContainer, e));
// backImageInput.addEventListener('change', (e) => createImage(backImageContainer, e));

function createButton(num) {
    addImageButtonsContainer.innerHTML = '';
    imageContainer.innerHTML = '';
    imageGalery.innerHTML = '';

    for (let i = 0; i < num; i++) {
        let labelFor = document.createElement('label');
        labelFor.setAttribute("for", "front-file");
        labelFor.className = "item__title"
        labelFor.innerText = "Файл";

        let labelInput = document.createElement('label');
        labelInput.className = "input-file";

        let input = document.createElement('input');
        input.setAttribute("type", "file");
        input.setAttribute("name", "images");
        input.setAttribute("accept", ".jpeg, .jpg, .tif, .pdf");
        input.setAttribute("required", "");
        input.id = `image-button-${i}`;
        input.addEventListener('change', (e) => {
            e.target.closest('.input-file').querySelector('.input-file-text').innerText = e.target.files[0].name;
            createImage(e, e.target.files[0].name);
        });

        let spanFile = document.createElement('span');
        spanFile.className = "input-file-btn";
        spanFile.innerText = `Виберіть файл ${i+1}`;

        let spanSize = document.createElement('span');
        spanSize.className = "input-file-text";
        spanSize.innerText = 'Максимум 100мб';

        labelInput.appendChild(input);
        labelInput.appendChild(spanFile);
        labelInput.appendChild(spanSize);

        addImageButtonsContainer.appendChild(labelFor);
        addImageButtonsContainer.appendChild(labelInput);

        imageContainer.appendChild(createShowImageContainer(i));
        imageGalery.appendChild(addImageToModalGalery(i));
    }
}

function addImageToModalGalery(id) {
    let li = document.createElement('li');
    li.id = `image-container-${id}`;
    li.className = 'galery-image-container';
    return li;

}


function createShowImageContainer(id) {

    // <div class="content__container">
    //       <label for="front-img" class="item__title">Лице</label>
    //       <div class="image-container" id="front-img"></div>
    // </div>

    let wrapperDivId = `wrapper-div-${id}`;

    let div = document.createElement('div');
    div.className = "thumbnail__container";
    div.id = wrapperDivId;

    let label = document.createElement('label');
    label.className = 'item__title';
    label.innerText = `Файл ${id+1}`;

    let imageDiv = document.createElement('div');
    imageDiv.className = 'image-container';
    // imageDiv.addEventListener('click', openModal);

    div.appendChild(label);
    div.appendChild(imageDiv);

    return div;
}


// function createShowImageContainer(name, id) {
//
//     // <div class="content__container">
//     //       <label for="front-img" class="item__title">Лице</label>
//     //       <div class="image-container" id="front-img"></div>
//     // </div>
//
//     let div = document.createElement('div');
//     div.className = "thumbnail__container";
//     div.id = id;
//
//     let label = document.createElement('label');
//     label.className = 'item__title';
//     label.innerText = `Файл ${name}`;
//
//     let imageDiv = document.createElement('div');
//     imageDiv.className = 'image-container';
//     imageDiv.addEventListener('click', openModal);
//
//     div.appendChild(label);
//     div.appendChild(imageDiv);
//
//     return div;
// }

const createImage = async (e, name) => {
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

    addImageToList(newImage, name, e.target.id);
}

function addImageToList(image, name, targetId) {

    let img = document.createElement('img');
    img.src = image['images'];
    img.width = 150;

    let galeryImg = document.createElement('img');
    galeryImg.src = image['images'];
    galeryImg.width = 600;

    let numberTargetId = targetId.match(/\d+/)[0];

    let imageGalleryLi = imageGalery.querySelector(`#image-container-${numberTargetId}`);
    imageGalleryLi.innerHTML = '';
    imageGalleryLi.appendChild(galeryImg);

    let wrapperDiv = imageContainer.querySelector(`#wrapper-div-${numberTargetId}`);
    wrapperDiv.querySelector('.item__title').innerText = name;

    let imageDiv = wrapperDiv.querySelector('.image-container');
    imageDiv.innerHTML = '';
    imageDiv.appendChild(img);
    imageDiv.addEventListener('click', openModal);


    // let wrapperDiv = createShowImageContainer(name, wrapperDivId);
    // let imageDiv = wrapperDiv.querySelector('.image-container');
    // imageDiv.appendChild(img);

    // let listOfThumbnails = imageContainer.querySelectorAll('.thumbnail__container');
    // let listOfThumbnails = Array.from(imageContainer.querySelectorAll('.thumbnail__container'));
    //
    // if (listOfThumbnails.length > 1) {
    //     listOfThumbnails.forEach( (item, index, array) => {
    //         if (item.id === `${wrapperDivId}`) {
    //             item.removeChild(item.querySelector('div'));
    //             item.querySelector('label').innerText = name;
    //             item.appendChild(imageDiv);
    //         }
    //     });

        // listOfThumbnails.sort(function (a, b) {
        //     let one = a.querySelector('div').id.match(/\d+/)[0];
        //     let two = b.querySelector('div').id.match(/\d+/)[0];
        //
        //     return +one > +two ? 1 : -1;
        // });
    // }else {
    //     listOfThumbnails.push(wrapperDiv);
    // }
    //
    // for (const thumbnail of listOfThumbnails) {
    //     imageContainer.appendChild(thumbnail);
    // }

    // let prevThumbnail = listOfThumbnails.find((element) => {
    //     console.log(element);
    //     return element.id === wrapperDivId;
    // })


    // let result;
    //
    // if (listOfThumbnails.length > 0) {
    //     result = listOfThumbnails.querySelector(`#${wrapperDivId}`);
    // }
    // if (result) {
    //     listOfThumbnails.removeChild(imageContainer.querySelector(`#${wrapperDivId}`));
    // }

    // let result = imageContainer.querySelector(`#${wrapperDivId}`);
    // if (result) {
    //     imageContainer.removeChild(imageContainer.querySelector(`#${wrapperDivId}`));
    // }

    // let wrapperDiv = createShowImageContainer(name, wrapperDivId);
    // let imageDiv = wrapperDiv.querySelector('.image-container');
    // imageDiv.appendChild(img);

    // imageContainer.appendChild(wrapperDiv);
    // listOfThumbnails.append(wrapperDiv);
    // let sortedListOfThumbnails = [].slice.call(listOfThumbnails).sort(function (a, b) {
    //     return a.id > b.id ? 1 : -1;
    // });
    //
    // console.log(sortedListOfThumbnails);
}

let position = 0;

let rightButton = document.querySelector('#move-right');
    rightButton.addEventListener('click', (e) => {
    position -= 600;
    console.log('Right');
    position = Math.max(position, -600 * (document.querySelectorAll('.galery-image-container').length - 1));

    imageGalery.style.marginLeft = position + 'px';
})

let leftButton = document.querySelector('#move-left');
    leftButton.addEventListener('click', (e) => {
    position += 600;
    position = Math.min(position, 0)
    imageGalery.style.marginLeft = position + 'px';
})

// Modal window
const modal = document.querySelector(".modal");
const overlay = document.querySelector(".overlay");
const closeModalBtn = document.querySelector(".btn-close");

// close modal function
function closeModal() {
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
}

// close the modal when the close button and overlay is clicked
closeModalBtn.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);

// close modal when the Esc key is pressed
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !modal.classList.contains("hidden")) {
    closeModal();
  }
});

// open modal function
function openModal(e) {
    let id = e.target.closest('.thumbnail__container').id.match(/\d+/)[0];
    position = 0;
    position -= 600 * +id;
    imageGalery.style.marginLeft = position + 'px';

    modal.classList.remove("hidden");
    overlay.classList.remove("hidden");
}

