function responsiveNav() {
    let x = document.getElementById("navbarMenuHeroA");
    if (x.className === "navbar-menu") {
        x.className += " responsive";
    } else {
        x.className = "navbar-menu";
    }
}

function tabView(page) {
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("tabcontent");

    for (i = 0; i <tabcontent.length; i++){
        tabcontent[i].style.display = "none";
    }
    document.getElementById(page).style.display = "block";
}

function httpGetAsync(url, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200)
            callback(JSON.parse(xmlHttp.response));
    }
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}