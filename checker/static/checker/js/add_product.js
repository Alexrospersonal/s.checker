$('.input-file input[type=file]').on('change', function(){
	let file = this.files[0];
	$(this).closest('.input-file').find('.input-file-text').html(file.name);
});

let loadDiv = document.getElementById('load-image');

function addMultiPageProduct() {
    loadDiv.replaceChildren();
    loadDiv.innerHTML = `
    <div class="content__container">
        <label for="front-img" class="item__title">Лице</label>
        <canvas id="front-img"></canvas>
    </div>
    <div class="content__container">
        <fieldset form="product-form">
            <div>
                <label for="front-file" class="item__title">Файл</label>
                <label class="input-file">
                    <input type="file" name="file" accept=".pdf multipl">
                    <span class="input-file-btn">Виберіть файл</span>           
                    <span class="input-file-text">Максимум 250мб</span>
                </label>
        </fieldset>
    `;
}

function addOnePageProduct() {
    loadDiv.replaceChildren();
    loadDiv.innerHTML = `
    <div class="content__container">
        <label for="front-img" class="item__title">Лице</label>
        <canvas id="front-img"></canvas>
    </div>
    <div class="content__container">
        <fieldset form="product-form">
            <div>
                <label for="front-file" class="item__title">Лице</label>
                <label class="input-file">
                    <input type="file" name="file" accept=".jpeg, .jpg, .tiff, .pdf">
                    <span class="input-file-btn">Виберіть файл</span>           
                    <span class="input-file-text">Максимум 100мб</span>
                </label>
            </div>
            <div>
                <label for="back-file" class="item__title">Зворот</label>
                <label class="input-file">
                    <input type="file" name="file" accept=".jpeg, .jpg, .tiff, .pdf" disabled>
                    <span class="input-file-btn">Виберіть файл</span>           
                </label>
            </div>
        </fieldset>
</div>
    `;
}

function addTwoPageProduct() {
    loadDiv.replaceChildren();
    loadDiv.innerHTML = `
        <div class="content__container">
            <label for="front-img" class="item__title">Зображення</label>
            <canvas id="front-img"></canvas>
        </div>
        <div class="content__container">
            <label for="back-img" class="item__title">Зворот</label>
            <canvas id="back-img"></canvas>
        </div>
        <div class="content__container">
            <fieldset form="product-form">
                <div>
                    <label for="front-file" class="item__title">Лице</label>
                    <label class="input-file">
                        <input type="file" name="file" accept=".jpeg, .jpg, .tiff, .pdf">
                        <span class="input-file-btn">Виберіть файл</span>           
                        <span class="input-file-text">Максимум 100мб</span>
                    </label>
                </div>
                <div>
                    <label for="back-file" class="item__title">Зворот</label>
                    <label class="input-file">
                        <input type="file" name="file" accept=".jpeg, .jpg, .tiff, .pdf">
                        <span class="input-file-btn">Виберіть файл</span>           
                        <span class="input-file-text">Максимум 100мб</span>
                    </label>
                </div>
            </fieldset>
        </div>
    `;
}


let addFrontFileButton = document.getElementById("front-image-button");
let addBackFileButton = document.getElementById("back-image-button");

let frontImageCanvas = document.getElementById("front-img");
let backImageCanvas = document.getElementById("back-img");

// let backImageContainer = document.getElementById("back-image-container");




// addBackFileButton.onchange = function(event) {
//     console.log(event.target.files[0]);
//     show(event.target.files[0]);
// }

// function show(file) {
//     var reader = new FileReader();
//     reader.onload = (function (theFile) {
//       return function (e) {
//         var buffer = e.target.result;
//         var tiff = new Tiff({buffer: buffer});
//         var canvas = tiff.toCanvas();
//         var width = tiff.width();
//         var height = tiff.height();
//         if (canvas) {
//             backImageContainer.appendChild(canvas);
//         }
//       };
//     })(file);
//     reader.readAsArrayBuffer(file);
//   }


// addFrontFileButton.onchange = function() {
//     var img = new Image;
//     img.onload = convert;
//     img.src = URL.createObjectURL(this.files[0]);
//     let ctx = frontImageCanvas.getContext("2d");
//     img.onload = onload = function() {
//         ctx.drawImage(img, 0, 0);
//       };
    
// }

// function convert() {
//     URL.revokeObjectURL(this.src);             // free up memory
//     var c = document.createElement("canvas"),  // create a temp. canvas
//         ctx = c.getContext("2d");
//     c.width = this.width;                      // set size = image, draw
//     c.height = this.height;
//     ctx.drawImage(this, 0, 0);
    
//     // convert to File object, NOTE: we're using binary mime-type for the final Blob/File
//     c.toBlob(function(blob) {
//       var file = new File([blob], "MyJPEG.jpg", {type: "application/octet-stream"});
//       window.location = URL.createObjectURL(file);
//     }, "image/jpeg", 0.75);  // mime=JPEG, quality=0.75
//   }


// function convert() {
//     URL.revokeObjectURL(this.src);             // free up memory
//     var c = document.createElement("canvas"),  // create a temp. canvas
//         ctx = c.getContext("2d");
//     c.width = this.width;                      // set size = image, draw
//     c.height = this.height;
//     ctx.drawImage(this, 0, 0);
    
//     // convert to File object, NOTE: we're using binary mime-type for the final Blob/File
//     var jpeg = c.toDataURL("image/jpeg", 0.75);  // mime=JPEG, quality=0.75
//     console.log(jpeg.length)
// }


// const selectedFile = addFrontFileButton.files[0];


// addFrontFileButton.addEventListener('change', addFiletoCanvas, false);

// function addFiletoCanvas() {
//     const file = this.files[0];
//     const image = new Image();
//     image.src = URL.createObjectURL(file);
//     console.log(typeof image);
//     // let ctx = frontImageCanvas.getContext("2d");
//     // ctx.drawImage(image, 0,0, 300, 150);
//     testDiv.appendChild(image);
// }