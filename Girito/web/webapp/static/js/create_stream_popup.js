document.addEventListener("DOMContentLoaded", function () {
    const showPopupButton = document.getElementById("show-popup");
    const popupContainer = document.getElementById("popup-container");
    const closePopupButton = document.getElementById("close-popup");
    const createTransmisionButton = document.getElementById("create-transmision-button");

    showPopupButton.addEventListener("click", function () {
        popupContainer.style.display = "block";
    });

    closePopupButton.addEventListener("click", function () {
        popupContainer.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === popupContainer) {
            popupContainer.style.display = "none";
        }
    });

    popupContainer.addEventListener("click", function (event) {
        event.stopPropagation();
    });

    // Add event listener to the "Crear transmisión" button
    createTransmisionButton.addEventListener("click", function () {
        popupContainer.style.display = "none"; // Close the popup
    });
});
