/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Updated between 8th and 24th November, 2021
 * Webapp assignment : Park page search
 */


window.onload = initialize;
// For map
var extraStateInfo = {};
var map = null;


function initialize() {
    loadParkSelector();
    loadStateSelector();
    initializeMap();
    let element1 = document.getElementById('park_name_selector');
    let element2 = document.getElementById('state_selector');
    let element4 = document.getElementById('park_search');
    element4.onclick = searchPark;
    let element5 = document.getElementById('state_search');
    element5.onclick = searchState;
    let url = window.location.href;
    let baseUrl = window.location.protocol
                        + '//' + window.location.hostname
                        + ':' + window.location.port
                        + '/park_search/';

    if (url != baseUrl){
        let park_code  = ''
        park_code = url.substring(url.length-4)
        onSearchButton('',park_code)
    }
    else{
        onSearchButton('','')
    }
}


function initializeMap() {
    // A function that loads the map on to our page.
    document.getElementById('map-container').innerHTML='';
    map = null;
    map = new Datamap({
        element: document.getElementById('map-container'), // where in the HTML to put the map
        scope: 'usa', // which map?
        projection: 'equirectangular', // what map projection? 'mercator' is also an option
        done: onMapDone, // once the map is loaded, call this function
        data: extraStateInfo, // here's some data that will be used by the popup template
        fills: {defaultFill: '#999999'},
        geographyConfig: {
            popupOnHover: false, // You can disable the hover popup
            highlightOnHover: true, // You can disable the color change on hover
            //popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
            borderColor: '#eeeeee', // state/country border color
            highlightFillColor: '#057E00', // color when you hover on a state/country
            highlightBorderColor: '#eeeeee', // border color when you hover on a state/country
        }
        });
}


// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
        dataMap.svg.selectAll('.datamaps-subunit').on('click',onStateClick);
}


function onStateClick(geography) {
    // geography.properties.name will be the state/country name (e.g. 'Minnesota')
    // geography.id will be the state/country name (e.g. 'MN')
    var stateSummaryElement = document.getElementById('state-summary');
    if (stateSummaryElement) {
        var summary = '<p><strong>State:</strong> ' + geography.properties.name + '</p>\n'
                    + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
        if (geography.id in extraStateInfo) {
            var info = extraStateInfo[geography.id];
            summary += '<p><strong>National Parks:<br> </strong> ' + info.parkName + '</p>\n'
                + '<p><strong>More information in table below</strong></p>';
        }
        else{
            summary += '<p>There is no data on national parks \n related to your search or in this state </p>'
        }

        stateSummaryElement.innerHTML = summary;
    }
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
    // A function to load the states into our state selector
    let url = getAPIBaseURL() + '/park_search/states';


    fetch(url, {method: 'get'})


    .then((response) => response.json())


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


function loadParkSelector() {
    // A function that loads the park names into the park selector.
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
        let selector = document.getElementById('park_name_selector');
        let url = window.location.href;
        let baseUrl = window.location.protocol
                            + '//' + window.location.hostname
                            + ':' + window.location.port
                            + '/parks_search/';
        let selectorBody = ''
        let park_code = url.substring(url.length-4)
        selectorBody += '<option value="' + 'selectParkName' + '">'
                                + '--' + '</option>\n';
        let nameToAdd = ''
        for (let k = 0; k < parks.length; k++) {
            let park = parks[k];
            selectorBody += '<option value="'+ park['park_code']+ '">' + park['park_name']+ '</option>\n';
            if (url != baseUrl && park['park_code'] == park_code ){
                 nameToAdd = park['park_name']
            }
        if (url != baseUrl && park['park_code'] == park_code ){
         selectorBody = '<option value="' + park_code + '">'
                         + nameToAdd + '</option>\n' + selectorBody;
     }
            }

        if (selector) {
            selector.innerHTML = selectorBody;
        }

    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}


function searchState(){
    // A function that is linked to the state search button and specifies that the search function should use a default
    // for the park_name value
    let stateId = document.getElementById('state_selector').value;
    onSearchButton(stateId, '');
    loadParkSelector();
}


function searchPark(){
     // A function that is linked to the state search button and specifies that the search function should use a default
    // for the state value
    let parkCode = document.getElementById('park_name_selector').value;
    onSearchButton('', parkCode);
    loadStateSelector();
}    


function onSearchButton(inputStateId, inputParkCode) {
    // This function is called when the search button is clicked, or for some exceptions called without that trigger.
    // It takes the results from the JSON dump and displays them to our park page. Some filtering is done to help other
    // features like our map display etc.
    extraStateInfo = {}
    document.getElementById('state-summary').innerHTML='';
    let stateId = inputStateId;
    let parkCode = inputParkCode;
    let url = getAPIBaseURL() + '/park_search'+ '?park_name='+ parkCode + '&state=' + stateId;
     fetch(url, {method: 'get'})

         // way to get search filters from the user and then give that to the api
         .then((response) => response.json())
     .then(function(park_results) {
         let tableBody = '';
         let stateSplit;
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
                 let link = '/species_search?park_name=' + park['park_code']
                 tableBody += '<tr>'
                     + '<td>' + park['park_code'] + '</td>'
                     + '<td><a href=' + link + '>' + park['park_name'] + '</a></td>'
                     + '<td>' + park['state_code'] + '</td>'
                     + '<td>' + park['acreage'] + '</td>'
                     + ' <td>' + park['longitude'] + '</td>'
                     + '<td>' + park['latitude'] + '</td>'
                     + '</tr>'

                 // This is a filter that ensures states are individually loaded and updated with the search results.
                 let state_result = '';
                 let temp = park['state_code'];
                 if (park['state_code'].length <= 2 & stateId != '--'){
                     let state_result = park['state_code'];
                     if(state_result in extraStateInfo){
                         extraStateInfo[state_result].parkName.push(' ' + park['park_name'])
                     }
                     else{
                         extraStateInfo[state_result] = {parkName: [park['park_name']], fillColor: '#055D00'}
                     } 
                 }
                 if (park['state_code'].length > 2) {
                     let stateSplit = temp.trim().split(",");
                     for (let i = 0; i < stateSplit.length; i++){
                        let state_result = stateSplit[i].trim();
                        if(state_result in extraStateInfo){
                             extraStateInfo[state_result].parkName.push(park['park_name'])
                         }
                         else{
                             extraStateInfo[state_result] = {parkName: [park['park_name']], fillColor: '#055D00'}
                         } 
                    }   
                 }
             }
         }
        let parksTable = document.getElementById('parks_table');
        if (parksTable) {
        parksTable.innerHTML = tableBody;
        }
        initializeMap()
    })
}
