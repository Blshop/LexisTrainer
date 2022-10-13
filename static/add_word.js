document.getElementById('add').addEventListener('click', show)

function show() {
    if (document.getElementById('id1').style.display == 'flex') {
        document.getElementById('id2').style.display = 'flex'
    }
    else {
        document.getElementById('id1').style.display = 'flex'
    }

}