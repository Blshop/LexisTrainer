let translation_number = 0
var input = document.getElementById('word');
input.addEventListener('input', verify_value);
document.getElementById('add').addEventListener('click', show)

function show() {
    if (document.getElementById('id1').style.display == 'flex') {
        document.getElementById('id2').style.display = 'flex'
    }
    else {
        document.getElementById('id1').style.display = 'flex'
    }
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
    console.log(word)
    let parts = word['parts']
    console.log(parts)
    document.getElementById("id").value = word['id']
    for (i in parts) {
        document.getElementById('part-' + i).value = parts[i]
        document.getElementById("translation-" + i).innerHTML = word[parts[i]]['translation'].join('\r\n')
        document.getElementById("id-" + i).value = word[parts[i]]['id']
        document.getElementById("answer-" + i).value = word[parts[i]]['answer']
    }
}

function tip(word) {
    document.getElementById("word").value = word
    verify_value()
    load_word()
}


function clear() {
    for (let i = 0; i < 3; i++) {
        document.getElementById('id' + i).style.display = "none"
        document.getElementById('part-' + i).value = ''
        document.getElementById("translation-" + i).innerHTML = ""
        document.getElementById("id-" + i).value = ''
        document.getElementById("answer-" + i).value = ''
    }
}

function create_translations() {
    var parent_container = document.getElementsByClassName('translations')[0]
    parent_container.innerHTML += `
    <div class="trans" id="id{{i}}">
                <label for="part-{{i}}">partdfgdfg</label>
                <select name="part-{{i}}" id="part-{{i}}">
                    <option value="noun">noun</option>
                    <option value="verb">verb</option>
                    <option value="adjective">adjective</option>
                    <option value="adverb">adverb</option>
                    <option value="misc">misc</option>
                </select>
                <label for="translation-{{i}}">translation</label>
                <textarea name="translation-{{i}}" placeholder="translation-{{i}}" id="translation-{{i}}"></textarea>
    </div>
    `
}

create_translations()