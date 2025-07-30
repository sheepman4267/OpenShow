from django.shortcuts import render
import lorem
import base64


def generate_lorem(request, css_class:str, words:int):
    return render(request, 'editor/lorem.html',
                  context={
                      'css_class': css_class,
                      'lorem': lorem.get_word(count=words)
                  })

def lazy_load_image(request, image_url):
    return render(
        request,
        'editor/lazy_load_image.html',
        context={
            'image_url': base64.b64decode(image_url).decode('utf-8'),
        }
    )
