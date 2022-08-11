// window.addEventListener("load", function() {
$(document).ready(function(){
    (function($) {
        $(function() {
            var modelname = 'modulecontent',
                suffix = '_set',
                trigger_field_name = 'content_type',
                inline_group = $('#'+modelname+suffix+'-group');

            function process_the_forms(){

                function show_fields_by_value(target, value) {
                    target.find('.form-row').hide();
                    target.find('.order').show();
                    target.find('.'+trigger_field_name).show();
                    if(value){
                        target.find('div[class*=form-row][class*='+ value+']').show();
                    }
                }
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    var field_set = $(this),
                        num = $(this).attr('id').substring(modelname.length + suffix.length),
                        trigger_field = $(this).find('select[id$='+ trigger_field_name +']');

                    show_fields_by_value(field_set, trigger_field.val());

                    trigger_field.change(function(){
                        show_fields_by_value(field_set, $(this).val());
                    });
                });
            }

            process_the_forms();

            inline_group.find('a.grp-add-handler').click(function(){
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    process_the_forms();
                });
            });

        });

    })(django.jQuery);
});