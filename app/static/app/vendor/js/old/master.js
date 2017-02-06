function myFunction() {
    document.getElementById("myTextarea").placeholder = "Your Message";
}

function remo() {
        $('#rem').fadeOut();
    }
var messageDelay = 2000;  // How long to display status messages (in milliseconds)

// Init the form once the document is ready
$(init);
$(initialize);
$(initialize1);
// Initialize the form
function init() {
    // Hide the form initially.
    // Make submitForm() the form's submit handler.
    // Position the form so it sits in the centre of the browser window.
    $('#contactForm').hide().addClass('positioned');


    // When the "Send us an email" link is clicked:
    // 1. Fade the content out
    // 2. Display the form
    // 3. Move focus to the first field
    // 4. Prevent the link being followed

    $('a[href="#contactForm"]').click(function () {
        $('#contactForm1').hide();
        $('#contactForm').fadeIn('slow', function () {
            $('#senderName').focus();
        })

        return false;
    });


    // When the "Cancel" button is clicked, close the form
    $('#cancel').click(function () {
        $('#contactForm').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
    $('#cancel3').click(function () {
        $('#mod').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
    $('#cancel4').click(function () {
        $('#mod11').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
    // When the "Escape" key is pressed, close the form
    //$('#contactForm').keydown(function (event) {
    //    if (event.which == 27) {
    //        $('#contactForm').fadeOut();
    //        $('#content').fadeTo('slow', 1);
    //    }
    //});
}
function initialize() {

    // Hide the form initially.
    // Make submitForm() the form's submit handler.
    // Position the form so it sits in the centre of the browser window.
    //$('#contactForm1').hide().addClass('positioned');

    // When the "Send us an email" link is clicked:
    // 1. Fade the content out
    // 2. Display the form
    // 3. Move focus to the first field
    // 4. Prevent the link being followed

    //$('a[href="#contactForm1"]').click(function () {
    //    $('#contactForm').hide();
    //    $('#contactForm1').fadeIn('slow', function () {
    //        $('#sendername').focus();
    //    })
    //    return true;
    //});

    // When the "Cancel" button is clicked, close the form



    // When the "Cancel" button is clicked, close the form

    $('#cancel1').click(function () {
        $('#contactForm1').fadeOut();
        $('#content').fadeTo('slow', 1);
    });

    $('#cancel').click(function () {
        $('#contactForm').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
    // When the "Escape" key is pressed, close the form


    $('#contactForm1').keydown(function (event) {
        if (event.which == 27) {
            $('#contactForm1').fadeOut();
            $('#content').fadeTo('slow', 1);
        }
    });
}
function initialize1() {
    // Hide the form initially.
    // Make submitForm() the form's submit handler.
    // Position the form so it sits in the centre of the browser window.
    //$('#contactForm2').hide().addClass('positioned');

    // When the "Send us an email" link is clicked:
    // 1. Fade the content out
    // 2. Display the form
    // 3. Move focus to the first field
    // 4. Prevent the link being followed

    $('a[href="#contactForm2"]').click(function () {
        $('#contactForm').hide();
        $('#contactForm1').hide();
        $('#contactForm2').fadeIn('slow', function () {
            $('#sendername').focus();
        })
        return true;
    });


    // When the "Cancel" button is clicked, close the form

    $('#cancel1').click(function () {
        $('#contactForm1').fadeOut();
        $('#content').fadeTo('slow', 1);
    });

    $('#cancel').click(function () {
        $('#contactForm').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
    // When the "Escape" key is pressed, close the form


    $('#contactForm1').keydown(function (event) {
        if (event.which == 27) {
            $('#contactForm1').fadeOut();
            $('#content').fadeTo('slow', 1);
        }
    });
}
function sign() {
    window.bPopup();
}

// Submit the form via Ajax

function submitForm() {
    var contactForm = $(this);


    // Are all the fields filled in?

    if (!$('#senderEmail').val() || !$('#password11').val() || !$('#message').val()) {

        // No; display a warning message and return to the form
        $('#incompleteMessage').fadeIn().delay(messageDelay).fadeOut();
        contactForm.fadeOut().delay(messageDelay).fadeIn();

    } else {

        // Yes; submit the form to the PHP script via Ajax

        $('#sendingMessage').fadeIn();
        contactForm.fadeOut();

        $.ajax({
            url: contactForm.attr('action') + "?ajax=true",
            type: contactForm.attr('method'),
            data: contactForm.serialize(),
            success: submitFinished
        });
    }

    // Prevent the default form submission occurring
    return false;
}
function submitform() {
    var contactForm1 = $(this);


    // Are all the fields filled in?

    if (!$('#sendername').val() || !$('#senderPhone').val() || !$('#senderemail').val() || !$('#senderpassword').val() || !$('#senderaddress').val() || !$('#message1').val()) {

        // No; display a warning message and return to the form
        $('#incompleteMessage').fadeIn().delay(messageDelay).fadeOut();
        contactForm1.fadeOut().delay(messageDelay).fadeIn();

    } else {

        // Yes; submit the form to the PHP script via Ajax

        $('#sendingMessage1').fadeIn();
        contactForm1.fadeOut();

        $.ajax({
            url: contactForm1.attr('action') + "?ajax=true",
            type: contactForm1.attr('method'),
            data: contactForm1.serialize(),
            success: submitfinished
        });
    }

    // Prevent the default form submission occurring
    return false;
}


// Handle the Ajax response

function submitFinished(response) {
    response = $.trim(response);
    $('#sendingMessage').fadeOut();

    if (response == "success") {

        // Form submitted successfully:
        // 1. Display the success message
        // 2. Clear the form fields
        // 3. Fade the content back in

        $('#successMessage').fadeIn().delay(messageDelay).fadeOut();
        $('#senderName').val("");
        $('#password11').val("");
        $('#message').val("");

        $('#content').delay(messageDelay + 500).fadeTo('slow', 1);

    } else {

        // Form submission failed: Display the failure message,
        // then redisplay the form
        $('#failureMessage').fadeIn().delay(messageDelay).fadeOut();
        $('#contactForm').delay(messageDelay + 500).fadeIn();
    }
}


function submitfinished(response) {
    response = $.trim(response);
    $('#sendingMessage1').fadeOut();

    if (response == "success") {

        // Form submitted successfully:
        // 1. Display the success message
        // 2. Clear the form fields
        // 3. Fade the content back in

        $('#successMessage1').fadeIn().delay(messageDelay).fadeOut();
        $('#sendername').val("");
        $('#senderPhone').val("");
        $('#senderemail').val("");
        $('#senderpassword').val("");
        $('#senderaddress').val("");
        $('#message1').val("");

        $('#content').delay(messageDelay + 500).fadeTo('slow', 1);

    } else {

        // Form submission failed: Display the failure message,
        // then redisplay the form
        $('#failureMessage1').fadeIn().delay(messageDelay).fadeOut();
        $('#contactForm1').delay(messageDelay + 500).fadeIn();
    }
}

function getpopup(a) {
    // map.closePopup();
    $('.b-iframe').attr("src", a);
    popupframe = $('#element_to_pop_up').bPopup({
        modalClose: false,
        content: 'iframe',
        opacity: 0.5,
        positionStyle: 'fixed'

    });
}

function callme1() {
    document.getElementById('<%=Text1.ClientID%>').value = document.getElementById('<%=photofileup.ClientID %>').value;

}

function callme2() {
    document.getElementById('<%=idproof.ClientID%>').value = document.getElementById('<%=idfileup.ClientID %>').value;

}

function callme3() {
    document.getElementById('<%=addrproof.ClientID%>').value = document.getElementById('<%=addfileup.ClientID %>').value;

}
function hidepopup() {
    $("#forgettonform").css({ "visibility": "hidden", "display": "none" });
}