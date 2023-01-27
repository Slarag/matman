function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function suggest_tags(inp) {

  var currentFocus, arr = []

  function get_suggestions(value) {
    fetch("/utils/tags?value=" + encodeURIComponent(value), {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        arr = data['suggestions']
        redraw_suggestions();
    })
  }

  inp.addEventListener("input", e => {
    get_suggestions(inp.value.split(',').pop().trim())
    redraw_suggestions()
  })

  function redraw_suggestions() {
    var list_div, item_div, val = inp.value.split(',').pop().trim()
    closeAllLists()

    if (!val) return false;
    currentFocus = -1

    list_div = document.createElement("DIV")
    list_div.setAttribute("id", this.id + "autocomplete-list")
    list_div.setAttribute("class", "autocomplete-items list-group")
    inp.parentNode.appendChild(list_div)

    arr.forEach( suggestion => {
      if (suggestion.toLowerCase().startsWith(val.toLowerCase())) {
        item_div = document.createElement("DIV")
        item_div.setAttribute("class", "list-group-item list-group-item-secondary list-group-item-action")
        item_div.innerHTML = "<strong>" + suggestion.substr(0, val.length) + "</strong>"
        item_div.innerHTML += suggestion.substr(val.length)
        item_div.innerHTML += "<input type='hidden' value='" + suggestion + "'>"
        item_div.addEventListener("click", function(e) {
            var tags = inp.value.split(',').map(item => item.trim())
            tags.pop()
            tags.push(this.getElementsByTagName("input")[0].value)
            inp.value = tags.join(', ')
            closeAllLists()
        });
        list_div.appendChild(item_div)
      }
    })
  }

  inp.addEventListener("keydown", e => {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      //arrow DOWN
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      //arrow UP
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      //Enter
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });

  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("list-group-item-primary");
    x[currentFocus].classList.remove("list-group-item-secondary");
  }

  function removeActive(x) {
    [...x].forEach( item => {
        item.classList.add("list-group-item-secondary");
        item.classList.remove("list-group-item-primary");
    })
  }

  function closeAllLists(elmnt) {
    document.querySelectorAll(".autocomplete-items").forEach( item => {
      if (elmnt != item && elmnt != inp) {
        item.parentNode.removeChild(item)
      }
    })
  }

  document.addEventListener("click", e => {
    closeAllLists(e.target);
  });
}


function suggest_user(inp) {

  var currentFocus, arr = []

  function get_suggestions(value) {
    fetch("/utils/users?value=" + encodeURIComponent(value), {
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        arr = data['suggestions']
        redraw_suggestions();
    })
  }

  inp.addEventListener("input", e => {
    get_suggestions(inp.value.split(',').pop().trim())
    redraw_suggestions()
  })

  function redraw_suggestions() {
    var list_div, item_div, val = inp.value.split(',').pop().trim()
    closeAllLists()

    if (!val) return false;
    currentFocus = -1

    list_div = document.createElement("DIV")
    list_div.setAttribute("id", this.id + "autocomplete-list")
    list_div.setAttribute("class", "autocomplete-items list-group")
    inp.parentNode.appendChild(list_div)

    arr.forEach( suggestion => {
      if (suggestion.toLowerCase().startsWith(val.toLowerCase())) {
        item_div = document.createElement("DIV")
        item_div.setAttribute("class", "list-group-item list-group-item-secondary list-group-item-action")
        item_div.innerHTML = "<strong>" + suggestion.substr(0, val.length) + "</strong>"
        item_div.innerHTML += suggestion.substr(val.length)
        item_div.innerHTML += "<input type='hidden' value='" + suggestion + "'>"
        item_div.addEventListener("click", function(e) {
            inp.value = this.getElementsByTagName("input")[0].value
            closeAllLists()
        });
        list_div.appendChild(item_div)
      }
    })
  }

  inp.addEventListener("keydown", e => {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      //arrow DOWN
      currentFocus++;
      addActive(x);
    } else if (e.keyCode == 38) {
      //arrow UP
      currentFocus--;
      addActive(x);
    } else if (e.keyCode == 13) {
      //Enter
      e.preventDefault();
      if (currentFocus > -1) {
        if (x) x[currentFocus].click();
      }
    }
  });

  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("list-group-item-primary");
    x[currentFocus].classList.remove("list-group-item-secondary");
  }

  function removeActive(x) {
    [...x].forEach( item => {
        item.classList.add("list-group-item-secondary");
        item.classList.remove("list-group-item-primary");
    })
  }

  function closeAllLists(elmnt) {
    document.querySelectorAll(".autocomplete-items").forEach( item => {
      if (elmnt != item && elmnt != inp) {
        item.parentNode.removeChild(item)
      }
    })
  }

  document.addEventListener("click", e => {
    closeAllLists(e.target);
  });
}


//###############################
function toggle_bookmark(button) {
    fetch('/utils/bookmark/',
      {
        method: 'post',
        credentials: "same-origin",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest',
        },
        mode: 'same-origin',
        body: JSON.stringify({
          identifier: button.value,
        })
      })
      .then(response => response.json())
      .then(data => {
        is_bookmarked = data['bookmarked'];
        text_element = button.querySelector('.text');
        if (is_bookmarked){
            button.title = "Bookmarked";
            button.querySelector("i").classList.remove('bi-bookmark');
            button.querySelector("i").classList.add('bi-bookmark-check-fill');
            if(text_element){
                text_element.textContent = "Bookmarked";
            }
        }
        else {
            button.title = "Bookmark";
            button.querySelector("i").classList.remove('bi-bookmark-check-fill');
            button.querySelector("i").classList.add('bi-bookmark');
            if(text_element){
                text_element.textContent = "Bookmark";
            }
        }
      })
      .catch(function (error) {
        console.error(error);
      });
}


function checkCollapsables(element){
    event.preventDefault();
    // var baseUrl = window.location.href.split('?')[0];
    var url = new URL(element.href);
    var urlParams = new URLSearchParams(url.search);

    document.querySelectorAll('[id^=id_collapse_]').forEach(element => {
        var parameter = element.id.split('_')[2] + '_open';
        var value = String(element.classList.contains('show'));
        urlParams.set(parameter, value);
    });
    console.log(urlParams.toString());
    window.location = '?' + urlParams.toString();
    return false;
}
