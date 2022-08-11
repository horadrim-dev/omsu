// window.addEventListener("load", function() {
$(document).ready(function(){
    (function($) {
        $(function() {
            var modelname = 'extracontent',
                suffix = '_set',
                trigger_field_name = 'content_type'
                inline_group = $('#'+modelname+suffix+'-group');

            function process_the_fieldsets(){

                function show_fields_by_value(target, value) {
                    target.find('.form-row').hide();
                    target.find('.order').show();
                    // target.find('.tied_to_menu').show();
                    target.find('.position').show();
                    target.find('.show_title').show();
                    target.find('.'+trigger_field_name).show();
                    if(value){
                        target.find('div[class*=form-row][class*='+ value+']').show();
                    }
                }
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    var fieldset = $(this).find('fieldset'),
                        // num = $(this).attr('id').substring(modelname.length + suffix.length),
                        trigger_field = fieldset.find('select[id^=id_'+modelname+suffix+'][id$='+ trigger_field_name +']');
                    // alert(trigger_field.attr('id'));
                    show_fields_by_value(fieldset, trigger_field.val());

                    trigger_field.change(function(){
                        show_fields_by_value(fieldset, $(this).val());
                    });
                });
            }

            process_the_fieldsets();

            inline_group.find('a.grp-add-handler').click(function(){
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    process_the_fieldsets();
                });
            });

        });

    })(django.jQuery);
});