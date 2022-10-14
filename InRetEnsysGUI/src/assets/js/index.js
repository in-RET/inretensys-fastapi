function toggle_display() {
    el = document.getElementById('popupForm_Storage');
    //el = document.querySelector('.content_section');
    if (el.style.display == "none") {
        el.style.display = "block";
        //alert(document.getElementById("StorageWindow5").id);
        drag_and_drop_element_id = document.getElementById("StorageWindow5").id;

        var server_data = [
            { "drag_and_drop_element_id": drag_and_drop_element_id },
            { "Hello": "World" }
        ];

        $.ajax({
            type: "POST",
            url: "/getdivID_storage",
            data: JSON.stringify(server_data),
            contentType: "application/json",
            dataType: 'json',
            success: function (result) {
                $("#successMessage1").show();
            }
        });

    } else {
        el.style.display = "none";
        alert("2");
    }
}


var optimisation_results_meta = document.getElementById("optimisation_results_meta");
function runTheSystem() {
    $.ajax({
        type: "POST",
        url: "/solveEnergysystem",
        contentType: "application/json",
        //dataType: 'json',
        success: function (response) {
            optimisation_results_meta.innerHTML = response;
        }
    });

}

function show_popup() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
}
/*function displayMessage(){
    //document.getElementById("msg").innerHTML = "The button has been clicked.";
    alert('inside here');
var form_data = new FormData($('#upload-file')[0]);
alert(form_data);
$.ajax({
    type: 'POST',
    url: '/uploadajax',
    data: form_data,
    contentType: false,
    cache: false,
    processData: false,
    success: function(data) {
        console.log('Success!');
    },
});
}   
var btn = document.getElementById("upload-file-btn");
btn.addEventListener("click", displayMessage);*/


/*document.getElementById('button2')
.addEventListener('click', function () {
    createElement();
});*/

function createElement() {
    /*const el = document.createElement('div');
    el.classList.add('window');
    el.textContent = 'Source';
    const box = document.getElementById('box');
    box.appendChild(el);*/

    // create paragraph element
    let pElement = document.createElement('div');
    pElement.classList.add("window");

    // create text node
    //let pElementText = document.createTextNode("50% off!!"); 

    // append text node to paragraph
    //pElement.appendChild(pElementText);

    // get handle of parent element where we need to insert dynamic element
    let parent = document.querySelector('#SourceWindow1');

    // append the dynamic paragrah element
    parent.appendChild(pElement);

}
///////////////////////////////////////////////////////////////////////

function myFunction() {
    var checkBox = document.getElementById("investment");
    var text_for_invest = document.getElementById("text_for_invest");
    if (checkBox.checked == true) {
        text_for_invest.style.display = "block";
    } else {
        text_for_invest.style.display = "none";
    }
}

//Performance Price
function myFunction_for_pp() {
    var checkBox = document.getElementById("investment_for_pp");
    var text_for_invest = document.getElementById("text_for_invest_for_pp");
    if (checkBox.checked == true) {
        text_for_invest.style.display = "block";
    } else {
        text_for_invest.style.display = "none";
    }
}


var drag_and_drop_element_id = "";
function getId(component) {
    drag_and_drop_element_id = component.id;
}

///////////////////////////////////////////////////////////////////////

//close and clear input fields
function closeForm_Source() {
    document.getElementById("popupForm_Source").style.display = "none";
    const inputs = document.querySelectorAll('#label_source, #min_source, #max_source, #summed_max_source, #summed_min_source, #capex_source, #opex_source, #amortisation_source, #min_leistung_source, #max_leistung_source, #capex_pp, #max_leistung_pp');
    inputs.forEach(input => {
        input.value = '';
    });
    $("#investment_for_pp").prop('checked', false);
    $("#investment").prop('checked', false);
    myFunction_for_pp();
    myFunction();
    $('#id_fix_file_input_field_source').val(''); //reset file input element
    $('#id_vc_file_input_field_source').val(''); //reset file input element
}

