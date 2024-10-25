from django.shortcuts import render

def under_development(request):
    return render(request, 'under_development.html')