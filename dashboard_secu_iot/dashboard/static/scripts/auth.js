export async function register(email, password, confirm_password) {
    return await fetch("/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, confirm_password }),
        redirect: "follow",
    }).then((res) => {
        if (res.status === 200) {
            window.location.href = res.url;
        } else {
            document.getElementById("email").value = "";
            document.getElementById("password").value = "";
            document.getElementById("confirm-password").value = "";
        }
    });
}

export async function login(email, password) {
    return await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    }).then((res) => {
        if (res.status === 200) {
            window.location.href = res.url;
        } else {
            document.getElementById("email").value = "";
            document.getElementById("password").value = "";
        }
    });
}

export async function logout() {
    return await fetch("/auth/logout", {
        method: "POST",
    }).then((res) => (window.location.href = res.url));
}

export async function validate_password() {
    const pwd = document.getElementById("password").value;
    let issues = [];

    if (pwd.length < 8) {
        issues.push("Must be at least 8 characters long.");
    }
    if (pwd.length > 64) {
        issues.push("Must be at most 64 characters long.");
    }
    if (!/[A-Z]/.test(pwd)) {
        issues.push("Must contain at least one uppercase letter.");
    }
    if (!/[a-z]/.test(pwd)) {
        issues.push("Must contain at least one lowercase letter.");
    }
    if (!/[0-9]/.test(pwd)) {
        issues.push("Must contain at least one number.");
    }
    if (!/[^A-Za-z0-9]/.test(pwd)) {
        issues.push("Must contain at least one special character.");
    }
    if (/password|123456|qwerty/i.test(pwd)) {
        issues.push("Cannot contain common passwords.");
    }

    pushError(issues);

    return issues.length === 0;
}

function pushError(issues) {
    const errorsList = document.getElementById("errors");

    errorsList.innerHTML = "";
    if (issues.length === 0 && pwd) {
        errorsList.innerHTML = `<li class='text-green-600 flex items-center gap-2'>✅ Strong password!</li>`;
    } else {
        issues.forEach((issue) => {
            errorsList.innerHTML += `<li class='text-red-600 flex items-center gap-2'>❌ ${issue}</li>`;
        });
    }
}

export async function check_password() {
    const pwd = document.getElementById("password").value;
    const confirm_pwd = document.getElementById("confirm-password").value;
    let issues = [];

    if (pwd !== confirm_pwd) {
        issues.push("Passwords do not match.");
    }
    const errorsList = document.getElementById("password-check");
    errorsList.innerHTML = "";
    if (issues.length === 0 && pwd) {
        errorsList.innerHTML = `<li class='text-green-600 flex items-center gap-2'>✅ Passwords match!</li>`;
    } else {
        issues.forEach((issue) => {
            errorsList.innerHTML += `<li class='text-red-600 flex items-center gap-2'>❌ ${issue}</li>`;
        });
    }

    return issues.length === 0;
}
