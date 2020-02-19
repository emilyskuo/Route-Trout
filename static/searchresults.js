"use strict";

// const fourPassLoop = {
//     lat: 39.0985,
//     lng: -106.9407
// };

// function initMap() {
//     const map = new google.maps.Map(
//         document.getElementById("map-container"), 
//         {zoom: 10, 
//         center: fourPassLoop
//         }
//     );
//     const marker = new google.maps.Marker(
//         {position: fourPassLoop, 
//          map: map
//         }
//     );
// }

const params = (new URL(document.location)).searchParams;
const search = params.get("search");

function initMap() {
    $.get(`/json/search-coords`, {search: search}, (res) => {
        const map = new google.maps.Map(
            document.querySelector("#map-container"),
            {zoom: 8,
            center: res
            }
        );
        $.get(`/json/search`, {search: search}, (res2) => {
            console.log(res2);
            for (const trail of res2) {
                console.log(trail.name);
                $("#trail-list").append(`<li><a href="/trail/${trail.id}">${trail.name}</li>`);
                const marker = new google.maps.Marker(
                    {position: {
                        lng: Number(trail.longitude),
                        lat: Number(trail.latitude)
                    },
                    map: map,
                    title: trail.name
                    }
                );
                const infowindow = new google.maps.InfoWindow({
                    content: `Trail Name : <a href="/trail/${trail.id}">${trail.name}</li>`,
                });
                marker.addListener("click", function() {
                    map.setZoom(11);
                    map.panTo(marker.getPosition());
                    infowindow.open(marker.get("map"), marker);
                });
                infowindow.addListener("closeclick", function() {
                    infowindow.close();
                    map.setZoom(8);
                    map.setCenter(res);
                })

                }
            });
            });
    }