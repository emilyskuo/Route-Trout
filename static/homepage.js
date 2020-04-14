"use strict";

const most_recent_trail = $("#most_recent_trail").html();
const second_most_recent = $("#second_most_recent").html();
const third_most_recent = $("#third_most_recent").html();

const most_recent_trails = [];

if (most_recent_trail) {
    most_recent_trails.push(most_recent_trail);
};
if (second_most_recent) {
    most_recent_trails.push(second_most_recent);
};
if (third_most_recent) {
    most_recent_trails.push(third_most_recent);
};

const colorToDifficultyConversion = {
    "green": "Easy",
    "greenBlue": "Moderately Easy",
    "blue": "Intermediate",
    "blueBlack": "Somewhat Difficult",
    "black": "Difficult",
    "dblack": "Extremely Difficult",
    "missing": "Information Missing"
};

for (const trail_id of most_recent_trails) {
    $.get("/gettrailbyid", {trail_id:trail_id}, (res) => {
        if (res.success == 1) {
            $("#most_recent_div").append(
            `<a href="/trail/${trail_id}" class="card ml-2 mr-2">
            <div class="col">
                <div class="row no-gutters align-items-center">
                    <div class="col-md-4">
                        <img src="${res.trails[0].imgSqSmall}" class="card-img" alt="${res.trails[0].name}">
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                        <h5 class="card-title">${res.trails[0].name}</h5>
                        <p class="card-text"><b>Length:</b> ${res.trails[0].length} miles</p>
                        <p class="card-text"><b>Difficulty:</b> ${colorToDifficultyConversion[res.trails[0].difficulty]}</p>
                        </div>
                    </div>
                </div>
                </div>
            </a>`
            );

        }
    });
}
