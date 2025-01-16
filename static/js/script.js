// script.js

// The URL of your Flask backend hosted on Render
const apiUrl = "https://fud-project.onrender.com"; // Replace with your actual backend URL

document.addEventListener("DOMContentLoaded", function () {
    // Button click handler
    const button = document.getElementById("myButton");
    button.addEventListener("click", function () {
        alert("Button clicked!");
    });

    // Form submission handler
    const form = document.querySelector("#loginForm"); // Adjust the form ID as needed

    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Collect form data
            const formData = new FormData(form);
            const data = {
                username: formData.get("username"),
                password: formData.get("password"),
            };

            try {
                // Send the data to the Flask backend
                const response = await fetch(`${apiUrl}/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(`Login successful: ${result.message}`);
                    // Redirect or perform further actions
                    window.location.href = "/dashboard"; // Example redirect
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.message}`);
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while connecting to the server.");
            }
        });
    }
});
