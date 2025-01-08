import re
from django.shortcuts import render
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def clean_text(text):
    text = text[2:-
                2] if text.startswith("['") and text.endswith("']") else text
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace('\n\n* ', '\n\n<li>')
    text = text.replace('\n* ', '\n<li>')
    paragraphs = text.split('\n\n')
    formatted_text = []

    for p in paragraphs:
        if p.strip().startswith('<li>'):
            # It's a list - wrap in ul tags
            items = p.split('\n')
            formatted_text.append('<ul>\n{}\n</ul>'.format("\n".join(items)))
        else:
            # It's a paragraph
            formatted_text.append(f'<p>{p.strip()}</p>')

    return '\n'.join(formatted_text)


def home(request):
    generated_content = []
    user_search_query = request.POST.get("user_search_query", "").strip()
    user_selected_genre = request.POST.getlist("genre")

    if user_search_query or user_selected_genre:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

# genres search
        genres_search = " ,".join(user_selected_genre)

        # combining with user search params
        query = f'''some songs from :{
            genres_search} .user_query:{user_search_query}'''

        response = model.generate_content(query)
        formatted_content = clean_text(str(response.text))
        generated_content.append(formatted_content)

    context = {"result": generated_content}
    return render(request, 'base/home.html', context)


def test(request):
    context = {}
    return render(request, 'base/test.html', context)
