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
const hikerIcon = "/static/images/hiker.png"

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
            const addMarker = (markerInfo, infoWindowContent) => {
                const marker = new google.maps.Marker(markerInfo);
                markerArray.push(marker);
                const infowindow = new google.maps.InfoWindow({
                    content: infoWindowContent,
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
                        const infoWindowContent = `Trail Name : <a href="/trail/${trail.id}">${trail.name}</a>`;
                        const marker = addMarker(markerInfo, infoWindowContent);
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
            const getTripTrails = (trip_id) => {
                $.get("/json/gettriptrailinfo", {trip_id: trip_id}, (res) => {
                    if (res !== "No tt here") {
                        for (const trail of Object.values(res)) {
                            const markerInfo = {
                                position: {
                                    lat: Number(trail.trail_lat),
                                    lng: Number(trail.trail_lng)
                                },
                                map: map,
                                title: trail.trail_name,
                                icon: hikerIcon,
                                zIndex: 50,
                            };
                            const infoWindowContent = `Trail: <a href="/trail/${trail.trail_id}">${trail.trail_name}</a> <br>
                                Trip Name : <a href="/trip/${trail.trip_id}">${trail.trip_name}</a>`;
                            addMarker(markerInfo, infoWindowContent);
                        }
                    }
                    else {
                        console.log("nope");
                    }
                });
            };
            const getTripLocations = () => {
                $.get("/json/getallusertrips", (res) => {
                    for (const trip_id of Object.values(res)) {
                        if (trip_id.trip_lat !== null) {
                            const markerInfo = {
                                position: {
                                    lat: Number(trip_id.trip_lat),
                                    lng: Number(trip_id.trip_lng)
                                },
                                map: map,
                                title: trip_id.trip_name,
                                icon: houseIcon,
                                zIndex: 50,
                            };
                            const infoWindowContent = `Trip Name : <a href="/trip/${trip_id.trip_id}">${trip_id.trip_name}</a>`;
                            addMarker(markerInfo, infoWindowContent);
                        } else {
                            console.log("this didn't work");
                        };
                        getTripTrails(trip_id.trip_id);
                    };
                    setMarkersOnMap(map);
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
                getTripLocations();
                $("#prev-button").removeClass("hidden");
            });

            prevButton.on("click", () => {
                start -= 10;
                stop -= 10;
                deleteMarkers();
                $("#trail-list-container").empty()
                getSearchResults(search);
                getTripLocations();
                $("#next-button").removeClass("hidden");
            });
        }
    });
}

