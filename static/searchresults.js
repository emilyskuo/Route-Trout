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


console.log(window.location)
console.log(window.location.pathname)
console.log(window.location.search)

let params = (new URL(document.location)).searchParams;
let search = params.get("search");

console.log(params)
console.log(search)

$.get(`/json/search`, {search: search}, (res) => {
    console.log(res);
});