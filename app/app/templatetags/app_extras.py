from django import template

register = template.Library()

@register.filter(name='range')
def _range(_min, args=None):
    '''
    Python range() function for templates

    Usage:
    {% for value in 5|range %}              0 1 2 3 4
    {% for value in 5|range:10 %}           5 6 7 8 9
    {% for value in 5|range:"10,2" %}       5 7 9
    '''
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    # args = filter(None, (_min, _max, _step))
    args = filter(lambda x: isinstance(x, int) and x >= 0, (_min, _max, _step))
    return range(*args)

# your solution does not work on for value in 0|range:"10,2". 
# You have to change your code as follow: 
# args = filter(lambda x: isinstance(x, int) and x >= 0, (_min, _max, _step))