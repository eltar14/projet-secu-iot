import { logout } from "./auth.js";

document.getElementById("btn-logout").addEventListener("click", async () => {
    await logout();
});

document
    .getElementById("btn-mobile-menu")
    .addEventListener("click", async () => {
        const iconMenu = document.getElementById("icon-menu");
        const iconClose = document.getElementById("icon-close");
        const mobileMenu = document.getElementById("mobile-menu");

        if (iconMenu.classList.contains("block")) {
            iconMenu.classList.remove("block");
            iconMenu.classList.add("hidden");
            iconClose.classList.remove("hidden");
            iconClose.classList.add("block");
            mobileMenu.classList.remove("hidden");
        } else {
            iconMenu.classList.remove("hidden");
            iconMenu.classList.add("block");
            iconClose.classList.remove("block");
            iconClose.classList.add("hidden");
            mobileMenu.classList.add("hidden");
        }
    });
