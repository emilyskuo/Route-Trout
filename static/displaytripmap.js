"use strict";

// Grab pathname from browser
const tripPath = window.location.pathname

// Slice pathname string to just include the trail_id
const trip_id = tripPath.slice(6)

function initMap() {
    $.get(`/json/tripcoords`, {trip_id: trip_id}, (res) => {
        const map = new google.maps.Map(
            document.querySelector("#tripmapdiv"), {
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
