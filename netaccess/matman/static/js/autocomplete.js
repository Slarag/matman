function autocomplete(inp, url, param) {

  var currentFocus, arr = []

  function get_suggestions(value) {
    const ajaxRequest = new XMLHttpRequest();
    ajaxRequest.onreadystatechange = function(){
      if(ajaxRequest.readyState == 4 && ajaxRequest.status == 200) {
        arr = JSON.parse(ajaxRequest.responseText)['suggestions'];
        redraw_suggestions();
      }
    }
    ajaxRequest.open("GET", url + "?" + param"=" + encodeURIComponent(value), true);
    ajaxRequest.send();
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

autocomplete(document.getElementById("id_tags"), "/utils/tags", "value");

