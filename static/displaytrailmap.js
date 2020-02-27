"use strict";

// Grab pathname from browser
const path = window.location.pathname

// Slice pathname string to just include the trail_id
const trail_id = path.slice(7)

function initMap() {
    $.get(`/json/latlongbyid/${trail_id}`, (res) => {
        const map = new google.maps.Map(
            document.querySelector("#trail-map-container"), {
                center: res,
                zoom: 15,
            },
        );
        const newMarker = new google.maps.Marker({
            position: res,
            map: map
        });
    });
};
