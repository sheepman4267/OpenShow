from django.shortcuts import render
import lorem


def generate_lorem(request, css_class:str, words:int):
    return render(request, 'editor/lorem.html',
                  context={
                      'css_class': css_class,
                      'lorem': lorem.get_word(count=words)
                  })
