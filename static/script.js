
const searchInput = document.getElementById("searchInput");
const recipeCards = document.querySelectorAll(".recipe-card");
const noResults = document.getElementById("noResults");

searchInput.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();
    let visibleCount = 0;

    recipeCards.forEach(function (card) {
        const matches = card.textContent.toLowerCase().includes(query);
        card.hidden = !matches;

        if (matches) {
            visibleCount++;
        }
    });

    noResults.hidden = visibleCount !== 0;
});

const substituteBtn = document.getElementById("substituteBtn");
const ingredientInput = document.getElementById("ingredientInput");
const substitutionResult = document.getElementById("substitutionResult");

substituteBtn.addEventListener("click", async function () {
    const ingredient = ingredientInput.value.trim();

    if (!ingredient) {
        substitutionResult.textContent = "Please enter an ingredient first.";
        return;
    }

    substitutionResult.textContent = "Finding alternatives...";

    try {
        const response = await fetch("/api/substitute", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredient: ingredient })
        });

        const data = await response.json();

        substitutionResult.replaceChildren();

        const heading = document.createElement("h3");
        heading.textContent = "Possible substitutes";
        substitutionResult.appendChild(heading);

        const result = document.createElement("p");
        result.textContent = data.substitutes
            ? data.substitutes.join(", ")
            : data.error || "No alternatives found.";
        substitutionResult.appendChild(result);
    } catch (error) {
        substitutionResult.textContent =
            "Unable to connect. Please try again.";
    }
});

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");

function addMessage(text, className) {
    const message = document.createElement("div");
    message.className = "message " + className;
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const ingredients = chatInput.value.trim();

    if (!ingredients) return;

    addMessage(ingredients, "user-message");
    chatInput.value = "";
    chatInput.disabled = true;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: ingredients })
        });

        const data = await response.json();

        addMessage(
            data.reply || data.error || "No response received.",
            "bot-message"
        );
    } catch (error) {
        addMessage("Unable to connect. Please try again.", "bot-message");
    } finally {
        chatInput.disabled = false;
        chatInput.focus();
    }
});
