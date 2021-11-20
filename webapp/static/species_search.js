/*
 * park_search.js
 * Shreya Nair and Elliot Hanson, 8th November 2021
 * Webapp assignment : Park page search
 */

window.onload = initialize;

function initialize() {
    let url = window.location.href;
    if (url != getAPIBaseURL()+'/species_search'){
        let park_code = url.substring(url.length-4)
        onSearchButton(park_code)
    }
    loadStateSelector();
    loadParkSelector();
    loadCategorySelector();

    let element1 = document.getElementById('state_selector');
    if (element1) {
        element1.onchange = onStateSelectionChanged;
    }
    let element2 = document.getElementById('park_selector');
    if (element2) {
        element2.onchange = onParkSelectionChanged;
    }
    let element3 = document.getElementById('category_selector');
    if (element3) {
        element3.onchange = onCategorySelectionChanged;
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
    let url = getAPIBaseURL() + '/species_search/states';

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
    let url = getAPIBaseURL() + '/species_search/parks';

    // Send the request to the parks API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(parks) {

        // Add the <option> elements to the <select> element
        let selectorBody = '<option value="' + 'selectPark' + '">'
                                + '--' + '</option>\n';
        for (let k = 0; k < parks.length; k++) {
            let park = parks[k];
            selectorBody += '<option value="' + park['park_code'] + '">' + park['park_name'] + '</option>\n';
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
    let url = getAPIBaseURL() + '/species_search';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

        // // Put the table body we just built inside the table that's already on the page.
        // let stateTable = document.getElementById('books_table');
        // if (booksTable) {
        //     booksTable.innerHTML = tableBody;
        // }
}
function loadCategorySelector() {
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
function onCategorySelectionChanged() {
    let category = this.value;
    let url = getAPIBaseURL() + '/species_search?category='+category ;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

        // // Put the table body we just built inside the table that's already on the page.
        // let stateTable = document.getElementById('books_table');
        // if (booksTable) {
        //     booksTable.innerHTML = tableBody;
        // }
}

function onSearchButton(park_code_input) {
    let park_code = ''
    if (park_code_input.length == 0){
        park_code = document.getElementById('park_selector').value
    }
    else {
        park_code = park_code_input
    }
    let state_id = document.getElementById('state_selector').value
    // let park_name = document.getElementById('park_selector').value
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
         if (species_results.length == 0) {
             tableBody = '<tr> No results came up for your search. Please try again </tr>'
         } else {
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
                 var value = species_results[species]
                 tableBody += '<tr>'
                     + '<td>' + value['common_name'] + '</td>'
                     + '<td>' + value['scientific_name'] + '</td>'
                     + '<td>' + value['category'] + '</td>'
                     + '<td>' + value['order'] + '</td>'
                      + '<td>' + value['family'] + '</td>'
                      + '<td>'+ value['nativeTo']+'</td>'
                      + '<td>'+value['notNative']+'</td>'
                      + '<td>'+ value['unknown']+'</td>'
                      + '</tr>'
             }

             // for (let k = 0; k < species_results.length; k++) {
             //
             //     let species = species_results[k];
             //      tableBody += '<tr>'
             //         + '<td>' + species['common_name'] + '</td>'
             //         + '<td>' + species['scientific_name'] + '</a></td>'
             //         + '<td>' + species['category'] + '</td>'
             //         + '<td>' + species['order'] + '</td>'
             //         + '<td>' + species['family'] + '</td>'
             //         + '<td></td>'
             //         + '<td></td>'
             //         + '<td></td>'
             //         + '</tr>'
             // tableBody += '<tr>'
             //     + '<td>' + species['common_name'] + '</td>'
             //     + '<td>' + species['scientific_name'] + '</a></td>'
             //     + '<td>' + species['category'] + '</td>'
             //     + '<td>' + species['order'] + '</td>'
             //     + '<td>' + species['family'] + '</td>'
             //     + '<td>' + species['nativeTo'] + '</td>'
             //     + '<td>' + species['park_name'] + '</td>'
             //     + '<td>' + species['state'] + '</td>'
             //     + '</tr>'
             // if (!state_list.includes(species['state'])){
             //     state_list.push(species['state'])
             // }

         }
            // extraStateInfo = {IL : {population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa'}}
            // map.updateChoropleth({IL: 'green'}, {reset: true})
        let speciesTable = document.getElementById('species_table');
        if (speciesTable) {
        speciesTable.innerHTML = tableBody;
        }
    })
}
