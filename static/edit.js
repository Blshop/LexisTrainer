var input = document.getElementById('word');
document.getElementById("check").addEventListener("click", check);
document.getElementById("add").addEventListener("click", show);
document.getElementById('id0').style.display = "flex"

function check() {
    clear()
    let parts = Object.keys(all_words[input.value])
    if (all_words[input.value] !== -1) {
        for (i in parts) {
            document.getElementById('id' + i).style.display = "flex"
            document.getElementById('part-' + i).value = parts[i]
            document.getElementById("translation-" + i).innerHTML = all_words[input.value][parts[i]][3].join('\r\n')
            document.getElementById("id-" + i).value = all_words[input.value][parts[i]][1]
            document.getElementById("answer-" + i).value = all_words[input.value][parts[i]][2]
        }
    } else {
        alert("Value does not exists!")
    }
}
function tip(word) {
    document.getElementById("word").value = word
    check()
}

function show() {
    if (document.getElementById('id1').style.display == 'flex') {
        document.getElementById('id2').style.display = 'flex'
    }
    else {
        document.getElementById('id1').style.display = 'flex'
    }
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