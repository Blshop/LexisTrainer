let all_words = JSON.parse(
    document.querySelector('meta[name="words"]').getAttribute('data-words')
)
let parts = JSON.parse(
    document.querySelector('meta[name="parts"]').getAttribute('data-parts')
)
console.log(parts)
let translation_container = document.getElementById('translations')
console.log(all_words)
let word_number = 0;
let max_words = Object.keys(all_words).length
console.log(max_words)
let keys = Object.keys(all_words)
console.log(keys)
let random
let ru_word
document.getElementById("all").innerHTML = max_words
document.getElementById("correct").addEventListener("click", addvalue);
document.getElementById("wrong").addEventListener("click", minusvalue);
document.getElementById("finish").addEventListener("click", finish);
next_word()

function show() {
    for (textarea of translation_container.lastElementChild.getElementsByTagName('textarea')) {
        textarea.style.color = 'black'
    }
}

function finish() {
    $(document).ready(function () {
        var data = {
            data: JSON.stringify(all_words)
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
    if (max_words > word_number) {
        word_number += 1
        random = Math.floor(Math.random() * keys.length)
        ru_word = keys[random]
        console.log(ru_word)
        let partss = (all_words[ru_word]['parts'])
        console.log(partss)
        keys.splice(random, 1)
        check(partss)
        document.getElementById("current").innerHTML = word_number
        document.getElementById("word").innerHTML = ru_word
        // for (i in parts) {
        //     document.getElementById('id' + i).style.display = "flex"
        //     document.getElementById('part-' + i).innerHTML = parts[i]
        //     document.getElementById("part-" + i).style.color = 'black'
        //     document.getElementById("translation-" + i).innerHTML = list_data[ru_word][parts[i]]['translation'].join('\r\n')
        // }
    }

}
function minusvalue() {
    // parts = Object.keys(list_data[ru_word])
    // for (i in parts) {
    //     if (list_data[ru_word][parts[i]]['amswer'] > 0) {
    //         list_data[ru_word][parts[i]]['answer'] -= 10
    //     }
    // }
    if (all_words[ru_word]['answer'] > 0) {
        all_words[ru_word]['answer'] += 10
    }

    if (word_number == max_words) {
        finish()
        // document.getElementById("translation-0").innerHTML = 'Finished'
        // document.getElementById("translation-1").innerHTML = 'Finished'
        // document.getElementById("translation-2").innerHTML = 'Finished'
    }
    else {
        next_word()
    }
}

function addvalue() {
    // parts = Object.keys(list_data[ru_word])
    // for (i in parts) {
    //     list_data[ru_word][parts[i]]['answer'] += 10
    //     console.log(list_data[ru_word][parts[i]]['answer'])
    // }
    all_words[ru_word]['answer'] += 10
    if (word_number == max_words) {
        finish()
        // document.getElementById("translation-0").innerHTML = 'Finished'
        // document.getElementById("translation-1").innerHTML = 'Finished'
        // document.getElementById("translation-2").innerHTML = 'Finished'
    }
    else { next_word() }


}

function check(word_parts) {
    clear_translations()
    for (let part of Object.keys(word_parts)) {
        create_translation(part)
        translation_container.lastElementChild.getElementsByTagName('textarea')[0].innerHTML =
            word_parts[part].join('\r\n')
        translation_container.lastElementChild.getElementsByTagName('textarea')[0].style.color = 'white'
        translation_container.lastElementChild.getElementsByTagName('textarea')[0].addEventListener('click', show)
    }
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
    console.log(parts)
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