function closeForm_Bus() {
    document.getElementById("popupForm_Bus").style.display = "none";
    //$('#popupForm_Bus').trigger("reset");
    const inputs = document.querySelectorAll('#label_bus');
    inputs.forEach(input => {
        input.value = '';
    });
}

function closeForm_Sink() {
    document.getElementById("popupForm_Sink").style.display = "none";
    const inputs = document.querySelectorAll('#label_sink, #nominal_value, #fix, #variable_costs');
    inputs.forEach(input => {
        input.value = '';
    });
    $('#id_fix_file_input_field_sink').val(''); //reset file input element
}

function closeForm_Storage() {
    document.getElementById("popupForm_Storage").style.display = "none";
}

///////////////////////////////////////////////////////////////////////

function connect_info(sourceId, targetId) {
    //window.alert(sourceId + ' ' + targetId);

    var server_data = [
        { "sourceId": sourceId },
        { "targetId": targetId },
    ];

    $.ajax({
        type: "POST",
        url: "/connect_info",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            $("#successMessage1").show();
        }
    });
}

function connect_info_bus_to_sink(sourceId, targetId) {
    //window.alert(sourceId + ' ' + targetId);

    var server_data = [
        { "sourceId": sourceId },
        { "targetId": targetId },
    ];

    $.ajax({
        type: "POST",
        url: "/connect_info_b_to_sink",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            $("#successMessage1").show();
        }
    });
}


function connect_info_bus_to_storage(sourceId, targetId) {
    window.alert(sourceId + ' ' + targetId);

    var server_data = [
        { "sourceId": sourceId },
        { "targetId": targetId },
    ];

    $.ajax({
        type: "POST",
        url: "/connect_info_b_to_storage",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            $("#successMessage1").show();
        }
    });
}


// epc calculation source
var epc = 0;
function epc_calc() {
    var capex = parseFloat(document.getElementById("capex_source").value);
    var opex = parseFloat(document.getElementById("opex_source").value) / 100;
    var n = parseFloat(document.getElementById("amortisation_source").value);
    var wacc = parseFloat(document.getElementById("zins_source").value) / 100;
    annuity = capex * (wacc * (1 + wacc) ** n) / ((1 + wacc) ** n - 1);
    betriebskosten = capex * opex;
    epc = annuity + betriebskosten;
    return epc;

}
/////////////////////////////////

//submit flow information and send them to server
function submit_flow_bus() {
    var label = document.getElementById("label_bus").value;
    //var btn_id = btn.id; //btn_submit_bus id

    var server_data = [
        { "label": label },
        { "drag_and_drop_element_id": drag_and_drop_element_id },
        //{"button_id": btn_id},
    ];

    $.ajax({
        type: "POST",
        url: "/flowBus",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            $("#successMessage").show();
            $('#bus_label_to_div').html(label);
        }
    });
}


