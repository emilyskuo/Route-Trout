"use strict";

// Grab pathname from browser
const tripPath = window.location.pathname

// Slice pathname string to just include the trail_id
const trip_id = tripPath.slice(6)

// Select 2 code
$(document).ready(function() {
    $("#add-users-to-trip").select2();
});
$(document).ready(function() {
    $("#remove-users-from-trip").select2();
});
$(document).ready(function() {
    $("#remove-trip-trails").select2();
});

// Event listeners for editing Trip Name
const editNameButton = $("#edit-trip-name-button");
const editNameDiv = $("#edit-trip-name-div");
const editNameSubmit = $("#edit-trip-name-submit");
const tripNameH = $("#trip-name-h")

editNameButton.on("click", () => {
    editNameDiv.toggle();
});

editNameSubmit.on("click", (evt) => {
    evt.preventDefault();
    const trip_name = $("#trip_name").val()
    $.post("/updatetripname", {trip_id: trip_id, trip_name: trip_name}, (res) => {
        if (res === "An error has occurred") {
            alert(res);
        } else {
            tripNameH.html(res);
            editNameDiv.toggle();
        };
    })
});

// Event listeners for editing Trip Accommodations
const editAccomButton = $("#edit-trip-accom-button");
const editAccomDiv = $("#edit-trip-accom-div");
const editAccomSubmit = $("#edit-trip-accom-submit");
const tripAccomP = $("#trip-accom-p")

editAccomButton.on("click", () => {
    editAccomDiv.toggle();
    tripAccomP.toggle();
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
            editAccomDiv.toggle();
            tripAccomP.toggle();
            // Refresh map with new coordinates
            initMap();
            // Update "Search for trails nearby" link
            $("#trip-trail-search-a").attr("href", `/search?search=${res}`)
        }
    });
});

// Event listener for Trip Participants edit button

const editUsersButton = $("#edit-trip-users-button");
const editUsersDiv = $("#add-remove-trip-users-div");

editUsersButton.on("click", () => {
    editUsersDiv.toggle();
});

// Event listeners for adding Trip Participants

const addUsersButton = $("#add-users-to-trip-button");
const addUsersSelect = $("#add-users-to-trip");
const tripUserUL = $("#trip-user-ul");

addUsersButton.on("click", (evt) => {
    evt.preventDefault();
    const list_users_selected = addUsersSelect.val();
    for (const user_id of list_users_selected) {
        $.post("/addtripusers", {trip_id: trip_id, user_id: user_id}, (res) => {
            if (res === "User already added to trip") {
                alert(res);
            } else {
                tripUserUL.append(`<li>${res}</li>`);
            };
        });
    };
    editUsersDiv.toggle();
});

// Event listeners for removing Trip Participants

const delUsersButton = $("#remove-users-from-trip-button");
const delUsersSelect = $("#remove-users-from-trip");

delUsersButton.on("click", (evt) => {
    evt.preventDefault();
    const users_to_del = delUsersSelect.val();
    for (const user_id of users_to_del) {
        $.post("/removetripusers", {trip_id: trip_id, user_id: user_id}, (res) => {
            if (res === "An error has occurred") {
                alert(res);
            } else {
                $(`#${res}`).remove();
            };
        });
    };
    editUsersDiv.toggle();
});


// Event listener for Remove Trails button

const editTrailsButton = $("#edit-trip-trails-button");
const editTrailsDiv = $("#remove-trip-trails-div");


editTrailsButton.on("click", () => {
    editTrailsDiv.toggle();
});

const remTrailsButton = $("#remove-trip-trails-button");
const remTrailsSelect = $("#remove-trip-trails");

remTrailsButton.on("click", (evt) => {
    evt.preventDefault();
    const trails_to_del = remTrailsSelect.val();
    for (const trail_id of trails_to_del) {
        $.post("/removetriptrails", {trip_id: trip_id, trail_id: trail_id}, (res) => {
            if (res === "An error has occurred") {
                alert(res);
            } else {
                $(`#${res}`).remove();
            };
        });
    };
    editTrailsDiv.toggle();
    initMap();
});

// Event listeners for Archive & Unarchive buttons

const archiveButton = $("#archive-trip");
const unarchiveButton = $("#unarchive-trip");

$.get("/istriparchived", {trip_id: trip_id}, (res) => {
    if (res === "true") {
        archiveButton.toggle();
        unarchiveButton.toggle();
    };
});

archiveButton.on("click", () => {
    $.post("/archivetrip", {trip_id: trip_id}, () => {
        archiveButton.toggle();
        unarchiveButton.toggle();
    });
});
unarchiveButton.on("click", () => {
    $.post("/unarchivetrip", {trip_id: trip_id}, () => {
        archiveButton.toggle();
        unarchiveButton.toggle();
    });
});


// Event listener for Delete button

const deleteTripButton = $("#first-delete-trip-button");
const deleteTripDiv = $("#confirm-delete-trip-div");

deleteTripButton.on("click", () => {
    deleteTripDiv.toggle();
});