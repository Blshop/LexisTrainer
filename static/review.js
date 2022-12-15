let word_number = 0;
let max_words = Object.keys(list_data).length
let keys = Object.keys(list_data)
let random
let ru_word
let parts
console.log(list_data)
document.getElementById("all").innerHTML = max_words
document.getElementById("correct").addEventListener("click", addvalue);
document.getElementById("wrong").addEventListener("click", minusvalue);
document.getElementById("finish").addEventListener("click", finish);
document.getElementById("translation-0").addEventListener("click", show);
document.getElementById("translation-1").addEventListener("click", show);
document.getElementById("translation-2").addEventListener("click", show);

next_word()

function show() {
    document.getElementById("translation-0").style.color = 'black'
    document.getElementById("translation-1").style.color = 'black'
    document.getElementById("translation-2").style.color = 'black'
}

function finish() {
    $(document).ready(function () {
        var data = {
            data: JSON.stringify(list_data)
        }
        $.ajax({
            url: "/review_finish",
            type: 'POST',
            data: data,
            success: function (msg) {
                alert(msg.name)
            }
        })
    });
}

function next_word() {
    document.getElementById("translation-0").style.color = 'white'
    document.getElementById("translation-1").style.color = 'white'
    document.getElementById("translation-2").style.color = 'white'
    document.getElementById("part-0").style.color = 'white'
    document.getElementById("part-1").style.color = 'white'
    document.getElementById("part-2").style.color = 'white'
    document.getElementById("translation-0").innerHTML = ''
    document.getElementById("translation-1").innerHTML = ''
    document.getElementById("translation-2").innerHTML = ''

    if (max_words > word_number) {
        word_number += 1
        random = Math.floor(Math.random() * keys.length)
        ru_word = keys[random]
        parts = Object.keys(list_data[ru_word])
        console.log(parts)
        keys.splice(random, 1)
        document.getElementById("current").innerHTML = word_number
        document.getElementById("word").innerHTML = ru_word
        for (i in parts) {
            document.getElementById('id' + i).style.display = "flex"
            document.getElementById('part-' + i).innerHTML = parts[i]
            document.getElementById("part-" + i).style.color = 'black'
            document.getElementById("translation-" + i).innerHTML = list_data[ru_word][parts[i]][1].join('\r\n')
        }
        // document.getElementById("2").innerHTML = ''
        // document.getElementById("3").innerHTML = list_data[word_number][2]
        // document.getElementById("4").innerHTML = list_data[word_number][3]
    }

}
function minusvalue() {
    parts = Object.keys(list_data[ru_word])
    for (i in parts) {
        list_data[ru_word][parts[i]][0] = 0

    }

    if (word_number == max_words) {
        document.getElementById("translation-0").innerHTML = 'Finished'
        document.getElementById("translation-1").innerHTML = 'Finished'
        document.getElementById("translation-2").innerHTML = 'Finished'
    }
    else {
        next_word()
    }
}

function addvalue() {
    parts = Object.keys(list_data[ru_word])
    if (word_number == max_words) {
        document.getElementById("translation-0").innerHTML = 'Finished'
        document.getElementById("translation-1").innerHTML = 'Finished'
        document.getElementById("translation-2").innerHTML = 'Finished'
    }
    else { next_word() }


}