// Modal window
const overlay = document.querySelector(".overlay");

const deleteButtons = document.querySelectorAll('.delete-product-button');
const cancelButtons = document.querySelectorAll('.grey');

for (let button of cancelButtons) {
    button.addEventListener("click", closeModal);
}

for (let button of deleteButtons) {
    button.addEventListener("click", openModal);
}

// close modal function
function closeModal(e) {
    let modal = e.target.closest('.modal');
    modal.classList.add("hidden");
    overlay.classList.add("hidden");
}

// open modal function
function openModal(e) {
    let contentItem = e.target.closest('.content__item-element');
    let modal = contentItem.querySelector(".modal");
    console.log(modal);

    modal.classList.remove("hidden");
    overlay.classList.remove("hidden");
}
