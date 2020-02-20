"use strict";

const accountLink = $("#account")
const registerLink = $("#register")
const loginLink = $("#login")
const logoutLink = $("#logout")

$.get("/user/loggedin", (res) => {
    if (res === "true") {
        accountLink.removeClass("hidden");
        registerLink.addClass("hidden");
        loginLink.addClass("hidden");
        logoutLink.removeClass("hidden");
    }
});