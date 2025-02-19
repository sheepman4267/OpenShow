# AOML Markup
OpenShow contains a custom markup language for serializing slide decks in a human-readable/writable text format. The primary goal of AOML is to be extremely fast to write (once you learn how it works).

This streamlined and predictable format makes creating new slide decks for song lyrics or readings very easy, especially when combined with an advanced text editor such as [Kate](https://kate-editor.org/) which supports placing a cursor in multiple places at once.

Workflow tip: Write or paste the entire text for a deck into a file, then use multiple cursors to simultaneously type slide element definitions for every slide all at once.
## Anatomy of an AOML File
AOML files have a very simple structure. Currently, the spec only stores information about slides (not deck metadata such as theme, transition, etc.).

Each slide element begins with a `>>` double-right chevron, with the four possible element attributes being separated by a `||` double-pipe. By convention, each double-pipe is followed by a newline. Possible attributes are:
- CSS Class (required)
- Image
- Media Object
- Body (Required)

Taking formatting convention into account, a single text-only slide in an AOML file looks like this:
```
>>lyrics||
Lyrics to a song go here.
>>subtitle||
Here is a subtitle to be projected on a slide.
```

Slides are separated by a `~~` double-tilde, which by convention is typically on its own line. Multiple slides together in an AOML file look like this:
```
>>lyrics||
Lyrics to a song go here.
>>subtitle||
Here is a subtitle to be projected on a slide.
~~
>>fit-image-height||
image:933ab3936b18eb2372306f2e039966c6aa5c7571652aca4658ed34327e8ead4d||
None
```
That AOML will produce two slides when parsed. Slide one will be text only, while slide two will contain an image referenced by the provided hash. If that image exists in the database, it will be added to the slide. Otherwise, that element will show a "missing image" error in the editor, and can be updated. Media objects can be referenced the same way, using `media:hash` rather than `image:hash`.