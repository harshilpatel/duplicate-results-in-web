function imageurl()
    {

        $("#txb2").datepicker({ beforeShowDay: noSunday, minDate: 0, dateFormat: "dd-mm-yy" });
        $("#txb1").datepicker({ beforeShowDay: noSunday, minDate: 0, dateFormat: "dd-mm-yy" });
        $('#TextBox3').timepicker({ step: 30, timeFormat: 'h:i A', 'minTime': '10:00 AM', 'maxTime': '07:00 PM' });
        $('#TextBox2').timepicker({ step: 30, timeFormat: 'h:i A', 'minTime': '10:00 AM', 'maxTime': '07:00 PM' });
    }
function noSunday(date) {
    return [date.getDay() != 0, ''];
};
function addqnt() {
    var val = parseInt($("#totq").val());
    if (val > 0) {
        $("#totq").val(val-1);
                
        var ttl = (parseFloat($("#Label2").html().trim()) * parseInt($("#totq").val()) * parseFloat($("#lblerrr").html()));
        $("#Label1").html(ttl);
    }
    if (parseInt($("#totq").val()) <= 0)
        $("#Label1").html("0");


}
function addqnt1() {
    var val = parseInt($("#totq").val());
    var max_quantity = parseInt($("#max_quantity").text());
    console.log(max_quantity);
    if (val + 1 > max_quantity) {
        alert("No More Available");
        return;
    }
    $("#totq").val(val+1);
    var ttl = (parseFloat($("#Label2").html().trim()) * parseInt($("#totq").val()) * parseFloat($("#lblerrr").html()));
    $("#Label1").html(ttl);
}
$(function () {
    $("#txb1").change(function (event) {
        calculate();
    });
    $("#txb2").change(function (event) {
        calculate();
    });
    $("#TextBox3").change(function (event) {
        calculate();
    });
    $("#TextBox2").change(function (event) {
        calculate();
    });
    $("#drpl").change(function (event) {
        var type = $("#drpl option:selected").text();
        if ($("#Label1").html() != "")
            $.ajax({
                type: "POST",
                url: "prodetail.aspx/ddlchng",
                data: '{type: "' + type + '"}',
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                async: "true",
                cache: "false",
                success: function (val) {
                    var data = JSON.parse(val.d);
                    var chgs = data[0].price;
                    if (parseInt($("#totq").val()) > 0) {
                        var ttl = parseFloat($("#Label1").html()) + parseFloat(chgs);
                        $("#Label2").html(ttl);
                    }
                    else
                        $("#Label2").html("0");
                },
                Error: function (x, e) {
                }
            });
    });
});
function calculate() {
    $("#Label3").hide();
    var fdate = $("#txb1").val();
    var ftime = $("#TextBox3").val();
    var tdate = $("#txb2").val();
    var ttime = $("#TextBox2").val();
    if (fdate == tdate) {
        $("#Label3").html('End Date Should be greater than Start Date');
        $("#Label3").show();
        return;
    }
    if (fdate == "" || ftime == "" || tdate == "" || ttime == "") {
        $("#Label3").html('Enter Date And Time');
        $("#Label3").show();
        return;
    }

    var ttl = (parseFloat($("#Label2").html().trim()) * parseInt($("#totq").val()) * parseFloat($("#lblerrr").html()));
    $("#Label1").html(ttl);

    //var days = parseFloat( $("#lblerrr").html() );
    //var quantity = parseFloat( $("#totq").val() );
    //var per_day = 1;
    //var total = 0;
    //switch( true ){
    //    case (days == 1):
    //        total = days * quantity * parseFloat($("#label6").html().trim());
    //        break;
    //    case (days > 1 && days < 5):
    //        total = days * quantity * parseFloat($("#label2_4").html().trim());
    //        break;
    //    case (days > 4 && days < 9):
    //        total = days * quantity * parseFloat($("#label5_8").html().trim());
    //        break;
    //    case (days > 8 && days < 15):
    //        total = days * quantity * parseFloat($("#label9_14").html().trim());
    //        break;
    //}
    //$("#Label1").html(total); return;

    $.ajax({
        type: "POST",
        url: "prodetail.aspx/calculate",
        data: '{fdate: "' + fdate + '",ftime:"' + ftime + '",tdate:"' + tdate + '",ttime:"' + ttime + '",id:"' + GetParameterValues('id') + '"}',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: "true",
        cache: "false",
        success: function (val) {
            var data = JSON.parse(val.d);
            $("#lblerrr").html(data[0].day);
            //$("#Label1").html(data[0].amt);

            $("#Label2").html(parseFloat(data[0].amt) / parseInt(data[0].day));
            if ($("#totq").val() > 0)
            {
                var ttl = parseFloat($("#Label1").html());
                $("#Label1").html(ttl);
            }
        },
        Error: function (x, e) {
        }
    });
}
function GetParameterValues(param) {
    var url = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < url.length; i++) {
        var urlparam = url[i].split('=');
        if (urlparam[0] == param) {
            return urlparam[1];
        }
    }
}
//function addtocart() {

