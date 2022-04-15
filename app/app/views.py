from django.shortcuts import render

def main(request, *args, **kwargs):
    return render(request, 'app/base.html', {})

def activity(request, slug = None):
    context = {}
    # if slug :
    context['slug'] = slug
    return render(request, 'app/base_activity.html', context)