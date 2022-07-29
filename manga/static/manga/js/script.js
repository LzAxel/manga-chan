function ready(callback){
    // in case the document is already rendered
    if (document.readyState!='loading') callback();
    // modern browsers
    else if (document.addEventListener) document.addEventListener('DOMContentLoaded', callback);
    // IE <= 8
    else document.attachEvent('onreadystatechange', function(){
        if (document.readyState=='complete') callback();
    });
}

ready(function(){

    const checkboxes = document.querySelectorAll('.check-box--exclude')

    checkboxes.forEach(cb => {
        cb.addEventListener('change', (event) => {

            cb.checked = true
            if (cb.name == 'tags_include') {
                cb.name = 'tags_exclude';
            } else if (cb.name == 'tags_exclude'){
                cb.name = '';
            } else {
                cb.name = 'tags_include';
            }
          })
    })


    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var tags_included = urlParams.getAll('tags_include')
    console.log(tags_included)
    var tags_excluded = urlParams.getAll('tags_exclude')
    var status = urlParams.getAll('status')

    tags_included.forEach(tag => {
        console.log(tag);
        var cb = document.getElementById(tag);
        cb.name = 'tags_include';
        cb.checked = true;
    })
    tags_excluded.forEach(tag => {
        console.log(tag);
        var cb = document.getElementById(tag);
        cb.name = 'tags_exclude';
        cb.checked = true;
    })
    status.forEach(tag => {
        console.log(tag);
        var cb = document.getElementById(tag);
        cb.checked = true;
    })

    let prevLink = document.getElementById("prevLink");
    let nextLink = document.getElementById("nextLink");
    document.addEventListener("keydown", ({key}) => {
    switch (key) {
        case 'ArrowLeft':
        prevLink.click();
        break;
        case 'ArrowRight':
        nextLink.click();
        break;
    }
    });

    document.querySelector('.filter__button').addEventListener('click', () => {
        document.querySelector('.filter__form').classList.toggle('active');
        document.querySelector('.filter__menu').classList.toggle('active');
        document.querySelector('body').classList.toggle('lock');
    });

}); 

