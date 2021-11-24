/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Updated 8th - 24th November, 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;

// For map
var extraStateInfo = {};
var isFirst = true;
var map = null;


function initialize() {
    loadParkSelector();
    loadStateSelector();
    loadCategorySelector();
    initializeMap();

    let element1 = document.getElementById('state_selector');

    let element2 = document.getElementById('park_selector');

    let element3 = document.getElementById('category_selector');      
    
    let element4 = document.getElementById('search_button');
    element4.onclick = onSearchButton;
    
    let url = window.location.href;
    let base_url = window.location.protocol
                        + '//' + window.location.hostname
                        + ':' + window.location.port
                        + '/species_search/';
    
    if (url != base_url){
        let park_code  =''
        park_code = url.substring(url.length-4)
        onSearchButton(park_code)  
    }
}


function initializeMap() {
    // A function that initializes our map, the first one is for when the page loads so there is no functionality.
    // The second map is loaded and contains the information required for our state summary.
    document.getElementById('map-container').innerHTML='';
    map = null;
    if (isFirst) {
        map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'usa', // which map?
                            projection: 'equirectangular',
                            data: extraStateInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#999999' },
                            geographyConfig: {
                                popupOnHover: false,
                                highlightOnHover: false,
                                //popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                borderColor: '#eeeeee', // state/country border color
                                highlightFillColor: '#057E00', // color when you hover on a state/country
                                highlightBorderColor: '#eeeeee', // border color when you hover on a state/country
                            }
                          });
        isFirst = false;
    }
    else
    {
        map = new Datamap({
            element: document.getElementById('map-container'), // where in the HTML to put the map
            scope: 'usa', // which map?
            projection: 'equirectangular',
            done: onMapDone, // once the map is loaded, call this function
            data: extraStateInfo, // here's some data that will be used by the popup template
            fills: {defaultFill: '#999999'},
            geographyConfig: {
                popupOnHover: false,
                highlightOnHover: true,
                //popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                borderColor: '#eeeeee', // state/country border color
                highlightFillColor: '#057E00', // color when you hover on a state/country
                highlightBorderColor: '#eeeeee', // border color when you hover on a state/country
            }
        });
    }
}


// This gets called once the map is drawn, so you can set various attributes like
// state/country click-handlers, etc.
function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick);
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
            summary += '<p>There is no data on national parks \n related to your search or in this state  </p>'
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
    // A function that loads states into our state selector.
    let url = getAPIBaseURL() + '/species_search/states';


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
    // A function that loads park names into our park selector.
    let url = getAPIBaseURL() + '/species_search/parks';


    fetch(url, {method: 'get'})


    .then((response) => response.json())


    .then(function(parks) {
        let selector = document.getElementById('park_selector');
        let url = window.location.href;
        let base_url = window.location.protocol
                            + '//' + window.location.hostname
                            + ':' + window.location.port
                            + '/species_search/';
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
        if (selector) {
                selector.innerHTML = selectorBody;
            }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}


function loadCategorySelector() {
    // A function that loads the different categories into our category selector.
    let url = getAPIBaseURL() + '/species_search/categories';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(categories) {

        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="' + 'selectCategory' + '">'
                                + '--' + '</option>\n';
        for (let k = 0; k < categories.length; k++) {
            let category = categories[k];
            selectorBody += '<option value="' + category['name'] + '">' +category['name']+ '</option>\n';
        }

        let selector = document.getElementById('category_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }

    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}


function onSearchButton(park_code_input) {

    // A function that is triggered by the use of our search button. That can be overridden in one case when the species
    // a park is searched from the parks page. This function sorts through our JSON response and puts it into the
    // table as well as the map.

    extraStateInfo = {}

    let park_code = ''
    if (park_code_input.length != 4){
        park_code = document.getElementById('park_selector').value
    }
    else {
        park_code = park_code_input
    }

    let state_id = document.getElementById('state_selector').value
    let category = document.getElementById('category_selector').value
    let species_name = document.getElementById('species_name').value
    let order = document.getElementById('order').value
    let family = document.getElementById('family').value
    let url = getAPIBaseURL() + '/species_search'+'?name='+ species_name +'&category='+ category +'&order='+ order
        +'&family='+ family +'&park_code='+ park_code + '&state=' + state_id ;

     fetch(url, {method: 'get'})
         // way to get search filters from the user and then give that to the api
         .then((response) => response.json())


     .then(function(species_results) {

         let tableBody = '';
         if (Object.keys(species_results).length == 0) {
             tableBody = '<tr> <th>No results came up for your search. Please try again</th> </tr>'
         }

         else {
             tableBody += '<tr>'
                 + '<th> Common Name </th>'
                 + '<th>Scientific Name</th>'
                 + '<th>Category</th>'
                 + '<th>Order</th>'
                 + '<th>Family</th>'
                 + '<th class="nativity_field">Native to</th>'
                 + '<th class="nativity_field">Non-Native</th>'
                 + '<th class="nativity_field">Nativity Unkown In</th>'

             let state_list = []

             for (var species in species_results) {
                 // Makes links for each park that shows up in the native to, non native and unknown columns
                 var value = species_results[species]
                 for (let k = 0; k < value['nativeTo'].length; k++){
                     let x = value['nativeTo'][k].trim()
                     let link = '/park_search?park_name='+ x
                     let parks = '<a href=' + link + '>'+x+'</a>'
                     value['nativeTo'][k] = parks
                 }

                 for (let k = 0; k < value['notNative'].length; k++){
                     let x = value['notNative'][k].trim()
                     let link = '/park_search?park_name='+ x
                     let parks = '<a href=' + link + '>'+x+'</a>'
                     value['notNative'][k] = parks
                 }

                 for (let k = 0; k < value['unknown'].length; k++){
                     let x = value['unknown'][k].trim()
                     let link = '/park_search?park_name='+ x
                     let parks = '<a href=' + link + '>'+x+'</a>'
                     value['unknown'][k] = parks
                 }

                 tableBody += '<tr>'
                     + '<td>' + value['common_name'] + '</td>'
                     + '<td>' + value['scientific_name'] + '</td>'
                     + '<td>' + value['category'] + '</td>'
                     + '<td>' + value['order'] + '</td>'
                      + '<td>' + value['family'] + '</td>'
                      + '<td class = "nativity_field">'+ value['nativeTo']+'</td>'
                      + '<td class = "nativity_field">'+value['notNative']+'</td>'
                      + '<td class = "nativity_field">'+ value['unknown']+'</td>'
                      + '</tr>'

                     // This is a loop that updates our extraStateInfo to make sure that all state that come up in the
                    // results are in the dictionary and that they have their relevant park information.
                    for(let k = 0; k < value['state'].length; k++)
                        if(value['state'][k] in extraStateInfo){
                            if(value['park_names'][k] in extraStateInfo[value['state'][k]].parkName){
                                extraStateInfo[value['state'][k]].parkName.push(value['park_names'][k])
                            }
                         }
                         else{
                             extraStateInfo[value['state'][k]] = {parkName: [value['park_names'][k]], fillColor: '#055D00'}
                         } 
                    }   
                 }

                initializeMap();
                let speciesTable = document.getElementById('species_table');
                if (speciesTable) {
                speciesTable.innerHTML = tableBody;
                }

            })
}
