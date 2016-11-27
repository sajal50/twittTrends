var map;
var markers = []
var locations = [];
var currentRequest;
var index=0;
var timerLoop;


function parseResponse (resp) {
  var loc = []

  for (var i = 0 ;  i < resp.length ; i++) {
        loc.push( resp[i].coordinates.toString() );
  };

  return loc;
}

function parseResponseForSentiment (resp) {
  var sentiment = {}

  for (var i = 0 ;  i < resp.length ; i++) {
    sentiment[resp[i].coordinates.toString()] = resp[i].sentiment 
  };

  return sentiment;


}
$(document).ready(function (){

  $('.key-words').change(function() {

    newChangeOfMap(null);


  });
  
});


function newChangeOfMap (object) {

    console.log(object);
    var keyword = $('.key-words option:selected').val();


    var url  = "search/"+keyword;
    
    clearTheMap();

    if (currentRequest) {

      currentRequest.abort();

    }


    clearInterval (timerLoop);


    timerLoop = setInterval (function () {

    currentRequest =  $.ajax({

      url : url,
      success: function (resp) {


        resploc = parseResponse (resp);
        hashOfSentiment = parseResponseForSentiment(resp);
        var difference = differenceBetweenTwoArrays (locations, resploc);
        locations =  locations.concat(difference);

        plotNewLocationsOnMap(locations, hashOfSentiment);
      }

    });
    
    }, 1000);
  


}




function initializeTheMap() {
  
  var coordinates="";
  map = new google.maps.Map(document.getElementById('map'), {
    center: new google.maps.LatLng(0, 0),
    zoom: 2
  });

  

}

function plotNewLocationsOnMap ( locations, hashOfSentiment ) {

  for ( ; index < locations.length; index++) {
        var image = null;
        if (hashOfSentiment[locations[index]] == 'positive') {
          var image = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';

        } else if (hashOfSentiment[locations[index]] == 'negative') {
          var image = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
        } else if (hashOfSentiment[locations[index]] == 'neutral') {
          var image = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png';
        }
        var lat=parseFloat(locations[index].split(",")[0]);
        var lng=parseFloat(locations[index].split(",")[1]);

        var myLatLng = new google.maps.LatLng(lat,lng);
        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon : image

        });

        markers.push(marker);
  }
}

function clearTheMap () {
  locations = [];
  index=0;
  for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(null);
  }

}


function differenceBetweenTwoArrays (a2, a1) {

  var a = [], diff = [];

    for (var i = 0; i < a1.length; i++) {
        a[a1[i]] = true;
    }

    for (var i = 0; i < a2.length; i++) {
        if (a[a2[i]]) {
            delete a[a2[i]];
        } else {
            a[a2[i]] = true;
        }
    }

    for (var k in a) {
        diff.push(k);
    }

    return diff;

}

