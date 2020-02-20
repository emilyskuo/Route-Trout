"use strict";

const saveButton = $("#save-button")
const completeButton = $("#complete-button")

// Grab pathname from browser
const path1 = window.location.pathname

// Slice pathname string to just include the trail_id
const trail_id1 = path1.slice(7)

saveButton.on("click", () => {
    $.post("/user/save-trail", {trail_id: trail_id1}, (res) => {
        alert(res);
        saveButton.addClass("disabled");
        });
});

completeButton.on("click", () => {
    console.log("hi")
    $.post("/user/complete-trail", {trail_id: trail_id1}, (res) => {
        alert(res);
        completeButton.addClass("disabled");
        saveButton.addClass("disabled");
        });
});