"use strict";

const path = window.location.pathname
const trail_id = path.slice(7)

console.log(trail_id)

function initMap() {
    $.get(`/json/latlongbyid/${trail_id}`, (res) => {
        const map = new google.maps.Map(
            document.querySelector("#map-container"), {
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
