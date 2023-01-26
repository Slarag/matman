const draggables = document.querySelectorAll('.draggable');
const containers = document.querySelectorAll('.drag-container')
const clonable = document.querySelector('.draggable:last-child')
const submitButtons = [
    document.querySelector('#buttonSave'),
    document.querySelector('#buttonAddAnother'),
]

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
    })

    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')
    })
})

containers.forEach(container => {
    container.addEventListener('dragover', e => {
        e.preventDefault()
        const afterElement = getDragAfterElement(container, e.clientY)
        const draggable = document.querySelector('.dragging')
        if (afterElement == null) {
            container.appendChild(draggable)
        } else {
            container.insertBefore(draggable, afterElement)
        }
        const ordered_items = [...container.querySelectorAll('.draggable')]
        for (const [index, element] of ordered_items.entries()) {
            var old = element.querySelector('[id$="ORDER"]').value
            element.querySelector('[id$="ORDER"]').value = index
          }
    })
})

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')]

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
            return {offset: offset, element: child}
        } else {
            return closest
        }
    }, {offset: Number.NEGATIVE_INFINITY}).element
}


function cloneForm() {
    const newElement = clonable.cloneNode(true)
    var total = document.querySelector('[id$=-TOTAL_FORMS]').value
    newElement.querySelectorAll('input').forEach( input => {
        input.name = input.name.replace(RegExp('-\\d-'),'-' + total + '-')
        input.id = 'id_' + input.name
        input.value = null
    })
    newElement.querySelectorAll('label').forEach( label => {
        label.htmlFor = label.htmlFor.replace(RegExp('-\\d-'),'-' + total + '-')
    })
    newElement.querySelectorAll('label,div').forEach( node => {
        node.id = node.id.replace(RegExp('-\\d-'),'-' + total + '-')
    })
    total++;
    document.querySelector('[id$=-TOTAL_FORMS]').value = total
    clonable.parentNode.appendChild(newElement)
}


function onLoad(clicked) {
    // Disable all submit buttons when form is being submitted and display a spinner on the clicked button
    clicked.classList.add('loading')
    submitButtons.forEach( button =>{
        button.classList.add('disabled')
    })
}


document.querySelector('#add-more').addEventListener('click', () => {
    cloneForm()
})


submitButtons.forEach( button =>{
    button.addEventListener('click', () => {
        onLoad(button)
    })
})