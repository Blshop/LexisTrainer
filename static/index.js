let main_language = ''
let secondary_language = ''

function get_main_language() {
    let main_container = document.querySelector('#main-language')
    let current_active_language = main_container.querySelector('.active')
    selected_language = event.target
    main_language = selected_language.classList.value
    selected_language.classList.add('active')
    if (current_active_language != null) {
        current_active_language.classList.remove('active')
        main_language = ''
    }
    if ((main_language != "") && (secondary_language != "")) {
        lang_select(main_language, secondary_language)
    }
}

function get_secondary_class_name() {
    let main_container = document.querySelector('#secondary-language')
    let current_active_language = main_container.querySelector('.active')
    selected_language = event.target
    secondary_language = selected_language.classList.value
    selected_language.classList.add('active')
    if (current_active_language != null) {
        current_active_language.classList.remove('active')
        secondary_language = ''
    }
    if ((main_language != "") && (secondary_language != "")) {
        lang_select(main_language, secondary_language)
    }
}

function lang_select(main_language, secondary_language) {
    fetch('/set_lang', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'main_language': main_language, 'secondary_language': secondary_language }),
    });
}
