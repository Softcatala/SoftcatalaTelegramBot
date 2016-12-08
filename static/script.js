$(function () {
    var base64 = decodeURIComponent(window.location.hash.split('#')[1]);
    var event = JSON.parse(Base64.decode(base64));

    fillCard(event);
    addButtons(event);
});

function fillCard(event) {
    $('#title').html(event.name);
    $('#description').html(event.description);

    // Create place link
    if (event.place) {
    var place = $('#place');
    place.html('<img draggable="false" class="emoji" alt="󾔿" src="http://twemoji.maxcdn.com/16x16/1f4cd.png"> ' + event.place + '<br>');
    place.click(function () {
        window.open('http://www.openstreetmap.org/search?query=' + event.place);
    });
    };

    // Create event URL link
    if (event.eventurl) {
    var route = $('#eventurl');
    route.html('<img draggable="false" class="emoji" alt="ℹ" src="http://twemoji.maxcdn.com/16x16/2139.png"> Més informació');
    eventurl.click(function () {
        window.open(event.eventurl);
    });

    // Create event URL iframe
    var iframe = '<center><iframe scrolling="yes" height="400" frameborder="0" width="100%" src="' + event.eventurl +'"></iframe></center><br><br>'; 
    document.getElementById('iframe').innerHTML=iframe;
    };

    // Format and show date
    var date = new Date(parseInt(event.date) * 1000);

    var options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long',
        hour: 'numeric',
        minute: 'numeric'
    };

    var formattedDate = date.toLocaleDateString('ca-ES', options);

    $('#date').html(formattedDate);

    // Preload and set image
    var image = getImage(event);
    var imageUrl = 'images/img_' + image + '.jpg';

    $('<img/>').attr('src', imageUrl).load(function () {
        $(this).remove();
        $('.picture').css('background-image', 'url(' + imageUrl + ')');
        showCard();
    });
}

function addButtons(event) {
    var data = {
        title: event.name,
        start: new Date(parseInt(event.date) * 1000),
        duration: 60
    };

    if (event.place) {
        data.address = event.place;
    }

    if (event.description) {
        data.description = event.description;
    }

    var calendar = createCalendar({
        data: data
    });
    $('.add').append(calendar);
}

function showCard() {
    $('.page').fadeIn(200);
}
