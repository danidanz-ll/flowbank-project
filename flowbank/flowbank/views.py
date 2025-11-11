#from django.http import HttpResponse
from django.shortcuts import render
def homepage(request):
    return render(request, 'home.html')
    #return HttpResponse("Welcome to the FlowBank Homepage!")

def about_page(request):
    return render(request, 'about.html')
    #return HttpResponse("About FlowBank: We are committed to providing excellent banking services.")