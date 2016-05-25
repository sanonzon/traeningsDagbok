$(document).ready(function () {
    $('.fast-workout-sections').hide();

    $('#selectFastWorkout').change(function () {
        $('.fast-workout-sections').hide();
        $('#'+$(this).val()).show();
    });
});

document.getElementById('toggleButton').onclick = function() {
    document.getElementsByClassName('menu')[0].classList.toggle('responsive');
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$('#register-form').on('submit', function(e) {
    var csrftoken = getCookie('csrftoken');
    var formData = $('#register-form').serialize();
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        //~ dataType: "json",
        data: {
            formData,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function(serverResponse) {
            console.log(serverResponse)
            console.log("OKLART SOM FAN, success ka det vara.");
        },
        error: function(XMLHttpRequest) {
            console.log("FAIL");
            $('#registerModal').modal('show');
        },
    });
    //~ return false;

});


$("#contactbutton").click(function() {
    var formData = $("#contactform").serialize();
    $.ajax({
        type: "POST",
        url: "contact.php",
        data: formData,
        success: function(serverResponse) {
            $("#message-sent").text(serverResponse);
            $("#message-sent").show(500).delay(5000).hide(500);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("some error: " + textStatus + ", " + errorThrown);
        }
    });
});



$('#login-form').on('submit', function(e) {
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        dataType: "json",
        data: {
                'csrfmiddlewaretoken': csrftoken,
        },
        success: function() {
                console.log("OKLART SOM FAN, success ka det vara.");
        },
        error: function() {
                console.log("FAIL");
                $('#loginModal').modal('show');
        },
    });
    //~ return false;

});

//~ http://stackoverflow.com/questions/19468088/handling-django-model-form-error-in-ajax-submit
