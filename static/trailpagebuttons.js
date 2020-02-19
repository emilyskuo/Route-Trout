"use strict";

const saveButton = $("#save-button")
const completeButton = $("#complete-button")

// Grab pathname from browser
const path1 = window.location.pathname

// Slice pathname string to just include the trail_id
const trail_id1 = path1.slice(7)

saveButton.on("click", () => {
    alert("button clicked");
    $.post("/user/save-trail", {trail_id: trail_id1}, (res) => {
        console.log(res);
        });
});