// load selected languages from DB
let active_languages = JSON.parse(
  document
    .querySelector('meta[name="active_languages"]')
    .getAttribute('data-active_languages')
)

// variables to store primary and secondary languages
var primary_element = document.getElementById(
  'primary-' + active_languages['primary_language']
)
var secondary_element = document.getElementById(
  'secondary-' + active_languages['secondary_language']
)

// apply previously set languages
if (active_languages != null) {
  primary(primary_element, secondary_element)
}


function lang_select() {
  if (primary_element != null && secondary_element != null) {
    fetch('/set_lang', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        primary_language: primary_element.innerHTML,
        secondary_language: secondary_element.innerHTML
      })
    })
  }
}

function primary(new_element) {
  if (new_element.classList.contains('selected')) {
    new_element.classList.remove('selected')
    var secondaries = document.getElementById('secondary-language').children
    for (i = 0; i < secondaries.length; i++) {
      secondaries[i].classList.add('inactive')
      secondaries[i].classList.remove('selected')
    }
    primary_element = null
    secondary_element = null
    console.log(primary_element)
  } else {
    if (primary_element != null) {
      primary_element.classList.remove('selected')
    }
    new_element.classList.add('selected')
    primary_element = new_element
    secondary(secondary_element)
  }
}

function secondary(new_element = null) {
  var secondaries = document.getElementById('secondary-language').children
  for (i = 0; i < secondaries.length; i++) {
    secondaries[i].classList.remove('inactive')
    secondaries[i].classList.remove('selected')
  }
  document
    .getElementById('secondary-' + primary_element.innerHTML)
    .classList.add('inactive')
  if (new_element != null) {
    secondary_element = new_element
    secondary_element.classList.add('selected')
  }
  lang_select()
}

function set_default() {
  var secondaries = document.getElementById('secondary-language').children
  for (i = 0; i < secondaries.length; i++) {
    secondaries[i].classList.add('inactive')
    secondaries[i].classList.remove('selected')
  }
}