from django.shortcuts import render
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def test(request):
    context = {}
    return render(request, 'base/test.html', context)
