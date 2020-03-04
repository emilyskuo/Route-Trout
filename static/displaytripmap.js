"use strict";

// Grab pathname from browser
const tripPath = window.location.pathname

// Slice pathname string to just include the trail_id
// const trip_id = tripPath.slice(6)

const houseIcon = "/static/images/house.png"

function initMap() {
    $.get(`/json/tripinfo`, {trip_id: trip_id}, (res) => {
        const map = new google.maps.Map(
            document.querySelector("#tripmapdiv"), {
                center: res.lat_long,
                zoom: 13,
            },
        );
        const newMarker = new google.maps.Marker({
            position: res.lat_long,
            map: map,
            icon: houseIcon
        });
        const infowindow = new google.maps.InfoWindow({
            content: `<b>Trip Accommodations:</b> ${res.accom_text}`,
        });
        newMarker.addListener("click", () => {
            infowindow.open(newMarker.get("map"), newMarker);
        });

        for (const trail of res.trip_trails) {
            console.log(trail)
            const trailMarker = new google.maps.Marker({
                position: trail.trail_lat_long,
                map: map,
            });
            const trailWindow = new google.maps.InfoWindow({
                content: `<b>Trail:</b> <a href="/trail/${trail.trail_id}">${trail.trail_name}</a>`
            });
            trailMarker.addListener("click", () => {
                trailWindow.open(trailMarker.get("map"), trailMarker);
            });
        };

    });
};
