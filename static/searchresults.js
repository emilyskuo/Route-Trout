"use strict";

const params = (new URL(document.location)).searchParams;
const search = params.get("search");

$("#search-results-search").attr("value", search);

const nextButton = $("#next-button");
const prevButton = $("#prev-button");

let start = 0;
let stop = 10;
let markerArray = [];

function initMap() {
    $.get(`/json/search-coords`, {search: search}, (res) => {
        if (res === "Invalid search terms") {
            $("#map-container").html("Invalid search terms, <a href='/'>please try again</a>")
        } else {
            const map = new google.maps.Map(
                document.querySelector("#search-map-container"),
                {zoom: 8,
                center: res
                }
            );
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
            const setMarkersOnMap = (map) => {
                for (let i = 0; i < markerArray.length; i++) {
                    markerArray[i].setMap(map);
                }
            };
            const deleteMarkers = () => {
                setMarkersOnMap(null);
                markerArray = []
            }
            const getSearchResults = (searchTerms) => {
                $.get(`/json/search`, {search: searchTerms}, (res2) => {
                    if (start <= 0) {
                        $("#prev-button").addClass("hidden");
                    }
                    if (stop >= res2.length){
                        $("#next-button").addClass("hidden");
                    }
                    let list_slice = res2.slice(start, stop);
                    for (const trail of list_slice) {
                        $("#trail-list-container").append(
                            `<div id=${trail.id}>
                            <img src="${trail.imgSqSmall}">
                            <a href="/trail/${trail.id}">${trail.name}</a>
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
                        $(`#${trail.id}`).on("mouseenter", () => {
                            console.log(marker.getAnimation());
                            console.log("this is a mouseenter");
                            marker.setOptions({
                                zIndex: 50,
                            });
                            marker.setAnimation(google.maps.Animation.BOUNCE);
                            console.log(marker.getAnimation());
                        });
                        
                        $(`#${trail.id}`).on("mouseleave", () => {
                            console.log(marker.getAnimation());
                            console.log("this is a mouseleave");
                            marker.setOptions({
                                zIndex: 5,
                            });
                            marker.setAnimation(null);
                            console.log(marker.getAnimation());
                        });
                    }
                    setMarkersOnMap(map);
                })
            };
            getSearchResults(search);
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

