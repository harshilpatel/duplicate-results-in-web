function validate1() {
    var Email = document.getElementById('<%=txtemail.ClientID %>').value;

    var Password = document.getElementById('<%=txtpass.ClientID %>').value;



    if (Email == "") {
        alert("Enter Email");
        return false;
    }

    if (Password == "") {
        alert("Enter password");
        return false;
    }

}


var messageDelay = 2000;  // How long to display status messages (in milliseconds)

// Init the form once the document is ready
$(init);
$(initialize);


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
        $("#notlogin").hide();
        $('#contactForm').show();
        $('#contactForm').fadeIn('slow', function () {
            $('#senderName').focus();
        });
    });


    // When the "Cancel" button is clicked, close the form
    $('#cancel34').click(function () {
        $('#contactForm').fadeOut();
        $('#content').fadeTo('slow', 1);
    });
}


function initialize() {

    // Hide the form initially.
    // Make submitForm() the form's submit handler.
    // Position the form so it sits in the centre of the browser window.


    $('#contactForm1').hide().addClass('positioned');

    // When the "Send us an email" link is clicked:
    // 1. Fade the content out
    // 2. Display the form
    // 3. Move focus to the first field
    // 4. Prevent the link being followed


    $('a[href="#contactForm1"]').click(function () {
        $('#contactForm').hide();
        $("#notlogin").hide();
        $('#contactForm1').fadeIn('slow', function () {
            $('#sendername').focus();
        });

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



function addqnt(val) {
    var int1 = parseInt($(val).next().val()) - 1;

    var data = [];
    // data = $.parseJSON(readCookie('Productcookie'));
    // console.log($(val).next()[0].innerHTML);
    $.each($.parseJSON(readCookie('Productcookie')), function (i) {
        var values = {};
        values["fromdatetime"] = this.fromdatetime;
        values["todatetime"] = this.todatetime;
        values["amount"] = this.amount;
        values["option"] = this.option;
        values["charges"] = this.charges;
        values["total"] = this.total;
        values["qnty"] = this.qnty;
        values["prodname"] = this.prodname;
        values["image"] = this.image;
        values["subtotal"] = this.subtotal;
        values["total1"] = this.total1;
        values["days"] = this.days;
        values["cost"] = this.cost;
        values["id"] = this.id;
        values["address"] = this.address;
        if (this.id == $(val).next().next().next()[0].innerHTML) {
            values["qnty"] = int1;
        }
        else {
            values["qnty"] = this.qnty;
        }
        data.push(values);

    });
    document.cookie = 'Productcookie=' + JSON.stringify(data);

    var amt1 = parseInt($(val).parent().closest("td").prev().children(".spancls").html());
    var amt3 = parseInt($("#lblcharge").html());
    $(val).parent().closest("td").next().children(".spancls2").html(int1 * amt1);
    var tempamt = 0.0;
    $(".spancls2").each(function (index, value) {
        tempamt += parseFloat($(value)[0].innerHTML.trim());
    });
    $(".spancls23").each(function (index, value) {
        tempamt += parseFloat($(value)[0].innerHTML.trim());
    });


    $("#spncls3").html(tempamt);
    $("#spncls5").html(tempamt + amt3);
    var amt41 = parseInt($("#spncls5").html());
    $("#spncls6").html(amt41);
    loadcart();
    //$("#spnadd").html(int1);
    // $("#spnadd1").html(amt1);
    //  $("#spancls23").html(int1 * amt1);
    //  $("#spncls67").html(tempamt + amt3);

}
function addqnt123(val) {
    var int = parseInt($(val).prev().val()) + 1;
    var data = [];
    // data = $.parseJSON(readCookie('Productcookie'));
    // console.log($(val).next()[0].innerHTML);
    $.each($.parseJSON(readCookie('Productcookie')), function (i) {
        var values = {};
        values["fromdatetime"] = this.fromdatetime;
        values["todatetime"] = this.todatetime;
        values["amount"] = this.amount;
        values["option"] = this.option;
        values["charges"] = this.charges;
        values["total"] = this.total;
        values["qnty"] = this.qnty;
        values["prodname"] = this.prodname;
        values["image"] = this.image;
        values["subtotal"] = this.subtotal;
        values["total1"] = this.total1;
        values["days"] = this.days;
        values["cost"] = this.cost;
        values["id"] = this.id;
        if (this.id == $(val).next()[0].innerHTML) {
            values["qnty"] = int;
        }
        else {
            values["qnty"] = this.qnty;
        }
        data.push(values);
    });
    document.cookie = 'Productcookie=' + JSON.stringify(data);

    var amt = parseInt($(val).parent().closest("td").prev().children(".spancls").html());
    $(val).parent().closest("td").next().children(".spancls2").html(int * amt);
    var tempamt = 0.0;
    $(".spancls2").each(function (index, value) {
        tempamt += parseFloat($(value)[0].innerHTML.trim());
    });
    $(".spancls23").each(function (index, value) {
        tempamt += parseFloat($(value)[0].innerHTML.trim());
    });

    var amt3 = parseInt($("#lblcharge").html());
    $("#spncls3").html(tempamt);
    $("#spncls5").html(tempamt + amt3);
    var amt4 = parseInt($("#spncls5").html());
    $("#spncls6").html(amt4);
    var amt5 = parseInt($("#lblcount44").html());
    // $("#spnadd").html(int);
    // $("#spnadd1").html(amt);
    //$("#spancls23").html(int * amt);
    // $("#spncls67").html(tempamt + amt3);
    loadcart();
}
function loadcart() {
    var data = $.parseJSON(readCookie('Productcookie'));
    if (data.length > 0) {
        $("#cnf").empty();
        $.each(data, function (i) {
            var ttl = parseFloat(this.amount) * parseFloat(this.qnty);
            var ttl1 = ((parseFloat(this.amount) * parseFloat(this.qnty)) + parseFloat(this.charges));
            $("#cnf").append('<li><a data-animated-link="fadeOut" href="#" class="dima-close" title="Remove this item" id="cancel"></a><a data-animated-link="fadeOut" href="#" title=""><img width="65" height="70" class="attachment-shop_thumbnail" src="' + this.image + '" alt="" />' + this.prodname + '</a><span class="price text-start"><ins><span class="amount"><label>' + this.qnty + ' x ' + this.amount + '</label></span></ins></span></li><p>Shipping Charge: Rs. ' + this.charges + '<br/>Total Amount:Rs. <span>' + ttl + '</span></p><li><p>SUBTOTAL :Rs. ' + ttl1 + '</span></p></li>');
        });
    }
}
function aj1() {
    //console.log("1");

    if ($('#drpl :selected').text() == "Add New") {

        $("#txtadd").attr("placeholder", "Enter New Delivery Address");

    }
    else if ($('#drpl :selected').text() == "Qwikgear Office") {
        $("#txtnew").val($(this).find('#drpl:selected').text());
    }
    $.ajax({
        type: "POST",
        url: "cart.aspx/getaddr",
        data: "{'data':'" + $('#drpl :selected').val() + "'}",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: OnSuccess1,
        failure: function (response) {
            // alert(response.d);
        },
        error: function (response) {
            //  alert(response.d);
        }

    });
}

function OnSuccess1(response) {
    //callme(response.d);

    $('#txtadd').val(response.d);
}

function aj2() {
    //console.log("1");
    if ($('#drpl2 :selected').text() == "Add New") {
        //$("#txtnewpic").css('visibility', 'visible');
        $("#txtpicaddr").attr("placeholder", "Enter New Pickup Address");
    }
    $.ajax({
        type: "POST",
        url: "cart.aspx/getaddr2",
        data: "{'data2':'" + $('#drpl2 :selected').val() + "'}",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: OnSuccess2,
        failure: function (response) {
            // alert(response.d);
        },
        error: function (response) {
            //  alert(response.d);
        }

    });
}

function OnSuccess2(response) {
    //callme(response.d);
    $('#txtpicaddr').val(response.d);
}


