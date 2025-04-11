import { loadVideo } from "./load_video.js";

loadVideo();

document
    .getElementById("video-container")
    .addEventListener("click", (event) => {
        if (event.target.classList.contains("intrusion-btn")) {
            event.preventDefault();
            const videoId = event.target.getAttribute("data-video-id");
            console.log(videoId);
        }
    });

document
    .getElementById("video-container")
    .addEventListener("click", (event) => {
        if (event.target.classList.contains("not-intrusion-btn")) {
            event.preventDefault();
            const videoId = event.target.getAttribute("data-video-id");
            console.log(videoId);
        }
    });
