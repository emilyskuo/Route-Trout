"use strict";

const params = (new URL(document.location)).searchParams;
const search = params.get("search");
const nextButton = $("#next-button");
let start = 0;
let stop = 10;



function initMap() {
    $.get(`/json/search-coords`, {search: search}, (res) => {
        if (res === "Invalid search terms") {
            $("#map-container").html("Invalid search terms, <a href='/'>please try again</a>")
        } else {
            const map = new google.maps.Map(
                document.querySelector("#map-container"),
                {zoom: 8,
                center: res
                }
            );
            const getSearchResults = (searchTerms) => {
                $.get(`/json/search`, {search: searchTerms}, (res2) => {
                let list_slice = res2.slice(start, stop);
                for (const trail of list_slice) {
                    $("#trail-list").append(`<li><a href="/trail/${trail.id}">${trail.name}</li>`);
                    const marker = new google.maps.Marker(
                        {position: {
                            lng: Number(trail.longitude),
                            lat: Number(trail.latitude)
                        },
                        map: map,
                        title: trail.name
                        }
                    );}
                })};
            getSearchResults(search);
            nextButton.on("click", () => {
                start += 10;
                stop += 10;
                $("#trail-list").empty()
                getSearchResults(search);
            });

                    // const infowindow = new google.maps.InfoWindow({
                    //     content: `Trail Name : <a href="/trail/${trail.id}">${trail.name}</li>`,
                    // });
                    // marker.addListener("click", function() {
                    //     map.setZoom(11);
                    //     map.panTo(marker.getPosition());
                    //     infowindow.open(marker.get("map"), marker);
                    // });
                    // infowindow.addListener("closeclick", function() {
                    //     infowindow.close();
                    //     map.setZoom(8);
                    //     map.setCenter(res);
            //         })
            //     }
            // });
        }
    });}
