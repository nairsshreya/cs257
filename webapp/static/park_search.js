/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;

function initialize() {
    loadStateSelector();

    let element1 = document.getElementById('park_selector');
    if (element1) {
        element1.onchange = onParkSelectionChanged;
    }
    let element2 = document.getElementById('state_selector');
    if (element2) {
        element2.onchange = onStateSelectionChanged;
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
    let url = getAPIBaseURL() + '/park_search';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(data) {
        let [parks, states] = data;
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        for (let k = 0; k < states.length; k++) {
            let state = states[k];
            selectorBody += '<option value="' + state['name'] + '">'
                                + state['id'] + '</option>\n';
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
    let url = getAPIBaseURL() + '/park_search' + state_id;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(data) {
        let [parks, states] = data;
        let tableBody = '';
        for (let k = 0; k < states.length; k++) {
            let state = states[k];
            tableBody += '<tr>'
                            + '<td>' + state['id'] + '</td>'
                            + '<td>' + state['name'] + '</td>'
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
    let url = getAPIBaseURL() + '/park_search';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(data) {
          let [parks, states] = data;
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        for (let k = 0; k < parks.length; k++) {
            let park = parks[k];
            selectorBody += '<option value="' + park['name'] + '"></option>\n';
        }

        let selector = document.getElementById('park_selector');
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
    let url = getAPIBaseURL() + '/park_search' + state_id;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(data) {
        let [parks, states] = data;
        let tableBody = '';
        tableBody += '<tr>'
                +'<th>Park Code </th>'
                +'<th>Park Name</th>'
                +'<th>State</th>'
                +'<th>Acres</th>'
               +' <th>Longitude</th>'
                +'<th>Latitude</th>'
            +'</tr>'
        for (let k = 0; k < parks.length; k++) {
            let park = parks[k];
            tableBody += '<tr>'
                +'<td>'+ park['park_code']+'</td>'
                +'<td>'+ park['name']+'</td>'
                +'<td>State</td>'
                +'<td>Acres</td>'
               +' <td>Longitude</td>'
                +'<td>Latitude</td>'
            +'</tr>'
        }
     let parksTable = document.getElementById('parks_table');
        if (parksTable) {
            parksTable.innerHTML = tableBody;
        }
        // // Put the table body we just built inside the table that's already on the page.
        // let stateTable = document.getElementById('books_table');
        // if (booksTable) {
        //     booksTable.innerHTML = tableBody;
        // }
    })
}