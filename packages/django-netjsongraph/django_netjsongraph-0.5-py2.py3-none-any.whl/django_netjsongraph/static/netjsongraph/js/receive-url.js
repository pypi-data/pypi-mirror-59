(function ($) {
    'use strict';
    $(document).ready(function () {
        var p = $('.field-receive_url p, .field-receive_url > div > div'),
            value = window.location.origin + p.text();
        p.html('<input readonly id="id_receive_url" type="text" class="vTextField readonly" value="' + value + '">');
        var field = $('#id_receive_url');
        field.click(function () {
            $(this).select();
        });
    });
}(django.jQuery));
