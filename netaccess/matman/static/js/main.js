$(document).ready(function(){
{% block domready %}
{% endblock %}
})


function update_get_parameters(name, value){
    let dict = {};
    const get_params = window.location.search.split('?')[1].split('&');
    for (const param of get_params) {
        let name, value;
        [name, value] = param.split('=', 2);
        dict[name] = value;
    }
}



