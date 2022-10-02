const tables = document.querySelectorAll('[id^=material-table-]')

tables.forEach(table => {
    table.querySelectorAll('[class^=column-header]').forEach(columnheader => {
        console.log(columnheader)
        columnheader.addEventListener('click', () => {
            test()
        })
    })
})


function GET_parameters(){
//    Return parameter of GET request as dictionary
    let dict = {};
    const get_params = window.location.search.split('?')[1].split('&');
    for (const param of get_params) {
        let name, value;
        [name, value] = param.split('=', 2);
        dict[decodeURIComponent(name)] = decodeURIComponent(value);
    }
    return dict
}


function test() {
    console.log(this)
    console.log('*')
}

function get_open_accordion_tabs(){
    return [...document.querySelectorAll('div.accordion-collapse.show')].map(item => item.id).join(',')
}

function update_params(key='', value=)''{
    var parameters = GET_parameters()
    parameters['open'] = get_open_accordion_tabs()

    if (key) {
        parameters[key] = value
    }

    var query = Object.keys( parameters ).map( function(key){
        return encodeURIComponent(key) + "=" + encodeURIComponent(parameters[key])
    }).join("&")

    return query
}

function reload_page(){
    window.location.href = window.location.origin + window.location.pathname + '?' + updated_params()
}
