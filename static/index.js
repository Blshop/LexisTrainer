let active_languages = JSON.parse(
  document
    .querySelector('meta[name="active_languages"]')
    .getAttribute('data-active_languages')
)

var primary_element
var secondary_element

if (active_languages == null) {
  primary_element = null
  secondary_element = null
} else {
  primary_element = document.getElementById(
    'primary-' + active_languages['primary_language']
  )
  secondary_element = document.getElementById(
    'secondary-' + active_languages['secondary_language']
  )
  primary(primary_element, secondary_element)
}

function set_primary_language(event) {
  let new_element = event.target
  primary(new_element)
}

function set_secondary_language(event) {
  let new_element = event.target
  secondary(new_element)
  lang_select()
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
  if (new_element.classList.contains('active')) {
    new_element.classList.remove('active')
    var secondaries = document.getElementById('secondary-language').children
    for (i = 0; i < secondaries.length; i++) {
      secondaries[i].classList.add('inactive')
      secondaries[i].classList.remove('active')
    }
    primary_element = null
    secondary_element = null
    console.log(primary_element)
  } else {
    if (primary_element != null) {
      primary_element.classList.remove('active')
    }
    new_element.classList.add('active')
    primary_element = new_element
    secondary(secondary_element)
  }
}

function secondary(new_element = null) {
  var secondaries = document.getElementById('secondary-language').children
  for (i = 0; i < secondaries.length; i++) {
    secondaries[i].classList.remove('inactive')
    secondaries[i].classList.remove('active')
  }
  document
    .getElementById('secondary-' + primary_element.innerHTML)
    .classList.add('inactive')
  if (new_element != null) {
    secondary_element = new_element
    secondary_element.classList.add('active')
  }
}
