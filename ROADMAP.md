# Concepts

## Slide
It's a slide, like in PowerPoint, but cooler.

## Display
A location where the slide deck can be seen. In OpenShow, this will be an HTTP endpoint like openshow/displays/projector1. Load this using some browser in kiosk mode, display that to a projector.

## Segment
A small group of slides, which can be reused in multiple decks

## Deck
The set of slides to be displayed in a presentation. You can add single slides to a deck, or you can add Segments, which allows for reusing common slides (such as an intro sequence).

# Version Targets

## v0.1.0
- Slide Editor
- Segment Editor
- Deck Editor
- Display Editor
- User-definable slide templates

## v0.2.0
- Audio file playback
- Display element on only one display

## Future
- Video capture input
- Audio capture input
- Video file playback
- WYSIWYG slide layout editor
- Headless auto-advancing slides (for digital signage)
- Constant background for Displays
