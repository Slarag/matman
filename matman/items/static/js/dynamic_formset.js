const clonable = document.querySelector('.draggable:last-child');
const submitButtons = [
    document.querySelector('#buttonSave'),
    document.querySelector('#buttonAddAnother'),
];


function cloneForm() {
    const newElement = clonable.cloneNode(true);
    var total = document.querySelector('[id$=-TOTAL_FORMS]').value;
    newElement.querySelectorAll('input').forEach( input => {
        input.name = input.name.replace(RegExp('-\\d-'),'-' + total + '-');
        input.id = 'id_' + input.name;
        input.value = null;
    })
    newElement.querySelectorAll('label').forEach( label => {
        label.htmlFor = label.htmlFor.replace(RegExp('-\\d-'),'-' + total + '-');
    })
    newElement.querySelectorAll('label,div').forEach( node => {
        node.id = node.id.replace(RegExp('-\\d-'),'-' + total + '-');
    })
    total++;
    document.querySelector('[id$=-TOTAL_FORMS]').value = total;
    clonable.parentNode.appendChild(newElement);
}


function onLoad(clicked) {
    // Disable all submit buttons when form is being submitted and display a spinner on the clicked button
    clicked.classList.add('loading');
    submitButtons.forEach( button =>{
        button.classList.add('disabled');
    })
}


document.querySelector('#add-more').addEventListener('click', () => {
    cloneForm();
})


submitButtons.forEach( button =>{
    if (button != null){
        button.addEventListener('click', () => {
            onLoad(button);
        })
    }
})