/*
    From: https://github.com/turban/Leaflet.Photo

    Modified in this project to:
        1) Fix images that were not loading if they had spaces in the name (by wrapping the URL in
           the background-image icon style)
 */

L.Photo = L.FeatureGroup.extend({
    options: {
        icon: {
            iconSize: [40, 40],
        },
    },

    initialize: function (photos, options) {
        L.setOptions(this, options)
        L.FeatureGroup.prototype.initialize.call(this, photos)
    },

    addLayers: function (photos) {
        if (photos) {
            for (var i = 0, len = photos.length; i < len; i++) {
                this.addLayer(photos[i])
            }
        }
        return this
    },

    addLayer: function (photo) {
        L.FeatureGroup.prototype.addLayer.call(this, this.createMarker(photo))
    },

    createMarker: function (photo) {
        var marker = L.marker(photo, {
            icon: L.divIcon(L.extend({
                html: `<div style="background-image: url('${photo.thumbnail}');"></div>​`,
                className: 'leaflet-marker-photo',
            }, photo, this.options.icon)),
            title: photo.caption || '',
        })
        marker.photo = photo
        return marker
    },
})

L.photo = function (photos, options) {
    return new L.Photo(photos, options)
}

if (L.MarkerClusterGroup) {
    L.Photo.Cluster = L.MarkerClusterGroup.extend({
        options: {
            featureGroup: L.photo,
            maxClusterRadius: 100,
            showCoverageOnHover: false,
            iconCreateFunction: function (cluster) {
                return new L.DivIcon(L.extend({
                    className: 'leaflet-marker-photo',
                    html: `<div style="background-image: url('${cluster.getAllChildMarkers()[0].photo.thumbnail}');"></div>​<b>` + cluster.getChildCount() + '</b>',
                }, this.icon))
            },
            icon: {
                iconSize: [40, 40],
            },
        },

        initialize: function (options) {
            options = L.Util.setOptions(this, options)
            L.MarkerClusterGroup.prototype.initialize.call(this)
            this._photos = options.featureGroup(null, options)
        },

        add: function (photos) {
            this.addLayer(this._photos.addLayers(photos))
            return this
        },

        clear: function () {
            this._photos.clearLayers()
            this.clearLayers()
        },

    })

    L.photo.cluster = function (options) {
        return new L.Photo.Cluster(options)
    }

}