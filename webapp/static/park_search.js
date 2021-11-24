/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;
var isFirst = true;
// For map
var extraStateInfo = {};

var map = null;

function initialize() {
    loadParkSelector();
    loadStateSelector();
    initializeMap();
    let element1 = document.getElementById('park_name_selector');
//    if (element1) {
//        element1.onchange = onParkSelectionChanged;
//    }
    let element2 = document.getElementById('state_selector');
//    if (element2) {
//        element2.onchange = onStateSelectionChanged;
//    }
    let element4 = document.getElementById('park_search');
    element4.onclick = searchPark;
    let element5 = document.getElementById('state_search');
    element5.onclick = searchState;
    let url = window.location.href;
    let base_url = window.location.protocol
                        + '//' + window.location.hostname
                        + ':' + window.location.port
                        + '/park_search/';

    if (url != base_url){
        let park_code  = ''
        park_code = url.substring(url.length-4)
        onSearchButton('',park_code)
    }

}

function initializeMap() {
    document.getElementById('map-container').innerHTML='';
    map = null;
    if (isFirst) {
        map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'usa', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            //done: onMapDone, // once the map is loaded, call this function
                            data: extraStateInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#999999' },
                            geographyConfig: {
                                popupOnHover: false, // You can disable the hover popup
                                highlightOnHover: false, // You can disable the color change on hover
                                //popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                borderColor: '#eeeeee', // state/country border color
                                highlightFillColor: '#057E00', // color when you hover on a state/country
                                highlightBorderColor: '#000000', // border color when you hover on a state/country
                            }
                          });
        isFirst = false;
    }
    else
    {
        map = new Datamap({
            element: document.getElementById('map-container'), // where in the HTML to put the map
            scope: 'usa', // which map?
            projection: 'equirectangular', // what map projection? 'mercator' is also an option
            done: onMapDone, // once the map is loaded, call this function
            data: extraStateInfo, // here's some data that will be used by the popup template
            fills: {defaultFill: '#999999'},
            geographyConfig: {
                popupOnHover: true, // You can disable the hover popup
                highlightOnHover: true, // You can disable the color change on hover
                popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                borderColor: '#eeeeee', // state/country border color
                highlightFillColor: '#057E00', // color when you hover on a state/country
                highlightBorderColor: '#000000', // border color when you hover on a state/country
            }
        });
    }
}
// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
        dataMap.svg.selectAll('.datamaps-subunit').on('click',onStateClick);
}

function hoverPopupTemplate(geography, data) {
    var population = 0;
    if (data && 'population' in data) {
        population = data.population;
    }

    var jeffHasLivedThere = 'No';
    if (data && 'jeffhaslivedthere' in data && data.jeffhaslivedthere) {
        jeffHasLivedThere = 'Yes';
    }

    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
                    + '<strong>Population:</strong> ' + population + '<br>\n'
                    + '<strong>Has Jeff lived there?</strong> ' + jeffHasLivedThere + '<br>\n'
                    + '</div>';


    return template;
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
            summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
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
//    let stateId = this.value;
//    let url = getAPIBaseURL() + '/park_search?states=' + stateId;
//
//    fetch(url, {method: 'get'})
//
//    .then((response) => response.json())
//
//    .then(function(data) {
//        let [parks, states] = data;
//        let tableBody = '';
//        for (let k = 0; k < states.length; k++) {
//            let state = states[k];
//            tableBody += '<tr>'
//                            + '<td>' + state['name'] + '</td>'
//                            + '<td>' + state['id'] + '</td>'
//                            + '</tr>\n';
//        }
//
//    })
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
        let selector = document.getElementById('park_name_selector');
        let url = window.location.href;
        let base_url = window.location.protocol
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
            if (url != base_url && park['park_code'] == park_code ){
                 nameToAdd = park['park_name']
            }
        if (url != base_url && park['park_code'] == park_code ){
         selectorBody = '<option value="' + park_code + '">'
                         + nameToAdd + '</option>\n' + selectorBody;
     }
            }

        // if (url != base_url){
        //     let park_code = url.substring(url.length-4)
        //     onSearchButton(park_code)
        //     selectorBody += '<option value="' + park_code + '">'
        //                     + park_code + '</option>\n';
        // }
        //
        // selectorBody += '<option value="' + 'selectParkName' + '">'
        //                         + '--' + '</option>\n';
        // for (let k = 0; k < parks.length; k++) {
        //     let park = parks[k];
        //     // disp_string = park['park_code']+' -- '+park['name']
        //     selectorBody += '<option value="'+ park['park_code']+ '">' + park['park_name']+ '</option>\n';
        // }


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
    //let stateId = this.value;
//    let park_name = this.value;
//    let url = getAPIBaseURL() + '/park_search?park_name=' + park_name;
//
//    fetch(url, {method: 'get'})
//
//    .then((response) => response.json())

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
function searchState(){
    let stateId = document.getElementById('state_selector').value;
    onSearchButton(stateId, '');
    loadParkSelector();
}

function searchPark(){
    let parkCode = document.getElementById('park_name_selector').value;
    onSearchButton('', parkCode);
    loadStateSelector();
}    

function onSearchButton(inputStateId, inputParkCode) {
    extraStateInfo = {}
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

                 let state_result = '';
                 let temp = park['state_code'];
                 if (park['state_code'].length > 2) {
                     let stateSplit = temp.trim().split(",");
                     if (stateId.length <= 2 & stateId != '--'){
                         state_result = stateId;
                         extraStateInfo[state_result] = {population: 39500000, jeffhaslivedthere: true, fillColor: '#055D00'}
                     }
                    else {
                        for (let i = 0; i < stateSplit.length; i++){
                            //let state_str = stateSplit[i].replace('/\s/g', "")
                            let state = stateSplit[i].trim();
                            extraStateInfo[state] = {population: 39500000, jeffhaslivedthere: true, fillColor: '#055D00'}
                        }

                     }


                 } else {
                     state_result = park['state_code'];
                     extraStateInfo[state_result] = {population: 39500000, jeffhaslivedthere: true, fillColor: '#055D00'}
                 }
                 // extraStateInfo[state_result] = {population: 39500000, jeffhaslivedthere: true, fillColor: 'blue'}

             }
             // extraStateInfo.push({IL : {population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa'}})
             // map.updateChoropleth({'IL': 'green'}, {reset: true})

         }
        let parksTable = document.getElementById('parks_table');
        if (parksTable) {
        parksTable.innerHTML = tableBody;
        }
        initializeMap()
    })
}





// figure out a way to get selected values from the search - use app and api ?
