"use strict";

$(document).ready(function() {
    $("#add-users-to-trip").select2();
});

// $("#add-users-to-trip-button").on("submit", (evt) => {
//     evt.preventDefault();

// })

const editAccomButton = $("#edit-trip-accom-button");
const editAccomForm = $("#edit-trip-accom-form");
const editAccomDiv = $("#edit-trip-accom-div");
const editAccomSubmit = $("#edit-trip-accom-submit");
const tripAccomP = $("trip-accom-p")

editAccomButton.on("click", () => {
    editAccomDiv.removeClass("hidden");
    tripAccomP.addClass("hidden");
});

editAccomSubmit.on("click", (evt) => {
    evt.preventDefault();
    const trip_accom = $("#trip_accom").val()
    $.post("/updatetripaccoms", {trip_id: trip_id, trip_accom: trip_accom}, (res) => {
        if (res === "Address could not be read") {
            alert(res);
        } else {
            tripAccomP.html(res);
            editAccomDiv.addClass("hidden");
            tripAccomP.removeClass("hidden");
            initMap()
        }
    });
});