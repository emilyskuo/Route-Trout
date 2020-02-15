"use strict";

const trail_name = $("#trail-name").html();

console.log(trail_name);

function initMap() {
    const map = new google.maps.Map(
        document.getElementById("map-container"), {
            center: {
                lat: 37.601773, 
                lng: -122.202870
            },
            zoom: 11,
        },
    );
    
    $.get(`/json/latlongbyid/${trail_name}`, (res) => {
        map.setCenter(res);
        console.log(res);
        const newMarker = new google.maps.Marker({
            position: res,
            map: map
        });
    });
}


// const marker = new google.maps.Marker(
//     {position: current_trail, 
//     map: map
//     }
// );
// }

// console.log(current_trail_jquery);

// console.log(current_trail_jquery["responseJSON"]);

// console.log(current_trail_jquery.responseJSON);

// const current_trail = current_trail_jquery["responseJSON"];

// console.log(current_trail);


