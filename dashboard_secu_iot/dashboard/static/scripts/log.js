document.addEventListener("DOMContentLoaded", function () {
    const cancelButtons = document.querySelectorAll(".cancel-video");
    cancelButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const videoId = this.getAttribute("data-video-id");
            fetch("/video/cancel_intrusion", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ video_id: videoId }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    location.reload();
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        });
    });
});
