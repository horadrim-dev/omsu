// window.addEventListener("load", function() {
$(document).ready(function(){
    (function($) {
        $(function() {
            var selectField = $('#id_menu');
                // verified = $('#id_verified');

            function toggleVerified(value) {
                // value == 'value2' ? verified.show() : verified.hide();
                alert(value);
            }

            // show/hide on load based on pervious value of selectField
            toggleVerified(selectField.val());

            // show/hide on change
            selectField.change(function() {
                toggleVerified($(this).val());
            });
        });

        // $('#id_menu').on('change', function() {
        //     alert($(this).val())
        // });
    })(django.jQuery);
});