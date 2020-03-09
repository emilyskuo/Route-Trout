"use strict";

const saveButton = $("#save-button")
const completeButton = $("#complete-button")
const unsaveButton = $("#unsave-button")
const uncompleteButton = $("#uncomplete-button")
const tripsButton = $("#add-trips-span")

// Grab pathname from browser
const path1 = window.location.pathname

// Slice pathname string to just include the trail_id
const trail_id1 = path1.slice(7)

$.get("/user/loggedin", (res) => {
    if (res === "false") {
        saveButton.addClass("hidden");
        unsaveButton.addClass("hidden");
        completeButton.addClass("hidden");
        uncompleteButton.addClass("hidden");
        tripsButton.addClass("hidden");
    }
});


$.get(`/user/is-trail-saved/${trail_id1}`, (res) => {
    if (res.completed === true) {
        saveButton.addClass("hidden");
        unsaveButton.removeClass("hidden");
        completeButton.addClass("hidden");
        uncompleteButton.removeClass("hidden");
    } else if (res.saved === true) {
        saveButton.addClass("hidden");
        unsaveButton.removeClass("hidden");
    }
});

saveButton.on("click", () => {
    $.post("/user/save-trail", {trail_id: trail_id1}, (res) => {
        saveButton.addClass("hidden");
        unsaveButton.removeClass("hidden")
        });
});

unsaveButton.on("click", () => {
    $.post("/user/unsave-trail", {trail_id: trail_id1}, (res) => {
        unsaveButton.addClass("hidden");
        saveButton.removeClass("hidden")
        completeButton.removeClass("hidden")
        uncompleteButton.addClass("hidden")
        });
});

completeButton.on("click", () => {
    $.post("/user/complete-trail", {trail_id: trail_id1}, (res) => {
        completeButton.addClass("hidden");
        saveButton.addClass("hidden");
        unsaveButton.removeClass("hidden");
        uncompleteButton.removeClass("hidden")
        });
});

uncompleteButton.on("click", () => {
    $.post("/user/uncomplete-trail", {trail_id: trail_id1}, (res) => {
        uncompleteButton.addClass("hidden");
        completeButton.removeClass("hidden");
        });
});