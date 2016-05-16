$(document).ready(function () {
        $('.fast-workout-sections').hide();
        // $('#fastWorkoutRunning').show();
        $('#selectFastWorkout').change(function () {
            $('.fast-workout-sections').hide();
            $('#'+$(this).val()).show();
        });
    });

document.getElementById('toggleButton').onclick = function() {
    document.getElementsByClassName('menu')[0].classList.toggle('responsive');
}
