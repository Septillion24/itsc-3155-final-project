function initMap(latitude, longitude) {
    var myLatLng = { lat: parseFloat(latitude), lng: parseFloat(longitude) };
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 15
    });
    var marker = new google.maps.Marker({
        map: map,
        position: myLatLng,
        title: 'Location'
    });
}

function initializeMap() {
    var mapElement = document.getElementById('map');
    var lat = parseFloat(mapElement.getAttribute('data-lat'));
    var lng = parseFloat(mapElement.getAttribute('data-lng'));
    initMap(lat, lng);
}

google.maps.event.addDomListener(window, 'load', initializeMap);
