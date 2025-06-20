function toggleVisibility(fieldId, icon) {
    const input = document.getElementById(fieldId);
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈";
    } else {
        input.type = "password";
        icon.textContent = "👁️";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const feedback = document.getElementById("strength-text");

    passwordInput.addEventListener("input", function () {
        const pwd = passwordInput.value;
        let score = 0;

        if (pwd.length >= 8) score++;
        if (/[a-z]/.test(pwd)) score++;
        if (/[A-Z]/.test(pwd)) score++;
        if (/\d/.test(pwd)) score++;
        if (/[^A-Za-z0-9]/.test(pwd)) score++;

        if (score <= 2) {
            feedback.textContent = "Weak";
            feedback.style.color = "red";
        } else if (score === 3) {
            feedback.textContent = "Moderate";
            feedback.style.color = "orange";
        } else {
            feedback.textContent = "Strong";
            feedback.style.color = "green";
        }
    });
});




