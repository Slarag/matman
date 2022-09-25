const draggables = document.querySelectorAll('.draggable');
const containers = document.querySelectorAll('.drag-container')
const clonable = document.querySelector('.draggable:last-child')
const type = 'pictures'

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
            console.log(old, ' -> ', index);
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
    // var newElement = $(selector).clone(true);
    // var total = $('#id_' + type + '-TOTAL_FORMS').val();
    var total = document.querySelector('#id_' + type + '-TOTAL_FORMS').value
    newElement.querySelectorAll('input').forEach( input => {
        input.name = input.name.replace('-' + (total-1) + '-','-' + total + '-')
        input.id = 'id_' + input.name
        input.value = null
    })
    newElement.querySelectorAll('label').forEach( label => {
        label.htmlFor = label.htmlFor.replace('-' + (total-1) + '-','-' + total + '-')
    })
    total++;
    document.querySelector('#id_' + type + '-TOTAL_FORMS').value = total
    clonable.parentNode.appendChild(newElement)
}


document.querySelector('#add-more').addEventListener('click', () => {
    cloneForm()
})
