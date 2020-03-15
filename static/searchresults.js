"use strict";

const params = (new URL(document.location)).searchParams;
const search = params.get("search");

$("#search-results-search").attr("value", search);

$("#trail-list-header").html(`Hiking trails near ${search}`);

const nextButton = $("#next-button");
const prevButton = $("#prev-button");
const hideTripsButton = $("#hide-trip-markers");
const showTripsButton = $("#show-trip-markers");

// Variables for start & stop of search results
let start = 0;
let stop = 10;

// Array to hold Google Map Markers for trails being displayed on map
let searchMarkerArray = [];
let tripMarkerArray = [];

const houseIcon = "/static/images/house.png";
const hikerIcon = "/static/images/hiker.png";

const colorToDifficultyConversion = {
    "green": "Easy",
    "greenBlue": "Moderately Easy",
    "blue": "Intermediate",
    "blueBlack": "Somewhat Difficult",
    "black": "Difficult",
    "dblack": "Extremely Difficult",
    "missing": "Information Missing"
};

function initMap() {
    $.get(`/json/search-coords`, {search: search}, (res) => {
        console.log(res);
        if (res === "Invalid search terms") {
            $("#search-map-container").html("Invalid search terms, please try again");
            nextButton.addClass("hidden");
        } else {
            // Create a Map instance
            const map = new google.maps.Map(
                document.querySelector("#search-map-container"),
                {zoom: 10,
                center: res
                }
            );
            // Function to add markers to the map with an info window & event listeners
            const addMarker = (markerInfo, infoWindowContent, markerArray) => {
                const marker = new google.maps.Marker(markerInfo);
                markerArray.push(marker);
                const infowindow = new google.maps.InfoWindow({
                    content: infoWindowContent,
                });
                marker.addListener("click", () => {
                    map.setZoom(13);
                    map.panTo(marker.getPosition());
                    infowindow.open(marker.get("map"), marker);
                });
                infowindow.addListener("closeclick", () => {
                    infowindow.close();
                    map.setZoom(10);
                    map.setCenter(res);
                });
                return marker;
            };
            // Function to set each marker in given markerArray on the map
            const setMarkersOnMap = (map, markerArray) => {
                for (let i = 0; i < markerArray.length; i++) {
                    markerArray[i].setMap(map);
                }
            };
            // Function to remove markers from map & empty given markerArray
            const deleteMarkers = (markerArray) => {
                setMarkersOnMap(null, markerArray);
                searchMarkerArray = [];
            };
            // Function to hide markers from given markerArray
            const hideMarkers = (markerArray) => {
                setMarkersOnMap(null, markerArray);
            };
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
                        const difficulty = trail.difficulty;
                        $("#trail-list-container").append(
                            `<a href="/trail/${trail.id}" id=${trail.id} class="card mb-3">
                                <div class="row no-gutters align-items-center">
                                    <div class="col-md-4">
                                        <img src="${trail.imgSqSmall}" class="card-img" alt="${trail.name}">
                                    </div>
                                    <div class="col-md-8">
                                        <div class="card-body">
                                        <h5 class="card-title">${trail.name}</h5>
                                        <p class="card-text"><b>Length:</b> ${trail.length} miles</p>
                                        <p class="card-text"><b>Difficulty:</b> ${colorToDifficultyConversion[difficulty]}</p>
                                        </div>
                                    </div>
                                </div>
                            </a>`
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
                        const marker = addMarker(markerInfo, infoWindowContent, searchMarkerArray);
                        // Event listeners on each of the trail text divs to animate map marker
                        $(`#${trail.id}`).on("mouseenter", () => {
                            marker.setAnimation(google.maps.Animation.BOUNCE);
                            $(`#${trail.id}`).css("background-color", "#f8f9fa");
                        });
                        $(`#${trail.id}`).on("mouseleave", () => {
                            marker.setAnimation(undefined);
                            $(`#${trail.id}`).css("background-color", "#ffffff");
                        });
                    }
                    setMarkersOnMap(map, searchMarkerArray);
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
                            addMarker(markerInfo, infoWindowContent, tripMarkerArray);
                        };
                    };
                });
            };
            const getTripLocations = () => {
                $.get("/json/getallusertrips", (res) => {
                    if (res !== "none") {
                        hideTripsButton.removeClass("hidden");
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
                                addMarker(markerInfo, infoWindowContent, tripMarkerArray);
                            };
                            getTripTrails(trip_id.trip_id);
                        };
                        setMarkersOnMap(map, tripMarkerArray);
                    }
                });
            };
            // Load search results & trip locations
            getSearchResults(search);
            getTripLocations();
            // Increment/decrement when next or prev buttons are clicked
            nextButton.on("click", () => {
                start += 10;
                stop += 10;
                deleteMarkers(searchMarkerArray);
                $("#trail-list-container").empty()
                getSearchResults(search);
                $("#prev-button").removeClass("hidden");
            });
            prevButton.on("click", () => {
                start -= 10;
                stop -= 10;
                deleteMarkers(searchMarkerArray);
                $("#trail-list-container").empty()
                getSearchResults(search);
                $("#next-button").removeClass("hidden");
            });
            // Toggle trip markers on map
            hideTripsButton.on("click", () => {
                hideMarkers(tripMarkerArray);
                hideTripsButton.toggle();
                showTripsButton.toggle();
            });
            showTripsButton.on("click", () => {
                setMarkersOnMap(map, tripMarkerArray);
                hideTripsButton.toggle();
                showTripsButton.toggle();
            });
        };
    });
};

