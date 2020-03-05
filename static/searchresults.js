"use strict";

const params = (new URL(document.location)).searchParams;
const search = params.get("search");

$("#search-results-search").attr("value", search);

const nextButton = $("#next-button");
const prevButton = $("#prev-button");

// Variables for start & stop of search results
let start = 0;
let stop = 10;

// Array to hold Google Map Markers for trails being displayed on map
let markerArray = [];

const houseIcon = "/static/images/house.png"

function initMap() {
    $.get(`/json/search-coords`, {search: search}, (res) => {
        if (res === "Invalid search terms") {
            $("#search-map-container").html("Invalid search terms, please try again");
            nextButton.addClass("hidden");
        } else {
            // Create a Map instance
            const map = new google.maps.Map(
                document.querySelector("#search-map-container"),
                {zoom: 8,
                center: res
                }
            );
            // Function to add markers to the map with an info window & event listeners
            const addMarker = (markerInfo, trail) => {
                const marker = new google.maps.Marker(markerInfo);
                markerArray.push(marker);
                const infowindow = new google.maps.InfoWindow({
                    content: `Trail Name : <a href="/trail/${trail.id}">${trail.name}</a>`,
                });
                marker.addListener("click", () => {
                    map.setZoom(11);
                    map.panTo(marker.getPosition());
                    infowindow.open(marker.get("map"), marker);
                });
                infowindow.addListener("closeclick", () => {
                    infowindow.close();
                    map.setZoom(8);
                    map.setCenter(res);
                });
                return marker;
            };
            // Function to set each marker in markerArray on the map
            const setMarkersOnMap = (map) => {
                for (let i = 0; i < markerArray.length; i++) {
                    markerArray[i].setMap(map);
                }
            };
            // Function to remove all markers from map & empty markerArray
            const deleteMarkers = () => {
                setMarkersOnMap(null);
                markerArray = []
            }
            // Function to get search results
            const getSearchResults = (searchTerms) => {
                $.get(`/json/search`, {search: searchTerms}, (res2) => {
                    // Hide "previous button" if no previous trails available
                    if (start <= 0) {
                        $("#prev-button").addClass("hidden");
                    }
                    // Hide "next button" if no further trails are available
                    if (stop >= res2.length){
                        $("#next-button").addClass("hidden");
                    }
                    // Slice get request response based on start/stop
                    let list_slice = res2.slice(start, stop);
                    // Display each trail within the list slice & set markers on map
                    for (const trail of list_slice) {
                        $("#trail-list-container").append(
                            `<div id=${trail.id}>
                            <img src="${trail.imgSqSmall}">
                            <a href="/trail/${trail.id}">${trail.name}</a>
                            <b>Length:</b> ${trail.length}
                            </div>`
                            );
                        const markerInfo = {
                            position: {
                                lng: Number(trail.longitude),
                                lat: Number(trail.latitude)
                            },
                            map: map,
                            title: trail.name,
                        };
                        const marker = addMarker(markerInfo, trail);
                        // Event listeners on each of the trail text divs to animate map marker
                        $(`#${trail.id}`).on("mouseenter", () => {
                            marker.setAnimation(google.maps.Animation.BOUNCE);
                        });
                        $(`#${trail.id}`).on("mouseleave", () => {
                            marker.setAnimation(undefined);
                        });
                    }
                    setMarkersOnMap(map);
                })
            };
            const getTripLocations = () => {
                $.get("/trip/user/getallusertrips", (res) => {
                    console.log(res);
                    for (const trip_id of Object.values(res)) {
                        console.log(trip_id);
                        if (trip_id.trip_lat !== null) {
                            console.log(trip_id.trip_lat);
                            const marker = new google.maps.Marker({
                                position: {
                                    lat: Number(trip_id.trip_lat),
                                    lng: Number(trip_id.trip_lng)
                                },
                                map: map,
                                title: trip_id.trip_name,
                                icon: houseIcon
                            });
                            markerArray.push(marker);
                            const infowindow = new google.maps.InfoWindow({
                                content: `Trip Name : <a href="/trip/${trip_id.trip_id}">${trip_id.trip_name}</a>`,
                            });
                            marker.addListener("click", () => {
                                map.setZoom(11);
                                map.panTo(marker.getPosition());
                                infowindow.open(marker.get("map"), marker);
                            });
                            infowindow.addListener("closeclick", () => {
                                infowindow.close();
                                map.setZoom(8);
                                map.setCenter(res);
                            });
                        } else {
                            console.log("this didn't work");
                        };
                    };
                });
            };
            getSearchResults(search);
            getTripLocations();
            // Increment/decrement when next or prev buttons are clicked
            nextButton.on("click", () => {
                start += 10;
                stop += 10;
                deleteMarkers();
                $("#trail-list-container").empty()
                getSearchResults(search);
                $("#prev-button").removeClass("hidden");
            });

            prevButton.on("click", () => {
                start -= 10;
                stop -= 10;
                deleteMarkers();
                $("#trail-list-container").empty()
                getSearchResults(search);
                $("#next-button").removeClass("hidden");
            });
        }
    });
}

