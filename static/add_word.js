var input = document.getElementById('word');
document.getElementById("result").addEventListener("click", check);

function check() {
    if (word_list.indexOf(input.value) !== -1) {
        alert("Value exists!")
    } else {
        alert("Value does not exists!")
    }
}

document.getElementById('add').addEventListener('click', show)

function show() {
    if (document.getElementById('id1').style.display == 'flex') {
        document.getElementById('id2').style.display = 'flex'
    }
    else {
        document.getElementById('id1').style.display = 'flex'
    }

}