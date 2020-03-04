"use strict";

// Grab pathname from browser
const tripPath = window.location.pathname

// Slice pathname string to just include the trail_id
const trip_id = tripPath.slice(6)

// Select 2 code
$(document).ready(function() {
    $("#add-users-to-trip").select2();
});

// Event listeners for editing Trip Accommodations
const editAccomButton = $("#edit-trip-accom-button");
const editAccomDiv = $("#edit-trip-accom-div");
const editAccomSubmit = $("#edit-trip-accom-submit");
const tripAccomP = $("#trip-accom-p")

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
            // Update html in <p>
            tripAccomP.html(res);
            // Hide edit form & unhide tripAccomP
            editAccomDiv.addClass("hidden");
            tripAccomP.removeClass("hidden");
            // Refresh map with new coordinates
            initMap();
            // Update "Search for trails nearby" link
            $("#trip-trail-search-a").attr("href", `/search?search=${res}`)
        }
    });
});

// Event listeners for updating Trip Participants

const addUsersButton = $("#add-users-to-trip-button");
const addUsersSelect = $("#add-users-to-trip");

console.log(addUsersSelect.val())

addUsersButton.on("click", (evt) => {
    evt.preventDefault();
    const list_users_selected = addUsersSelect.val();
    // for (user_id of list_users_selected) {

    // }
});


// Event listeners for Archive & Unarchive buttons
const archiveButton = $("#archive-trip");
const unarchiveButton = $("#unarchive-trip");

archiveButton.on("click", () => {
    $.post("/archivetrip", {trip_id: trip_id}, (res) => {
        archiveButton.addClass("hidden");
        unarchiveButton.removeClass("hidden");
    });
});
unarchiveButton.on("click", () => {
    $.post("/unarchivetrip", {trip_id: trip_id}, (res) => {
        archiveButton.removeClass("hidden");
        unarchiveButton.addClass("hidden");
    });
});