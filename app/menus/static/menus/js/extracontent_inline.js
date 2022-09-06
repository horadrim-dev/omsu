// window.addEventListener("load", function() {
$(document).ready(function(){
    (function($) {
        $(function() {
            var modelname = 'extracontent',
                suffix = '_set',
                field_prefix = 'field-'
                trigger_field_name = 'content_type'
                inline_group = $('#'+modelname+suffix+'-group');

            function process_the_fieldsets(){

                function show_fields_by_value(target, value) {
                    target.find('.form-row').hide();
                    target.find('.' + field_prefix + 'order').show();
                    target.find('.' + field_prefix + 'position').show();
                    target.find('.' + field_prefix + 'show_title').show();
                    // target.find('.tied_to_menu').show();
                    target.find('.' + field_prefix +  trigger_field_name).show();
                    if(value){
                        console.log(value);
                        // alert(fieldset.attr('class'));
                        target.find('[class*='+ value+']').show();
                    }
                }
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    var fieldset = $(this).find('fieldset'),
                        // num = $(this).attr('id').substring(modelname.length + suffix.length),
                        trigger_field = fieldset.find('select[id^=id_'+modelname+suffix+'][id$='+ trigger_field_name +']');
                    // alert(trigger_field.attr('id'));
                    show_fields_by_value(fieldset, trigger_field.val());

                    trigger_field.change(function(){
                        // alert(fieldset.attr('class'));
                        show_fields_by_value(fieldset, $(this).val());
                    });
                });
            }

            process_the_fieldsets();

            inline_group.find('div.add-row a').click(function(){
                inline_group.find('[id^='+modelname+suffix+']').each(function(){
                    process_the_fieldsets();
                });
            });

        });

    })(django.jQuery);
});