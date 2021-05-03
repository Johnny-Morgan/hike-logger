// JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();


// Add the class table-sm to the hikes table for screens less than 500px
$(window).on('resize', function () {
    if ($(window).width() < 500) {
        $('.table').addClass('table-sm');
    } else {
        $('.table').removeClass('table-sm');
    }
});


// Datepicker
let today = new Date();
let dd = String(today.getDate()).padStart(2, '0');
let mm = String(today.getMonth() + 1).padStart(2, '0');
let yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;
$('#picker').datetimepicker({
    timepicker: false,
    datepicker: true,
    format: 'd-M-Y',
    value: today,
});

// Datepicker for editing a hike
// the value variable is removed as this value is take from the database
$('#edit-date-picker').datetimepicker({
    timepicker: false,
    datepicker: true,
    format: 'd-M-Y',
});


// Hikes table
$(document).ready(function () {
    $('#hikesTable').DataTable();
});