// get words to learn from DB
let words_data = JSON.parse(
    document.querySelector('meta[name="words"]').getAttribute('data-words')
)
console.log(words_data)
let studies_words = {}

// create support variables
let translation_container = document.getElementById('translations')
let current_word_number = 0;
let max_word_number = Object.keys(words_data).length
let words = Object.keys(words_data)
let random
let word

// add event listeners
document.getElementById("all").innerHTML = max_word_number
document.getElementById("correct").addEventListener("click", addvalue);
document.getElementById("wrong").addEventListener("click", minusvalue);
document.getElementById("finish").addEventListener("click", finish);

// load first word
next_word()

// make textare content visible
function show() {
    for (textarea of translation_container.getElementsByClassName('trans')) {
        textarea.getElementsByTagName('textarea')[0].style.color = 'black'
    }
}

// upload results to DB
function finish() {
    console.log(studies_words);

    const data = {
        data: JSON.stringify(studies_words)
    };

    fetch('/finish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text(); // or response.json() if server returns JSON
        })
        .then(() => {
            alert('Completed');
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}


function next_word() {
    if (max_word_number > current_word_number) {
        current_word_number += 1
        random = Math.floor(Math.random() * words.length)
        word = words[random]
        let parts = (words_data[word]['parts'])
        words.splice(random, 1)
        check(parts)
        document.getElementById("current").innerHTML = current_word_number
        document.getElementById("word").innerHTML = word
    }
    else {
    }
}

// decrease words answer value
function minusvalue() {
    if (words_data[word]['answer'] > 0) {
        if (!studies_words[word]) {
            studies_words[word] = {}
        }
        studies_words[word]['answer'] = words_data[word]['answer'] - 10
    }
    else {
        if (!studies_words[word]) {
            studies_words[word] = {}
        }
        studies_words[word]['answer'] = words_data[word]['answer']
    }
    next_word()
}


// increase words answer value
function addvalue() {
    if (words_data[word]) {
        if (!studies_words[word]) {
            studies_words[word] = {}
        }
        studies_words[word]['answer'] = words_data[word]['answer'] + 10
    }
    next_word()
}

function check(word_parts) {
    clear_translations()
    for (let part of Object.keys(word_parts)) {
        create_translation(part)

        translation_container.lastElementChild.getElementsByTagName('textarea')[0].innerHTML =
            word_parts[part].join('\r\n')
        translation_container.lastElementChild.getElementsByTagName('textarea')[0].style.color = 'white'
    }
    document.querySelectorAll('textarea').forEach(item => { item.addEventListener('click', show) })
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
    let option = document.createElement('option')
    option.value = temp
    option.innerHTML = temp
    parent.appendChild(option)
}


function clear_translations() {
    translation_container.innerHTML = ''
}