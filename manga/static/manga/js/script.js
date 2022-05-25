$(document).ready(function () {
    $('.menu__burger').click(function (event) {
        $('.menu__list, .menu__burger').toggleClass('active');
        $('body').toggleClass('lock');
    }
    )
}
)