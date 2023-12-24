[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
# OpenShow
A flexible, extensible, open-source presentation system. OpenShow is written in Python, using mostly Django and friends.

## Why?
OpenShow is in development right now for use in worship services and other events at a Unitarian Universalist Church. We've tried paid software packages which claim to work, but never found one that was fully-featured and stable enough. OpenShow tries to use advanced code others have written already, as is the custom in Django-land.

## Concepts
These are the core concepts used to make OpenShow work.

### Show
A collection of segments (at a concert, you might have a segment for each song being played, for example). A show is assigned a theme, which will be used to style slides being presented.

### Segment
A segment can have its own set of slides, or include a deck.

### Deck
A reusable collection of slides, such as the lyrics to a song. Decks are assigned their own theme.

### Slide
A slide. Right now, they're thinly veiled HTML.

### Slide Element
A text box, image, or audio/video clip to be played. These are styled with CSS from the selected theme, and make up the actual content of a Slide.

### Theme
Themes are written in CSS. TODO: Add a list of standard CSS class names which themes should implement to be compatible with most shows.

### Transition
Transitions are CSS animations. The editor allows you to specify your keyframes in a relatively intuitive way.

### Display
Displays are where slides get shown. This is a separate page to be opened in another broswer window, or used (for example) in an OBS Browser Source.

## Quickstart
As of release v0.1.0, OpenShow now has an official Docker container. The container does not serve static files or media. Those will have to be on bind mounts or volumes, so they can be served by some other webserver. In my deployment, I use the official `nginx` container for this. Both that and the dynamic application are behind a Traefik reverse proxy. `docker-compose.yml.example` contains a very simplified version of my deployment.

This is just my method, and nothing about OpenShow requires that you use Traefik or NGINX. It's the way I'm familiar with, though, and it works well for me.

A quickstart guide for actually using OpenShow will be written soon. However, for now:
The one thing you won't be able to find by poking around the UI is the URL to actually see a display. That is `/slides/displays/<pk>`, so the first display you add will be `localhost:8000/slides/displays/1`.

## Development Setup

This is a standard Django + Channels application, and a development copy can be set up (on Linux) by:

1. Clone this repository
2. Create a python virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install requirements as usual: `pip install -r requirements.txt`
5. Run the server: `python manage.py runserver`

Once you have this running, you can navigate to localhost:8000 in your web browser and start messing with OpenShow. 
