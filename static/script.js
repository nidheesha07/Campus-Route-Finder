// script.js
// This file adds small interactive touches to the Campus Route Finder.

document.addEventListener("DOMContentLoaded", function () {
    // 1. Fade in the main card smoothly when a page loads.
    const card = document.querySelector(".card");
    if (card) {
        card.style.opacity = "0";
        setTimeout(function () {
            card.style.transition = "opacity 0.4s ease-in";
            card.style.opacity = "1";
        }, 50);
    }

    // 2. On the "locations" page, warn the user immediately if they pick
    // the same start and destination, instead of waiting for the server.
    const startSelect = document.getElementById("start");
    const endSelect = document.getElementById("end");
    const form = startSelect ? startSelect.closest("form") : null;

    if (startSelect && endSelect && form) {
        form.addEventListener("submit", function (event) {
            if (startSelect.value === endSelect.value) {
                event.preventDefault();
                alert("Please choose two different locations.");
            }
        });
    }
});