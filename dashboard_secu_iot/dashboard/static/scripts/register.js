import { register, validate_password, check_password } from "./auth.js";

document
    .getElementById("register-form")
    .addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirm_password =
            document.getElementById("confirm-password").value;

        await register(email, password, confirm_password);
    });

document
    .getElementById("register-form")
    .addEventListener("input", async (e) => {
        e.preventDefault();
        console.log("Change event triggered");

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirm_password =
            document.getElementById("confirm-password").value;
        const registerButton = document.getElementById("register-button");

        if (
            email.length > 0 &&
            password.length > 0 &&
            validate_password() &&
            confirm_password.length > 0 &&
            check_password()
        ) {
            registerButton.disabled = false;
            registerButton.classList.remove(
                "cursor-not-allowed",
                "bg-indigo-400"
            );
            registerButton.classList.add("bg-indigo-600");
            console.log("Enabled");
        } else {
            registerButton.disabled = true;
            registerButton.classList.add("cursor-not-allowed", "bg-indigo-400");
            registerButton.classList.remove("bg-indigo-600");
            console.log("Disabled");
        }
    });
