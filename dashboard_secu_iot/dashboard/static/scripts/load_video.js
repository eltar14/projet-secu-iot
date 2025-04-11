function createVideoCard(video, intrusion = false) {
    const card = document.createElement("div");
    card.className = "bg-white rounded-2xl shadow-lg p-4";

    const date = new Date(video.timestamp);
    const formattedDate = date.toLocaleString("fr-FR", {
        day: "2-digit",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });

    card.innerHTML = `
        <h3 class="text-lg font-semibold mb-2">${formattedDate}</h3>
        <video class="w-full rounded-lg" controls>
            <source src="${video.file_path}" type="video/mp4" />
            Your browser does not support the video tag.
        </video>
        ${
            intrusion
                ? ""
                : `<div class="flex justify-between mt-4">
                    <button data-video-id="${video.id}" class="intrusion-btn px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">Intrusion</button>
                    <button data-video-id="${video.id}" class="not-intrusion-btn px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600">Not Intrusion</button>
                  </div>`
        }
    `;
    return card;
}

export async function loadVideo(intrusion = false) {
    try {
        const response = intrusion
            ? await fetch("/video/get_intrusion")
            : await fetch("/video/get");
        const videos = await response.json();

        const container = document.getElementById("video-container");
        container.innerHTML = "";

        videos.forEach((video) => {
            const card = createVideoCard(video, intrusion);
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading videos:", error);
    }
}
