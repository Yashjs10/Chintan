async function postData(url = "", data = {}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

document.addEventListener("DOMContentLoaded", () => {
    // Select all buttons with the same ID
    const sendButtons = document.querySelectorAll("#sendButton");

    sendButtons.forEach((sendButton) => {
        sendButton.addEventListener("click", async () => {
            // Get the question input and clear it
            const questionInput = document.getElementById("questionInput");
            let question = "";
            if (questionInput) {
                question = questionInput.value; // Store the value
                questionInput.value = ""; // Clear the input
            }

            // Update the SVG or perform any action (currently unused)
            const sendButtonSvg = sendButton.querySelector("svg");
            if (sendButtonSvg) {
                // Perform actions with the SVG element if needed
            }

            // Update styles for `.right1` and `.right2` elements
            const right2 = document.querySelector(".right2");
            const right1 = document.querySelector(".right1");
            if (right2 && right1) {
                right2.style.display = "block";
                right1.style.display = "none";
            }

            // Update both `question` and `question1` elements
            const questionDisplay = document.getElementById("question");
            const question1Display = document.getElementById("question1");

            if (questionDisplay) {
                questionDisplay.innerHTML = question; // Update `question` text
            }
            if (question1Display) {
                question1Display.innerHTML = question; // Update `question1` text
            }

            // Call the API with the question
            let result = await postData("/api", { "question": question });

            // Define the solution element
            let solution = document.getElementById("answer");  // Ensure this element exists in your HTML

            // Check if solution element exists before trying to update it
            if (solution) {
                solution.innerHTML = result.answer;
            } else {
                console.error("Solution element not found.");
            }
        });
    });
});
