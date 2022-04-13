from django.shortcuts import render

def main(request, *args, **kwargs):
    return render(request, 'app/base.html', {})