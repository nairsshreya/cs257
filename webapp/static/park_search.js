/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;

// For map
var extraStateInfo = {
    MN: {population: 5640000, jeffhaslivedthere: true, fillColor: '#2222aa'},
    CA: {population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa'},
    NM: {population: 2100000, jeffhaslivedthere: false, fillColor: '#2222aa'},
    OH: {population: 0, jeffhaslivedthere: false, fillColor: '#aa2222'}
};

function initialize() {

    loadParkSelector();
    loadStateSelector();
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
        //let [parks, states] = data;
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
    let url = getAPIBaseURL() + '/park_search/states' + state_id;

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

        // // Put the table body we just built inside the table that's already on the page.
        // let stateTable = document.getElementById('books_table');
        // if (booksTable) {
        //     booksTable.innerHTML = tableBody;
        // }
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
            selectorBody += '<option value="'+ park['name']+ '">' + park['name']+ '</option>\n';
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
    let state_id = this.value;
    let url = getAPIBaseURL() + '/park_search/' + state_id;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

        // // Put the table body we just built inside the table that's already on the page.
        // let stateTable = document.getElementById('books_table');
        // if (booksTable) {
        //     booksTable.innerHTML = tableBody;
        // }
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
        tableBody += '<tr>'
                +'<th>Park Code </th>'
                +'<th>Park Name</th>'
                +'<th>State</th>'
                +'<th>Acres</th>'
               +' <th>Longitude</th>'
                +'<th>Latitude</th>'
            +'</tr>'
        for (let k = 0; k < park_results.length; k++) {
            let park = park_results[k];
            tableBody += '<tr>'
                +'<td>'+ park['park_code']+'</td>'
                +'<td><a href="/species_search/">'+ park['name']+'</a></td>'
                +'<td>'+park['state_code']+'</td>'
                +'<td>'+park['acreage']+'</td>'
               +' <td>'+park['longitude']+'</td>'
                +'<td>'+park['latitude']+'</td>'
            +'</tr>'
        }
     let parksTable = document.getElementById('parks_table');
        if (parksTable) {
            parksTable.innerHTML = tableBody;
        }
    })
}





// figure out a way to get selected values from the search - use app and api ?
