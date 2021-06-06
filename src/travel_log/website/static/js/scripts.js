const loadMap = id => {
    const map = L.map(id)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)

    return map
}

const addPicturesToMap = (pictures, map) => {
    let formattedPictures = []

    let photoLayer = L.photo.cluster({
        spiderfyDistanceMultiplier: 1.2,
        icon: { iconSize: [60, 60] },
    }).on('click', evt => {
        // Pop-up, from Leaflet.Photo example
        // evt.layer.bindPopup(L.Util.template('<img src="{url}"/></a><p>{caption} {lat} {lng}</p>', evt.layer.photo), {
        //     className: 'leaflet-popup-photo',
        //     minWidth: 500,
        // }).openPopup()

        // Our own integration with lightbox
        evt.layer.photo.openOnLightbox()
    })

    pictures.forEach(picture => {
        let longitude = parseFloat(picture.getAttribute('data-longitude'))
        let latitude = parseFloat(picture.getAttribute('data-latitude'))
        // let marker = L.marker({ lng: longitude, lat: latitude }).addTo(map)

        if (!(longitude && latitude)) return

        formattedPictures.push({
            lng: longitude,
            lat: latitude,
            caption: 'Photo',
            thumbnail: picture.getAttribute('src'),
            openOnLightbox: () => picture.click(),
        })
    })

    photoLayer.add(formattedPictures).addTo(map)
}

const fitBoundsMultipleTracks = (tracksLoaded, map) => {
    let bounds = L.latLngBounds(tracksLoaded[0].getBounds())

    tracksLoaded.forEach(trackLoaded => {
        bounds.extend(trackLoaded.getBounds())
    })

    map.fitBounds(bounds)
}

const addTracksToMapTripDay = (tracks, map) => {
    /*
     Tracks are added asynchronously to the map, which makes calling "fitBounds" a bit trickier.
     */
    let tracksLoadedOnMap = []

    tracks.forEach(track => {
        let gpx = track.getAttribute('data-gpx-url') // URL to your GPX file or the GPX itself

        new L.GPX(gpx, {
            async: true,
            marker_options: {
                startIconUrl: 'images/pin-icon-start.png',
                endIconUrl: 'images/pin-icon-end.png',
                shadowUrl: 'images/pin-shadow.png',
            },
        }).on('loaded', function (e) {
            tracksLoadedOnMap.push(e.target)

            if (tracks.length === tracksLoadedOnMap.length) {
                fitBoundsMultipleTracks(tracksLoadedOnMap, map)
            }
        }).addTo(map)
    })
}

const addTracksToMapTrip = (tracks, map) => {
    let tracksLoadedOnMap = []

    tracks.forEach(track => {
        let gpx = track.getAttribute('data-gpx-url') // URL to your GPX file or the GPX itself

        new L.GPX(gpx, {
            async: true,
            marker_options: {
                startIconUrl: undefined,
                endIconUrl: undefined,
                shadowUrl: undefined,
            },
        }).on('loaded', function (e) {
            tracksLoadedOnMap.push(e.target)

            if (tracks.length === tracksLoadedOnMap.length) {
                fitBoundsMultipleTracks(tracksLoadedOnMap, map)
            }

            // e.target.bindTooltip(track.getAttribute('data-trip-date'), {
            //     permanent: true,
            // }).openTooltip()
            e.target.bindTooltip(track.getAttribute('data-trip-date'))
        }).addTo(map)
    })
}

// The map for the entire trip. All routes should be added to this one
let allTracks = document.querySelectorAll('.track')
const mapTrip = loadMap('map_trip')
addTracksToMapTrip(allTracks, mapTrip)


// Maps for each individual TripDay
let maps = document.querySelectorAll('.map-trip-day')

maps.forEach(element => {
    let mapTripDay = loadMap(element.id)

    // Make the popup (used in the pictures) pop up in the center of the map canvas
    // From: https://stackoverflow.com/questions/22538473/leaflet-center-popup-and-marker-to-the-map
    mapTripDay.on('popupopen', function (e) {
        var px = mapTripDay.project(e.target._popup._latlng) // find the pixel location on the map where the popup anchor is
        px.y -= e.target._popup._container.clientHeight / 2 // find the height of the popup container, divide by 2, subtract from the Y axis of marker location
        mapTripDay.panTo(mapTripDay.unproject(px), { animate: true }) // pan to new center
    })

    let tripDate = element.getAttribute('data-trip-date')

    let tracks = document.querySelectorAll((`.track[data-trip-date*="${tripDate}"]`))
    addTracksToMapTripDay(tracks, mapTripDay)

    let pictures = document.querySelectorAll((`.picture[data-trip-date*="${tripDate}"]`))
    addPicturesToMap(pictures, mapTripDay)
})