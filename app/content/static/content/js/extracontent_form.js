// window.addEventListener("load", function() {
$(document).ready(function(){
    (function($) {
        $(function() {
            var modelname = 'extracontent',
                suffix = '_form',
                trigger_field_name = 'content_type'
                // inline_group = $('#'+modelname+suffix+'-group');

            function process_the_forms(){

                function show_fields_by_value(target, value) {
                    target.find('.form-row').hide();
                    target.find('.order').show();
                    target.find('.tied_to_menu').show();
                    target.find('.position').show();
                    target.find('.show_title').show();
                    target.find('.'+trigger_field_name).show();
                    if(value){
                        target.find('div[class*=form-row][class*='+ value+']').show();
                    }
                }
                // inline_group.find('[id^='+modelname+suffix+']').each(function(){
                var form = $('#' + modelname + suffix),
                    // num = $(this).attr('id').substring(modelname.length + suffix.length),
                    trigger_field = form.find('select[id$='+ trigger_field_name +']');

                show_fields_by_value(form, trigger_field.val());

                trigger_field.change(function(){
                    show_fields_by_value(form, $(this).val());
                });
                // });
            }

            process_the_forms();

            // inline_group.find('a.grp-add-handler').click(function(){
            //     inline_group.find('[id^='+modelname+suffix+']').each(function(){
            //         process_the_forms();
            //     });
            // });

        });

    })(django.jQuery);
});