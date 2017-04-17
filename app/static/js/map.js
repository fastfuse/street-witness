
var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 49.84104, lng: 24.03164},
    zoom:12,
    styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#263c3f'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#6b9a76'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{color: '#38414e'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry.stroke',
              stylers: [{color: '#212a37'}]
            },
            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#746855'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#1f2835'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#17263c'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#515c6d'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#17263c'}]
            }
          ]  });
}





{% extends "base.html" %}

{% block index %}

  {# <div id="map">Map</div> #}

  <div class="row">
    <div class="col-xs-3">
      <h3>App</h3>

      <div class="list-group">
        <a href="#" class="list-group-item">
          <h4 class="list-group-item-heading">Title</h4>
          <p class="list-group-item-text">escription</p>
          <p class="list-group-item-text">Location</p>
          <p class="list-group-item-text">Timestamp</p>
          <span class="label label-primary">Primary</span>
      <span class="label label-success">Success</span>
      <span class="label label-warning">Warning</span>
        </a>



        <a href="#" class="list-group-item">
          <h4 class="list-group-item-heading">List group item heading</h4>
          <p class="list-group-item-text">Donec id elit non mi porta gravida at eget metus. Maecenas sed diam eget risus varius blandit.</p>
        </a>


        <a href="#" class="list-group-item">
          <div class="row">
            <div class="col-xs-6">122</div>
            <div class="col-xs-6">333</div>
          </div>
        </a>


      </div>

    </div>

    <div class="col-xs-9" id="map">Map</div>
  </div>

{% endblock index %}
