const modeCards = document.querySelectorAll(".mode-card");

const rangeMinInput = document.getElementById("range-min");
const rangeMaxInput = document.getElementById("range-max");


modeCards.forEach((card) => {

    card.addEventListener("click", async () => {

        const mode = card.dataset.mode;

        const rangeMin = Number(rangeMinInput.value);
        const rangeMax = Number(rangeMaxInput.value);

        if (rangeMin >= rangeMax) {
            alert("Minimum must be less than maximum.");
            return;
        }

        if (mode === "single_player") {

            await startSinglePlayer(
                rangeMin,
                rangeMax
            );

            return;
        }

        alert(
            `${card.querySelector(".mode-title").textContent}\n\n` +
            "This mode is coming next! 🎯"
        );
    });

});


async function startSinglePlayer(rangeMin, rangeMax) {

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
                data.error || "Unable to create game."
            );
        }

        console.log("Game created:", data);

        window.location.href =`/games/single-player?game_id=${data.game_id}`;

    } catch (error) {

        console.error(error);

        alert(
            error.message
        );
    }
}