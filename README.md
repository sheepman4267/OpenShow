[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
# OpenShow
A flexible, extensible, open-source presentation system. OpenShow is written in Python, using mostly Django and friends.

## Why?
OpenShow is in use in worship services and other events at a Unitarian Universalist Church. We've tried paid software packages which claim to work, but never found one that was fully-featured and stable enough. OpenShow tries to use advanced code others have written already, as is the custom in Django-land.

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
OpenShow offers an official docker container, which is the recommended method for deployment. The container does not serve static files or media. Those will have to be on bind mounts or volumes, so they can be served by some other webserver. In my deployment, I use the official `nginx` container for this. Both that and the dynamic application are behind a Traefik reverse proxy. `docker-compose.yml.example` contains a good starting point for a new deployment.

This is just my method, and nothing about OpenShow requires that you use Traefik or NGINX. It's the way I'm familiar with, though, and it works well for me.

### Container Setup
> [!NOTE]
> This setup guide assumes that your container host is running linux. Any distro with a functional docker-compose should work. OpenShow has not been tested running anywhere other than a Linux host. If you have a working setup on another OS, please open an issue and share notes!

1. Save `docker-compose.yml.example` as `docker-compose.yml` somewhere on your system.
2. Edit `docker-compose.yml` to your specification.
    1. Out of the box, the only thing you must change is the value of `OPENSHOW_SECRET_KEY`. Set that to a random 50 character string.
    2. Be advised that the default docker-compose file will create a directory `./openshow` relative to the directory containing your docker-compose setup and place the application state within. This includes media files, static files, and the sqlite database. 
3. Start up the containers with `docker-compose up -d`.  
4. Open a web browser and visit [localhost:8080](localhost:8080). You should see the OpenShow index, assuming everything worked correctly. OpenShow currently has no authentication at all, so there's no initial account creation necessary.

### Usage
Now that you have a working instance of OpenShow, the next step is to learn how to use it. In-depth documentation is in progress, but here's a general overview.
Refer to the "Concepts" section above for explanation of terminology such as "Show", "Segment", "Theme", etc.
#### Hello, World!
1. Click "Slides" to enter the slides module. Other modules are not essential to most installations.
2. Before you start creating slides, you'll need a theme. Create one by clicking on the "Themes" tab, followed by "New Theme". Set a name and submit it.
> [!NOTE]
> The current theme editor dates back to the initial prototype of OpenShow, and is due for a complete rewrite. This isn't the final form of this interface (thank goodness!).
3. The unlabeled text box below the preview winodw is where you put CSS rules which make up your theme. If you're not experienced with CSS, or if you just want a somewhat sane place to start, copy the contents of `example-theme.css` from this repository into that text box and click "Submit".
4. Next, you'll need a display. Click the back button on the left side of the header to return to the slides index, select the "Displays" tab, and click "New Display". Enter a name for your display and submit it.
5. Click the link to open that display in a new tab, then move that tab to a new window. Put it somewhere that you can get to it easily.
4. Click the back button to return to the slides index, then click on the "Shows" tab. Click "New Show", enter a name, and submit it.
5. Welcome to the show editor! Now, you'll want to select the theme you just created. Click on "Set Theme", select your theme in the resulting dropdown, and click "Submit".
6. Next, click "New Segment" on the left. Enter a name and click "Submit". 
7. You'll see a box in the sidebar labeled with the name of your segment. Click "New Slide" inside your segment.
8. Click on the slide. This will open your new slide for editing. 
9. Click the plus button in the lower right corner of the slide editor to add a new element.
10. Enter the CSS class which you would like to apply to your new element. This should be a class (or set of classes) which is defined in the CSS you placed in the theme in step three. Click "Submit".
11. You should see placeholder text appear in the preview area saying "Double-click to edit". Follow that direction and add some text to your slide element. Press ctrl+enter or click the checkmark to save the content.
12. Click the back button twice (once to go back to editing show properties, then again to reach the presenter view for your show). In the right sidebar, there's a gear button. Click that, select your display in the list, and click the checkmark. That sets this Show object to send slides to your display.
13. In the main body of the presenter view, you'll see a thumbnail for the slide you just created. Click on it! The slide you created should appear in the browser window where you opened your display.

Congratulations! You've just displayed your first slide using OpenShow! Hopefully that gives you an idea of the UI. Many pieces of the editor have function descriptions built in - otherwise, more documentation will be forthcoming. Feel free to file an issue if you have a question, even if it's probably not a bug.

## Development Setup

OpenShow uses [honcho](https://honcho.readthedocs.io/en/latest/) both in development and production, as we need a separate worker process for video transcoding.
In production, you should almost certainly use the docker container, but here's how you set up a development environment:

1. Clone this repository
2. Create a python virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install requirements as usual: `pip install -r requirements.txt`
> [!NOTE]
> If you want your development instance to transcode media objects, you'll need to install `ffmpeg` as well. Everything else will work without it.
5. Run the server: `honcho start -f Procfile.development`

Once you have this running, you can navigate to localhost:8030 in your web browser and start messing with OpenShow. The development server port can be changed by editing `Procfile.development` to suit your needs.
