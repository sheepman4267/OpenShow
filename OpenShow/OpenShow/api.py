from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/slides/", "slides.api.router")