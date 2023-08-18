let active_languages
let primary_language = ''
let secondary_language = ''
let primary_element
let secondary_element

if (active_languages != null) {
  active_languages = JSON.parse(
    document
      .querySelector('meta[name="active_languages"]')
      .getAttribute('data-active_languages')
  )
  primary_language = active_languages['primary_language']
  secondary_language = active_languages['secondary_language']
  primary_element = document.getElementById('primary-' + primary_language)
  secondary_element = document.getElementById('secondary-' + secondary_language)
  primary_element.classList.add('active')
  secondary_element.classList.add('active')
}

function set_primary_language () {
  let new_element = event.target
  if (new_element.classList.contains('active')) {
    new_element.classList.remove('active')
    document
      .getElementById('secondary-' + new_element.innerHTML)
      .classList.toggle('inactive')
    primary_language = ''
    primary_element = null
  } else {
    new_element.classList.add('active')
    let inactive_language = document.getElementsByClassName('inactive')[0]
    if (secondary_language == new_element.innerHTML) {
      secondary_element.classList.toggle('active')
      secondary_language = ''
      secondary_element = null
    }
    if (inactive_language != null) {
      inactive_language.classList.toggle('inactive')
    }
    if (primary_element != null) {
      primary_element.classList.remove('active')
    }
    document
      .getElementById('secondary-' + new_element.innerHTML)
      .classList.toggle('inactive')
    primary_element = new_element
    primary_language = new_element.innerHTML
  }
  if (primary_language != '' && secondary_language != '') {
    lang_select(primary_language, secondary_language)
  }
}

function set_secondary_language () {
  let new_element = event.target
  if (new_element.classList.contains('active')) {
    new_element.classList.remove('active')
    secondary_language = ''
    secondary_element = null
  } else {
    new_element.classList.add('active')
    if (secondary_element != null) {
      secondary_element.classList.remove('active')
    }
    secondary_element = new_element
    secondary_language = new_element.innerHTML
  }

  if (primary_language != '' && secondary_language != '') {
    lang_select(primary_language, secondary_language)
  }
}

function lang_select (primary_language, secondary_language) {
  console.log(primary_language, secondary_language)
  fetch('/set_lang', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "primary_language": primary_language,
      "secondary_language": secondary_language
    })
  })
}
