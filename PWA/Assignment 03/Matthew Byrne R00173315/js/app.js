// Matthew Byrne, R00173315 

const searchTerms = ["Cat","Dog","Fish"] 
const searchButtons = [] 

for (i = 0; i < searchTerms.length; i++) {
  const button = document.createElement("button");
  button.innerText = searchTerms[i];
  button.className = "nav-item";

  (function(index) {
    button.onclick = function() {
      document.getElementById("main-grid").innerHTML = "";
      for (searchButton of searchButtons) { 
        searchButton.disabled = true;
        searchButton.style.color = "grey";
      }

      console.log(searchTerms[index]);
      document.getElementById("searchingText").style.display = "block";
      const script = document.createElement('script');
      script.src = 'https://api.flickr.com/services/feeds/photos_public.gne?tags=' + searchTerms[index] + '&format=json&jsoncallback=handleResponse';
      document.body.appendChild(script);
      
    }

  }) (i);
  searchButtons.push(button)
  document.getElementById("nav-list").appendChild(button);
}


function addModal(img, title) {
  img.addEventListener('click', () => {
    const modal = document.createElement('div');
    modal.className = "modal";

    const modalText = document.createElement('div');
    modalText.className = "modal-content";
    modalText.innerText = title;

    modal.appendChild(modalText);
    document.body.appendChild(modal);

    modal.addEventListener('click', () => {
      document.body.removeChild(modal);
    });
  });
}


if (JSON.parse(localStorage.getItem("flickrImages"))) {

  JSON.parse(localStorage.getItem("flickrImages")).forEach((cachedImage) => {
    const img = document.createElement("img");
    img.src = cachedImage.media.m;
    img.alt = cachedImage.title;
    document.getElementById("main-grid").appendChild(img);

    addModal(img, cachedImage.title)
  });
}


class ImageLoader {
  constructor(img, imgSrc, imageTitle) {
    this.img = img;
    this.imgSrc = imgSrc;
    this.imageTitle = imageTitle;
  }

  loadImage() {
    return new Promise((resolve, reject) => {
      this.img.onload = () => {
        this.img.src = this.imgSrc;
        this.img.alt = this.imageTitle;
        resolve();
      };
      this.img.onerror = () => {
        console.error("Failed to load image!");
        this.img.src = "./icon/error.png";
        this.img.alt = "Image failed to load";
        resolve();
      };
    })
  }
}


function handleResponse(res) {
  const promises = [];
  const flickrImages = [];
  
  for (let i = 0; i < 10; i++) {
    if (!res.items[i]) {
      continue;
    }
    const img = document.createElement("img");
    img.src = "./icon/loader.gif";
    document.getElementById("main-grid").appendChild(img);

    const imageLoader = new ImageLoader(img, res.items[i].media.m, res.items[i].title);
    const promise = imageLoader.loadImage();

    promise.then(() => {
      document.getElementById("searchingText").style.display = "none";
    });

    promises.push(promise);
    addModal(img, res.items[i].title)
    flickrImages.push(res.items[i]);
    }
  
  Promise.all(promises).then(() => {
    for (searchButton of searchButtons) {
      searchButton.disabled = false;
      searchButton.style.color = "white";
    }
  }).catch(error => {
    console.error(error);
  });

  localStorage.setItem("flickrImages", JSON.stringify(flickrImages));
}



function showNav() {
  if (document.getElementById('nav-list').style.display === "none") {
    document.getElementById('nav-list').style.display = "flex";
    document.getElementById('nav-list').style.flexWrap = "wrap";
  } else {
    document.getElementById('nav-list').style.display = "none";
  }
}
