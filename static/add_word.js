document.getElementById('add').addEventListener('click', show)

function show() {
    if (document.getElementById('two').style.display == 'flex') {
        document.getElementById('three').style.display = 'flex'
    }
    else {
        document.getElementById('two').style.display = 'flex'
    }

}