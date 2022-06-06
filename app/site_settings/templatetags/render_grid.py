from django import template
from site_settings.models import Section
register = template.Library()

@register.inclusion_tag('site_settings/grid.html')
def render_grid():
    context = {}

    # TODO сделать проверку на пустоту (не берем секции где в блоках нет контента)
    context['sections'] = Section.objects.all()

    return context
