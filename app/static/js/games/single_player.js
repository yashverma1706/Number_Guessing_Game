const params = new URLSearchParams(window.location.search);
const gameId = params.get("game_id");

const rangeText = document.getElementById("range-text");
const attemptsElement = document.getElementById("attempts");
const scoreElement = document.getElementById("score");
const statusElement = document.getElementById("status");

const messageElement = document.getElementById("message");
const guessInput = document.getElementById("guess-input");
const guessButton = document.getElementById("guess-button");

const resultCard = document.getElementById("result-card");
const resultTitle = document.getElementById("result-title");
const resultMessage = document.getElementById("result-message");

const backButton = document.getElementById("back-button");
const rematchButton = document.getElementById("rematch-button");
const homeButton = document.getElementById("home-button");


let rangeMin = 1;
let rangeMax = 100;


/* =========================================
   INITIALIZE GAME
   ========================================= */

async function loadGame() {

    if (!gameId) {
        messageElement.textContent =
            "No game was selected.";

        guessButton.disabled = true;
        return;
    }

    try {

        const response = await fetch(
            `/api/games/${gameId}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to load game."
            );
        }

        rangeMin = data.range_min;
        rangeMax = data.range_max;

        rangeText.textContent =
            `Guess a number between ${rangeMin} and ${rangeMax}.`;

        attemptsElement.textContent =
            data.attempts || 0;

        updateScore(data.attempts || 0);

        if (data.status !== "active") {
            finishGame(data);
        }

    } catch (error) {

        console.error(error);

        messageElement.textContent =
            error.message;

        guessButton.disabled = true;
    }
}


/* =========================================
   MAKE GUESS
   ========================================= */

async function makeGuess() {

    const guess = Number(
        guessInput.value
    );

    if (!Number.isInteger(guess)) {

        messageElement.textContent =
            "Please enter a valid number.";

        return;
    }

    if (guess < rangeMin || guess > rangeMax) {

        messageElement.textContent =
            `Enter a number between ${rangeMin} and ${rangeMax}.`;

        return;
    }

    guessButton.disabled = true;

    try {

        const response = await fetch(
            `/api/games/${gameId}/guess`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    player_id: 1,
                    guess: guess
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to submit guess."
            );
        }

        handleGuessResult(data);

    } catch (error) {

        console.error(error);

        messageElement.textContent =
            error.message;

    } finally {

        if (statusElement.textContent === "Playing") {
            guessButton.disabled = false;
        }
    }
}


/* =========================================
   HANDLE RESULT
   ========================================= */

function handleGuessResult(data) {

    if (data.attempts !== undefined) {

        attemptsElement.textContent =
            data.attempts;

        updateScore(data.attempts);
    }

    if (data.result === "higher") {

        messageElement.textContent =
            "⬆️ Try a higher number.";

    } else if (data.result === "lower") {

        messageElement.textContent =
            "⬇️ Try a lower number.";

    } else if (data.result === "correct") {

        statusElement.textContent =
            "Won";

        messageElement.textContent =
            "🎉 Correct!";

        finishGame(data);
    }
}


/* =========================================
   SCORE
   ========================================= */

function updateScore(attempts) {

    const baseScore = 1000;
    const penalty = attempts * 50;

    const score = Math.max(
        baseScore - penalty,
        0
    );

    scoreElement.textContent = score;
}


/* =========================================
   FINISH GAME
   ========================================= */

function finishGame(data) {

    guessButton.disabled = true;
    guessInput.disabled = true;

    statusElement.textContent =
        "Won";

    resultCard.classList.remove("hidden");

    resultTitle.textContent =
        "You Won! 🎉";

    const attempts =
        data.attempts || attemptsElement.textContent;

    const score =
        data.score !== undefined
            ? data.score
            : scoreElement.textContent;

    resultMessage.textContent =
        `You found the number in ${attempts} attempts with a score of ${score}.`;
}


/* =========================================
   NAVIGATION
   ========================================= */

backButton.addEventListener(
    "click",
    () => {
        window.location.href = "/";
    }
);


homeButton.addEventListener(
    "click",
    () => {
        window.location.href = "/";
    }
);


rematchButton.addEventListener(
    "click",
    startRematch
);


async function startRematch() {

    rematchButton.disabled = true;

    try {

        const response = await fetch(
            "/api/games/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    mode: "single_player",
                    player1_id: 1,
                    range_min: rangeMin,
                    range_max: rangeMax
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Unable to start rematch."
            );
        }

        window.location.href =
            `/games/single-player?game_id=${data.game_id}`;

    } catch (error) {

        console.error(error);

        rematchButton.disabled = false;

        alert(error.message);
    }
}


guessButton.addEventListener(
    "click",
    makeGuess
);


guessInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {
            makeGuess();
        }

    }
);


/* =========================================
   START
   ========================================= */

loadGame();