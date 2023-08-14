let word_list = JSON.parse(document.getElementsByTagName('meta')[3].getAttribute('data-words'))
let parts = JSON.parse(document.getElementsByTagName('meta')[4].getAttribute('data-parts'))
// console.log(JSON.parse(word_list))
// console.log(JSON.parse(JSON.parse(word_list)))

let translation_counter = 0
var input = document.getElementById('word');
input.addEventListener('input', verify_value);
document.getElementById('add').addEventListener('click', show)

function show() {
    create_translation()
    translation_counter += 1
}


function verify_value() {
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
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(input.value.trim()),
    })
        .then((response) => response.json())
        .then(json => check(json))
}


function noenter() {
    if (window.event.keyCode == 13) {
        load_word()
    }
    return !(window.event.keyCode == 13);
}


function check(word) {
    let word_parts = word['parts']
    clear_translations()
    for (let i = 0; i < Object.keys(word_parts).length; i++) {
        create_translation()
    }
    temp = 1
    for (let part of Object.keys(word_parts)) {
        let parent = document.getElementById(temp)
        parent.getElementsByTagName('select')[0].value = part
        parent.getElementsByTagName('textarea')[0].innerHTML = word_parts[part].join('\r\n')
        temp += 1
    }
    document.getElementById("id").value = word['id']
}

function tip(word) {
    document.getElementById("word").value = word
    verify_value()
    load_word()
}


function create_translation() {
    translation_counter += 1
    var parent_container = document.getElementsByClassName('translations')[0]
    parent_container.innerHTML += `
    <div class="trans" id="`+ translation_counter + `">
        <label for="part">part</label>
        <select name="part">
        </select>
        <label for="translation">translation</label>
        <textarea name="translation" placeholder="translation"></textarea>
        <input type="text" name="answer" autocomplete="off" list="autocompleteOff" />
    </div>
    `
    parent = document.getElementById(translation_counter).getElementsByTagName('select')[0]
    parent.id = translation_counter + 10
    for (let part of parts) {
        var option = document.createElement('option')
        option.value = part
        option.innerHTML = part
        parent.appendChild(option)
    }
}

function clear_translations() {
    for (let i = 1; i <= translation_counter; i++) {
        document.getElementById(i).remove()

    }
    translation_counter = 0
}

create_translation()