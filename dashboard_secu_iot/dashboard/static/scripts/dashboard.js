import { loadVideo } from "./load_video.js";

loadVideo();

document
    .getElementById("video-container")
    .addEventListener("click", (event) => {
        if (event.target.classList.contains("intrusion-btn")) {
            event.preventDefault();
            const video_id = event.target.getAttribute("data-video-id");
            const intrusion = true;

            fetch("/video/set_intrusion", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ video_id, intrusion }),
            })
                .then(() => {
                    const card = event.target.closest(".video-card");
                    if (card) card.remove();
                })
                .catch((error) => console.error("Error:", error));
        }
    });

document
    .getElementById("video-container")
    .addEventListener("click", (event) => {
        if (event.target.classList.contains("not-intrusion-btn")) {
            event.preventDefault();
            const video_id = event.target.getAttribute("data-video-id");
            const intrusion = false;

            fetch("/video/set_intrusion", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ video_id, intrusion }),
            })
                .then(() => {
                    const card = event.target.closest(".video-card");
                    if (card) card.remove();
                })
                .catch((error) => console.error("Error:", error));
        }
    });
