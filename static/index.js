
let lang = ""
function lang_select(language, id_1, id_2) {
    lang = language
    document.getElementById(id_1).classList.toggle('active')
    document.getElementById(id_2).classList.toggle('active')
    fetch('/set_lang', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(lang),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

document.getElementById("eng").addEventListener("click", function () { lang_select("english", 'eng', 'rus') })
document.getElementById("rus").addEventListener("click", function () { lang_select("russian", 'rus', 'eng') })