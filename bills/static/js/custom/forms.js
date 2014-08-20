/**
 * Created by roxnairani on 8/18/14.
 */

$(document).ready(function() {

    var prepareFormBlock = function () {
        $('#dashboard-block').hide();
        $('#chart-block').hide();
        $('#form-block').show();
    };

    // FORM BLOCK

    $.ajax({
        url: "/profile/",
        type: "GET",
        dataType: "html",
        success: function (profile_template) {
            $(document).on('click', '#profile', function () {
                $('#page-header').html('Profile');
                prepareFormBlock();
                $('#form-block').html(profile_template);
            });
        },
        error: function (error_message) {
            console.log(error_message);
        }
    });

    $(document).on('click', '#upload_data', function () {
        prepareFormBlock();
        $.ajax({
            url: "/upload_data/",
            type: "GET",
            dataType: "html",
            success: function (upload_data_template) {
                $('#page-header').html('Upload Data');
                $('#form-block').html(upload_data_template);
            },
            error: function (error_message) {
                console.log(error_message);
            }
        });
    });

});