from .models import Display, Slide

def show_slide_by_pk(slide_pk, display_pk):
    slide = Slide.objects.get(pk=slide_pk)
    display = Display.objects.get(pk=display_pk)
    slide.send_to_display([display])
    