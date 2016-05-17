$(document).ready(function () {
    $('.fast-workout-sections').hide();

    $('#selectFastWorkout').change(function () {
        $('.fast-workout-sections').hide();
        $('#'+$(this).val()).show();
    });

    $('#calendar').fullCalendar({
        
    });
});

document.getElementById('toggleButton').onclick = function() {
    document.getElementsByClassName('menu')[0].classList.toggle('responsive');
}
