"use strict";

// Grab pathname from browser
const tripPath = window.location.pathname
console.log(tripPath)

// Slice pathname string to just include the trail_id
const trip_id = tripPath.slice(6)
console.log(trip_id)


// function initMap() {
//     $.get(`/json/latlongbyid/${trail_id}`, (res) => {
//         const map = new google.maps.Map(
//             document.querySelector("#map-container"), {
//                 center: res,
//                 zoom: 15,
//             },
//         );
//         const newMarker = new google.maps.Marker({
//             position: res,
//             map: map
//         });
//     });
// };
