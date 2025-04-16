function createVideoCard(video, intrusion = false) {
    const card = document.createElement("div");
    card.className =
        "video-card bg-white border border-gray-200 rounded-lg shadow-sm dark:bg-gray-800 dark:border-gray-700";

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
            <video class="rounded-t-lg w-full aspect-4/3" controls>
                <source src="${video.file_path}" type="video/mp4" />
                Your browser does not support the video tag.
            </video>
            <div class="p-5">
                <h5 class="mb-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white">${formattedDate}</h5>
                <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">${
                    video.description
                }</p>
                ${
                    intrusion
                        ? ""
                        : `<div class="flex justify-between mt-4">
                            <button data-video-id="${video.id}" class="intrusion-btn inline-flex items-center px-3 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-800">
                                Intrusion
                            </button>
                            <button data-video-id="${video.id}" class="not-intrusion-btn inline-flex items-center px-3 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 dark:bg-green-500 dark:hover:bg-green-600 dark:focus:ring-green-800">
                                Not Intrusion
                            </button>
                          </div>`
                }
            </div>
    `;
    return card;
}

export async function loadVideo(intrusion = false) {
    try {
        const container = document.getElementById("video-container");

        const videos = intrusion
            ? await fetch("/video/get_intrusion").then((res) => res.json())
            : await fetch("/video/get").then((res) => res.json());

        container.innerHTML = "";
        console.log(videos);

        videos.forEach((video) => {
            const card = createVideoCard(video, intrusion);
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error loading videos:", error);
    }
}
