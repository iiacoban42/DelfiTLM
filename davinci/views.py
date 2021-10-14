"""API request handling. Map requests to the corresponding HTMLs."""
from django.shortcuts import render

def home(request):
    """render index.html page"""
    ren = render(request, "davinci/home/index.html")
    return ren
