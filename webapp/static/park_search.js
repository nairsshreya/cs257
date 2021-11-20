/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;

// For map
var extraStateInfo = {
   
};

var map = null;

function initialize() {

    loadParkSelector();
    loadStateSelector();
    initializeMap();
    let element1 = document.getElementById('park_name_selector');
    if (element1) {
        element1.onchange = onParkSelectionChanged;
    }
    let element2 = document.getElementById('state_selector');
    if (element2) {
        element2.onchange = onStateSelectionChanged;
    }
    let element4 = document.getElementById('search_button');
    element4.onclick = onSearchButton;
}

function initializeMap() {
     map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'usa', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            done: onMapDone, // once the map is loaded, call this function
                            data: extraStateInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#999999' },
                            geographyConfig: {
                                popupOnHover: false, // You can disable the hover popup
                                highlightOnHover: false, // You can disable the color change on hover
                                //popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                borderColor: '#eeeeee', // state/country border color
                                highlightFillColor: '#bbbbbb', // color when you hover on a state/country
                                highlightBorderColor: '#000000', // border color when you hover on a state/country
                            }
                          });
}
// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick);
}

function onStateClick(geography){
    return
    
}
// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function loadStateSelector() {
    let url = getAPIBaseURL() + '/park_search/states';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(states) {
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="' + 'selectState' + '">'
                                + '--' + '</option>\n';
        for (let k = 0; k < states.length; k++) {
            let state = states[k];
            selectorBody += '<option value="' + state['id'] + '">'
                                + state['name'] + '</option>\n';
        }

        let selector = document.getElementById('state_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
function onStateSelectionChanged() {
    let state_id = this.value;
    let url = getAPIBaseURL() + '/park_search?states=' + state_id;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(data) {
        let [parks, states] = data;
        let tableBody = '';
        for (let k = 0; k < states.length; k++) {
            let state = states[k];
            tableBody += '<tr>'
                            + '<td>' + state['name'] + '</td>'
                            + '<td>' + state['id'] + '</td>'
                            + '</tr>\n';
        }

    })
}

function loadParkSelector() {
    let url = getAPIBaseURL() + '/park_search/parks';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(parks) {
          //let [parks, states] = data;
        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="' + 'selectParkName' + '">'
                                + '--' + '</option>\n';
        for (let k = 0; k < parks.length; k++) {
            let park = parks[k];
            // disp_string = park['park_code']+' -- '+park['name']
            selectorBody += '<option value="'+ park['park_name']+ '">' + park['park_name']+ '</option>\n';
        }

        let selector = document.getElementById('park_name_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }

    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
function onParkSelectionChanged() {
    //let state_id = this.value;
    let park_name = this.value;
    let url = getAPIBaseURL() + '/park_search?park_name=' + park_name;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    // WE WERE TRYING SOMETHING
        // .then(function (park_results){
        //     let park = park_results[0];
        //     let selectorBody = '<option' + park['state_code']+'>'+ park['park_name']+ '</option>\n';
        //     let selector = document.getElementById('state_selector');
        //     if (selector) {
        //         selector.innerHTML = selectorBody;
    //     //     }
    // })


}

function onSearchButton() {
    let state_id = document.getElementById('state_selector').value
    let park_name = document.getElementById('park_name_selector').value

    let url = getAPIBaseURL() + '/park_search'+ '?park_name='+ park_name + '&state=' + state_id;
     fetch(url, {method: 'get'})

         // way to get search filters from the user and then give that to the api
         .then((response) => response.json())
     .then(function(park_results) {
         let tableBody = '';
         if (park_results.length == 0) {
             tableBody = '<tr> No results came up for your search. Please try again </tr>'
         } else {
         tableBody += '<tr>'
             + '<th>Park Code </th>'
             + '<th>Park Name</th>'
             + '<th>State</th>'
             + '<th>Acres</th>'
             + ' <th>Longitude</th>'
             + '<th>Latitude</th>'
             + '</tr>'

         for (let k = 0; k < park_results.length; k++) {
             let park = park_results[k];
             let link = '/species_search?park_name='+ park['park_code']
             tableBody += '<tr>'
                 + '<td>' + park['park_code'] + '</td>'
                 + '<td><a href='+link+'>' + park['park_name'] + '</a></td>'
                 + '<td>' + park['state_code'] + '</td>'
                 + '<td>' + park['acreage'] + '</td>'
                 + ' <td>' + park['longitude'] + '</td>'
                 + '<td>' + park['latitude'] + '</td>'
                 + '</tr>'
         }
            extraStateInfo = {IL : {population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa'}}
            map.updateChoropleth({'IL': 'green'}, {reset: true})
         }
        let parksTable = document.getElementById('parks_table');
        if (parksTable) {
        parksTable.innerHTML = tableBody;
        }
    })
}





// figure out a way to get selected values from the search - use app and api ?
