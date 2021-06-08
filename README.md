# Travel log

## Motivation

During my bike tours, hikes and car road trips, I always take pictures, record my tracks and sometimes write a journal
or keep track of my expenses and other stats. So far I have no proper way of visualizing all 3 data points (images,
locations and text) naturally, either for my own sake or for sharing it with friends or family members that might be
interested in a particular trip because they will do a similar journey in the future.

**This project aims to generate a website based on the assets (pictures, track and journal) from a single trip, with
minimal configuration**. Currently, it's in a very alpha stage while I validate some of the ideas.

For the proof-of-concept, the input format will be according to how I already store my assets: one folder per day, with
pictures from that day and the GPX route. To make it simpler, I will be copying my journal from whatever system I used
to store it and put it in a Markdown file in that folder. On a more practical example, consider that after a trip, I
have the following folder tree:

```
2021-05-01/
    |- car_route.gpx
    |- image1.jpeg
    |- image2.jpeg
    |- day.yaml
    |_ journal.md
2021-05-02/
    |- car_route.gpx
    |- image3.jpeg
    |- image4.jpeg
    |- day.yaml
    |_ journal.md
```

That should be the input, and the output should be a beautiful website.

![Website preview](https://s6.gifyu.com/images/preview.gif)

Sample website: https://travel-log-sample-trip.netlify.app/

> As you can see, this is not a beautiful website yet 😅. I've focused on the backend
> so far and built the most simple frontend possible to validate the backend.
> I'm currently looking for frontend/UX volunteers.
> Continue reading if you are interested.

## Vocabulary

The name of the project is Travel Log. It generates a website for each individual trip.

A **trip** (class `Trip`) can have a short title (eg: Summer vacation 2020) and a longer summary, described in
the `trip.yaml` file on the input folder root level.

A trip has one or more **trip days** (class `TripDay`). A trip day can contain pictures, tracks, and a journal. All the
image files in the folder will be parsed as pictures, and all the `.gpx` files as tracks. The journal is written as
a `day.yaml`.

A trip can contain zero or more **highlights** (class `Highlight`), which have a `name` and optionally a `summary` and
a `picture`. Note that highlights can conveniently be defined on `day.yaml` inside a date folder, but in the code they
actually belong to a trip, so multiple days highlights can be easily supported. Example of highlights: a waterfall, a
hike, a special road, a special event.

A trip can contain zero or more **privacy zones** (class `PrivacyZone`), which have a `name`, `lat`, `lng`, and
`radius` (in km). This feature is inspired by
a [Strava](https://support.strava.com/hc/en-us/articles/115000173384-Privacy-Zones)
feature with the same name. The purpose is to hide the location of specific places (eg: the house of a friend). Pictures
that have EXIF geolocation embedded and lies within a privacy zone will have its EXIF geolocation removed when processed
to be included in the website. Routes that have any points within a privacy zone will have those points removed.

On a more concrete example, the following privacy zone (taken from our `test/_sample_project`):

```yaml
privacy_zones:
  - name: Ristafallet waterfall
    lat: 63.3123834
    lng: 13.3511221
    radius: 0.5
```

will modify tracks and remove pictures from the map as seen below:
![Privacy zone example](https://github.com/fernandobrito/travel_log/blob/main/docs/privacy_zone_example.png?raw=true)

## Website generation

I'm more of a backend developer, so for now the frontend has only the minimal features necessary to validate my backend
and some of my ideas. Currently, it is done using Jinja2 + simple HTML pages.

One area for improvement would be to make the backend output `json` files and have the frontend be a modern and
independent frontend app (using React?).

## Installation

For now, only instructions to install for development. This project requires Python 3.9+ (mainly due to new type hinting
syntax).

Once you clone the repository, install the dependencies:
`$ pipenv install --dev`

Then install the Python module locally, in editable mode:
`$ pip insatll -e .`

## Commands

* `make test` to run the test suite;
* `make lint` to run the linters;
* `make build` to generate the website (to output/website);
* `make build-watch` to call the above upon any file change under `src/` (only MacOS for now);
* `make serve` to serve the website locally using Python's `http.server` module (for development purposes only);
* `make deploy-netlify-draft` to deploy the output on `output/website` on Netlify (draft);
* `make deploy-netlify-prod` to deploy the same as above but on production

> Idea: also enable/implement live-reload.

## Reference

(schema for YAMLs)

## Development

### Contributors

* Fernando Brito: author of the project. Focused on the back-end and on ideas.

I'm looking for contributors, specially UX designers and frontend developers. Please reach out if you are interested!

### Development principles

* Convention over configuration;
* Make almost every feature optional (journal, expenses tracking, etc);
* Cache as much as possible (image resizing, weather API requests, etc) so the development feedback/cycle remains
  smooth;
* [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) (but not strictly enforced)

## Testing

The sample project under `test/_sample_project` uses pictures from https://picsum.photos/ (generated
using https://picsum.photos/1024/576). The tracks are real tracks from one of my trips.

Fake EXIF coordinates were added to the images using https://www.geoimgr.com/.