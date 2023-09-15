let word_list = JSON.parse(
  document.querySelector('meta[name="words"]').getAttribute('data-words')
)
let parts = JSON.parse(
  document.querySelector('meta[name="parts"]').getAttribute('data-parts')
)
let translation_container = document.getElementById('translations')

var input = document.getElementById('word')
input.addEventListener('input', verify_word)
document.getElementById('add').addEventListener('click', show)
document.getElementById('submit').addEventListener('click', prep_word)
function show() {
  create_translation()
  translation_counter += 1
}

function verify_word() {
  if (word_list.indexOf(input.value.trim()) !== -1) {
    input.style.outline = '3px solid red'
  } else {
    input.style.outline = '3px solid green'
  }
}

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

function create_translation(temp) {
  translation_container.innerHTML +=
    `
    <div class="trans">
        <label for="part">part</label>
        <select name="part">
        </select>
        <label for="translation">translation</label>
        <textarea name="translation" placeholder="translation"></textarea>
        <input type="text" name="answer" autocomplete="off" list="autocompleteOff" />
    </div>
    `
  let parent = translation_container.lastElementChild
    .getElementsByTagName('select')[0]
  for (let part of parts) {
    let option = document.createElement('option')
    option.value = part
    option.innerHTML = part
    if (part == temp) { option.setAttribute('selected', 'selected') }
    parent.appendChild(option)
  }
}

function clear_translations() {
  translation_container.innerHTML = ''
}

create_translation(1)


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
  // location.reload()
}


function upload_word(word) {
  fetch('/add_word', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(word)
  })
}