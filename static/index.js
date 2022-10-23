active_lang(language)

function active_lang(language) {
    if (language == 'russian') {
        document.getElementById('rus').classList.add('active')
        document.getElementById('eng').classList.remove('active')
    }
    else {
        document.getElementById('eng').classList.add('active')
        document.getElementById('rus').classList.remove('active')
    }
}

function lang_select(language) {
    active_lang(language)
    fetch('/set_lang', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(language),
    })
        .then((response) => response.text())
        .then((data) => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

document.getElementById("eng").addEventListener("click", function () { lang_select("english") })
document.getElementById("rus").addEventListener("click", function () { lang_select("russian") })