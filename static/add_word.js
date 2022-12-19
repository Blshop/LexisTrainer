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
    let parts = Object.keys(word)
    if (true) {
        for (i in parts) {
            document.getElementById('id' + i).style.display = "flex"
            document.getElementById('part-' + i).value = parts[i]
            document.getElementById("translation-" + i).innerHTML = word[parts[i]]['translation'].join('\r\n')
            document.getElementById("id-" + i).value = word[parts[i]]['id']
            document.getElementById("answer-" + i).value = word[parts[i]]['answer']
        }
    } else {
        alert("Value does not exists!")
    }
}

function tip(word) {
    document.getElementById("word").value = word
    verify_value()
    load_word()
}