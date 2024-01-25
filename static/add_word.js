// load words and parts from DB
let word_list = JSON.parse(
  document.querySelector('meta[name="words"]').getAttribute('data-words')
)
let parts = JSON.parse(
  document.querySelector('meta[name="parts"]').getAttribute('data-parts')
)

// create support variables
let translation_container = document.getElementById('translations')
var input = document.getElementById('word')

// add events to elements
input.addEventListener('input', verify_word)
document.getElementById('add').addEventListener('click', create_translation)
document.getElementById('submit').addEventListener('click', prep_word)

// verify if word already in DB
function verify_word() {
  if (word_list.indexOf(input.value.trim()) !== -1) {
    input.style.outline = '3px solid red'
  } else {
    input.style.outline = '3px solid green'
  }
}

// load existing word from DB
function load_word() {
  fetch('/get_word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(input.value.trim())
  })
    .then(response => response.json())
    .then(json => check(json))
}

function noenter() {
  if (window.event.keyCode == 13) {
    load_word()
  }
  return !(window.event.keyCode == 13)
}

function check(word) {
  let word_parts = word['parts']
  clear_translations()
  for (let part of Object.keys(word_parts)) {
    create_translation(part)
    translation_container.lastElementChild.getElementsByTagName('textarea')[0].innerHTML =
      word_parts[part].join('\r\n')
  }
  document.getElementById('id').value = word['id']
}

function tip(word) {
  document.getElementById('word').value = word
  verify_word()
  load_word()
}

function create_translation(word_part = '') {
  let trans = document.createElement('div')
  trans.classList.add('trans')
  trans.innerHTML = `
        <select name="part">
        </select>
        <label for="translation">translation</label>
        <textarea name="translation" placeholder="translation"></textarea>
        <input type="text" name="answer" autocomplete="off" list="autocompleteOff" />
    `

  translation_container.appendChild(trans)
  let parent = translation_container.lastElementChild.getElementsByTagName('select')[0]

  for (let part of parts) {
    let option = document.createElement('option')
    option.value = part
    option.innerHTML = part
    if (part == word_part) { option.setAttribute('selected', 'selected') }
    parent.appendChild(option)
  }
}

function clear_translations() {
  translation_container.innerHTML = ''
}

create_translation()


function prep_word() {
  let parts = {}
  for (let parent of translation_container.getElementsByClassName('trans')) {
    console.log(parent)
    parts[parent.getElementsByTagName('select')[0].value] = parent.getElementsByTagName('textarea')[0].value.split('\n')
    console.log(parts)
  }
  if (input.value != "") {
    var prepared_word = {
      'word': input.value,
      'id': document.getElementById('id').value,
      'answer': 0,
      'parts': parts
    }
  }
  console.log(prepared_word)
  upload_word(prepared_word)
  window.location.href = "http://127.0.0.1:5000/add_words";
}


function upload_word(word) {
  fetch('/add_words', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(word)
  })
}