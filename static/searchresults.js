"use strict";

const fourPassLoop = {
    lat: 39.0985,
    lng: -106.9407
};

function initMap() {
    const map = new google.maps.Map(
        document.getElementById("map-container"), 
        {zoom: 10, 
        center: fourPassLoop
        }
    );
    const marker = new google.maps.Marker(
        {position: fourPassLoop, 
         map: map
        }
    );
}

const params = (new URL(document.location)).searchParams;
const search = params.get("search");

$.get(`/json/search`, {search: search}, (res) => {
    console.log(res);
    for (const trail of res) {
        console.log(trail.name);
        $("#trail-list").append(`<li><a href="/trail/${trail.id}">${trail.name}</li>`);
    }
});