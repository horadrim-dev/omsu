from django import template
from grid.models import Section
register = template.Library()

# @register.inclusion_tag('grid/grid.html')
# def render_grid():
#     context = {}

#     # TODO сделать проверку на пустоту (не берем секции где в блоках нет контента)
#     sections =  Section.objects.all()
#     context['sections'] = sections
#     # context['blocks'] = [s.block_set.all() for s in sections]
#     return context
