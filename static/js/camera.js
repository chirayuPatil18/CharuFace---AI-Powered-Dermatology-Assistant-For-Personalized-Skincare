const video = document.getElementById("video");

// RESET STATE
let step = 0;
const steps = ["LEFT", "CENTER", "RIGHT"];
const keys = ["left", "center", "right"];

let images = {
    left: null,
    center: null,
    right: null
};

// CAMERA START
if (video) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => video.srcObject = stream)
    .catch(err => console.error("Camera error:", err));
}

// CAPTURE FUNCTION
function capture(){

    if(step >= 3){
        return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    canvas.getContext("2d").drawImage(video,0,0);

    let img = canvas.toDataURL("image/jpeg", 0.7);

    images[keys[step]] = img;

    step++;

    if(step < 3){
        document.getElementById("stepTitle").innerText =
            "Capture " + steps[step] + " Face";
        return;
    }

    if(!images.left || !images.center || !images.right){
        alert("Please capture all 3 images properly.");
        resetCapture();
        return;
    }

    // STOP CAMERA
    if(video.srcObject){
        video.srcObject.getTracks().forEach(track => track.stop());
    }

    // ✅ SHOW LOADER
    const loader = document.getElementById("loadingScreen");
    if(loader){
        loader.style.display = "flex";
    }

    // ✅🔥 FORCE UI RENDER (FINAL FIX)
    setTimeout(() => {
    requestAnimationFrame(() => {
        sendToBackend(images);
    });
    }, 50);
}

// RESET
function resetCapture(){
    step = 0;

    images = {
        left: null,
        center: null,
        right: null
    };

    document.getElementById("stepTitle").innerText = "Capture LEFT Face";
}

// PAGE LOAD RESET
window.addEventListener("load", () => {
    resetCapture();
});