//    $("#Label3").hide();
//    var fdate = $("#txb1").val();
//    var ftime = $("#TextBox3").val();
//    var tdate = $("#txb2").val();
//    var ttime = $("#TextBox2").val();

//    if (fdate == "" || ftime == "" || tdate == "" || ttime == "") {
//        $("#Label3").html('Enter Date And Time');
//        $("#Label3").show();
//        return;
//    }
//    if (parseInt($("# totq").val().trim()) <= 0)
//        return;

//    var data = [];
//    var ckidata = readCookie('Productcookie');
//    if (ckidata != null) {

//        data = $.parseJSON(ckidata);
//        var values = {};
//        values["fromdatetime"] = $("#txb1").val() + ' ' + $("#TextBox3").val();
//        values["todatetime"] = $("#txb2").val() + ' ' + $("#TextBox2").val();
//        values["amount"] = $("#Label1").html().trim();
//        values["option"] = $("#drpl option:selected").text();
//        values["total"] = "";
//        values["qnty"] = $("# totq").val().trim();
//        values["prodname"] = $("#labelname1").html().trim();
//        values["image"] = $('.slide-item').first().attr('data-thumb');
//        values["subtotal"] = "";
//        values["total1"] = $("#Label2").html().trim();
//        values["days"] = $("#lblerrr").html().trim();
//        values["cost"] = parseFloat($("# totq").val().trim()) * parseFloat($("#Label1").html().trim());
//        values["id"] = GetParameterValues('id');
//        data.push(values);
//        document.cookie = 'Productcookie=' + JSON.stringify(data);
//    }


//    else {
//        var values = {};
//        values["fromdatetime"] = $("#txb1").val() + ' ' + $("#TextBox3").val();
//        values["todatetime"] = $("#txb2").val() + ' ' + $("#TextBox2").val();
//        values["amount"] = $("#Label1").html().trim();
//        values["option"] = $("#drpl option:selected").text();
//        values["total"] = "";
//        values["qnty"] = $("# totq").val().trim();
//        values["prodname"] = $("#labelname1").html().trim();
//        values["image"] = $('.slide-item').first().attr('data-thumb');
//        values["subtotal"] = "";
//        values["total1"] = $("#Label2").html().trim();
//        values["days"] = $("#lblerrr").html().trim();
//        values["cost"] = "";
//        values["id"] = GetParameterValues('id');
//        data.push(values);
//        document.cookie = 'Productcookie=' + JSON.stringify(data);
//    }
//    //alert("Item Added to Cart Successfully");
//    //console.log("Added.Continue?");
//    var answer = confirm('Item Added to Cart..!Do u want to Contiune Shopping ?');
//    if (answer)
//    {
//        console.log('yes');
//        window.top.location.href = "shop.aspx";
//    }
//    else
//    {
//        console.log('cancel');
//        window.top.location.href = "cart.aspx";
//    }


//}
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}
function logout() {
    window.top.location.href = "Default.aspx";
    delete_cookie('usrname');
}
var delete_cookie = function (name) {
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};
