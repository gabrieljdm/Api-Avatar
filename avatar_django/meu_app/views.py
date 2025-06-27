from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
import requests
from deep_translator import GoogleTranslator 

def personagens(request):
    
    api_url = f"https://last-airbender-api.fly.dev/api/v1/characters"
    
    response = requests.get(api_url)

    personagem = response.json()

    translator = GoogleTranslator(source='auto', target='pt')

    for p in personagem:
        afiliacao = p.get("affiliation", "")
        p["affiliacao_traduzida"] = translator.translate(afiliacao) if afiliacao else ""
        
        nome = p.get("name", "")
        p["name_traduzido"] = translator.translate(nome) if nome else ""
        
        aliados = p.get("allies", [])
        p["aliados_traduzidos"] = [translator.translate(a) for a in aliados if a]
        
        inimigos = p.get("enemies", [])
        p["inimigos_traduzidos"] = [translator.translate(i) for i in inimigos if i]

    personagem.sort(key=lambda x: x["name_traduzido"])    
        
    paginator = Paginator(personagem, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", 
    {'page_obj': page_obj,
    })
    