function submit_flow_source(btn) {
    //window.alert('I am here');
    alert(document.getElementById("capex_source").value);
    var label = document.getElementById("label_source").value;
    //Flow()
    var slider = document.getElementById("myRange");
    var nv = parseInt(slider.value); //parseFloat(document.getElementById("nominal_value").value);
    //var fix = parseFloat(document.getElementById("fix").value);
    var min = parseFloat(document.getElementById("min_source").value);
    var max = parseFloat(document.getElementById("max_source").value);
    var summed_max = parseFloat(document.getElementById("summed_max_source").value);
    var summed_min = parseFloat(document.getElementById("summed_min_source").value);
    //var vc = parseFloat(document.getElementById("variable_costs").value);
    //investment
    //epc_calc();
    var min_leistung = null; // = parseFloat(document.getElementById("min_leistung").value);
    var max_leistung = null; // = parseFloat(document.getElementById("max_leistung").value);
    var epc = null;
    //Leistungspreis
    //var performance_price_grid = parseFloat(document.getElementById("capex_pp").value);
    //var max_bezugsleistung_grid = parseFloat(document.getElementById("max_leistung_pp").value);

    if (document.getElementById("capex_source").value.length !== 0) //usual Investment modell
    {
        //alert('document.getElementById("capex").value.length !== 0');
        epc = epc_calc();
        min_leistung = parseFloat(document.getElementById("min_leistung_source").value);
        max_leistung = parseFloat(document.getElementById("max_leistung_source").value);
    }
    else if (document.getElementById("capex_pp").value.length !== 0) //using Performance Price for Grid
    {
        //alert('This way');
        epc = parseFloat(document.getElementById("capex_pp").value);
        min_leistung = 0;
        max_leistung = parseFloat(document.getElementById("max_leistung_pp").value);
    }

    //var btn_id = btn.id; //btn_submit_source id

    var server_data = [
        { "label": label },
        { "nominal_value": nv },
        //{"fix": fix},
        { "min": min },
        { "max": max },
        { "summed_max": summed_max },
        { "summed_min": summed_min },
        //{"variable_costs": vc},
        { "epc": epc },
        { "min_leistung": min_leistung },
        { "max_leistung": max_leistung },
        { "drag_and_drop_element_id": drag_and_drop_element_id },
        //{"button_id": btn_id},
    ];


    //alert('inside here');
    //var formdata = new FormData();
    //formdata.append('simpleFile', $('#upload-file').get('files')[0]); //use get('files')[0]
    //alert(form_Data);

    var bar = document.getElementById("bar");
    var form_Data = new FormData($('#upload-file')[0]);
    form_Data.append('label', label);
    $.ajax({
        type: 'POST',
        url: '/uploadajax',
        data: form_Data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {
            bar.innerHTML = response;
        },
    });

    var response_upload_source_vc = document.getElementById("response_upload_source_vc");
    var form_Data_source_vc = new FormData($('#upload_file_source_vc')[0]);
    form_Data_source_vc.append('label', label);
    $.ajax({
        type: 'POST',
        url: '/uploadajax_source_vc',
        data: form_Data_source_vc,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {
            response_upload_source_vc.innerHTML = response;
        },
    });


    $.ajax({
        type: "POST",
        url: "/flowSource",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            //$('#source2_label_to_div').html(label);
            //$("#" + drag_and_drop_element_id).html(label);
            //alert(drag_and_drop_element_id);
            //alert(document.getElementById(drag_and_drop_element_id.toString()));
            //tnames = $("#" + drag_and_drop_element_id).attr('id');
            //tnames = document.getElementById();
            //var toggle = document.getElementById(drag_and_drop_element_id.toString());
            //toggle.getElementsByTagName('span').textContent = "New Span content";

            let container = document.getElementById(drag_and_drop_element_id.toString());
            let spans = container.getElementsByTagName("span");
            for (let span of spans) {
                span.textContent = label;
            }
        }
    });



    /*				
    setInterval(function(){
        $.ajax({
          url: "/uploadajax",
          type: "get",
          success: function(response) {
            
     bar.innerHTML = response;
           },
          error: function(xhr) {
              //Handel error
          }
        }); 
    }, 10);*/
}

function submit_flow_sink() {
    //window.alert('I am here');
    var label = document.getElementById("label_sink").value;
    //Flow()
    var nv = parseFloat(document.getElementById("nominal_value_sink").value);
    //var fix = parseFloat(document.getElementById("fix_sink").value);
    var vc = parseFloat(document.getElementById("variable_costs_sink").value);

    var bar = document.getElementById("upload_error_sink");
    var form_Data = new FormData($('#upload_load_profile_sink')[0]);
    form_Data.append('label', label);
    $.ajax({
        type: 'POST',
        url: '/uploadajax_sink',
        data: form_Data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {
            bar.innerHTML = response;
        },
    });

    var server_data = [
        { "label": label },
        { "nominal_value": nv },
        //{"fix": fix},
        { "variable_costs": vc },
        { "drag_and_drop_element_id": drag_and_drop_element_id },
    ];

    $.ajax({
        type: "POST",
        url: "/flowSink",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            $('#sink_label_to_div').html(label);
        }
    });
}

//handle slider
var slider = document.getElementById("myRange");
var output = document.getElementById("slider_value");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function () {
    output.innerHTML = this.value;
}

