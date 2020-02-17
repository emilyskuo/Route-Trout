"use strict";

const trail_name = $("#trail-name").html();

console.log(trail_name);

function initMap() {
    $.get(`/json/latlongbyid/${trail_name}`, (res) => {
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
