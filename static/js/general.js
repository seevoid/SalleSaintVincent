$('#error_resa').append(' ')
$('#error_contact').append(' ')

var price = 0
$("#price_to_change").text(price.toString())
const price_per_day = 50
const price_video = 20
const price_sono = 30
const price_dj = 40

var verif_phone_resa = false
var verif_name_resa = false
var verif_email_resa = false
var verif_message_resa = false

var verif_phone_contact = false
var verif_name_contact = false
var verif_email_contact = false
var verif_message_contact = false

////////////------ FORMS VERIFICATION ------////////////

function validateEmail(email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return (email.length > 0 && emailReg.test(email));
}

$("#phone_number_resa").focusout(function(){
  var numTel = $(this).val();
  var rgxPhone = /(([0-9]{2})){5}/
  if ( !numTel.match(rgxPhone)){
    $("#verif_phone_resa").html('<i style="color: red;" class="fas fa-times"></i>')
    verif_phone_resa = false
  }else{
    $("#verif_phone_resa").html('<i style="color: green;" class="fas fa-check"></i>')
    verif_phone_resa = true
  }
});

$("#email_resa").focusout(function(){
  var emailaddress = $(this).val();
  if ( !validateEmail(emailaddress)){
    $("#verif_email_resa").html('<i style="color: red;" class="fas fa-times"></i>')
    verif_email_resa = false
  }else{
    $("#verif_email_resa").html('<i style="color: green;" class="fas fa-check"></i>')
    verif_email_resa = true
  }
});

$("#name_resa").focusout(function(){
  var name = $(this).val();
  if (name.length < 3){
    $("#verif_name_resa").html('<i style="color: red;" class="fas fa-times"></i>')
    verif_name_resa = false
  }else{
    $("#verif_name_resa").html('<i style="color: green;" class="fas fa-check"></i>')
    verif_name_resa = true
  }
});

$("#message_resa").focusout(function(){
  var message = $(this).val();
  console.log("message : "+ message)
  if (message.length < 50){
    $("#verif_message_resa").html('<i style="color: red;" class="fas fa-times"></i>')
    verif_message_resa = false
  }else{
    $("#verif_message_resa").html('<i style="color: green;" class="fas fa-check"></i>')
    verif_message_resa = true
  }
});

$("#phone_number_contact").focusout(function(){
  var numTel = $(this).val();
  var rgxPhone = /(([0-9]{2})){5}/
  if ( !numTel.match(rgxPhone)){
    $("#verif_phone_contact").html('<i style="color: red;" class="fas fa-times fa-lg"></i>')
    verif_phone_contact = false
  }else{
    $("#verif_phone_contact").html('<i style="color: green;" class="fas fa-check fa-lg"></i>')
    verif_phone_contact = true
  }
});

$("#email_contact").focusout(function(){
  var emailaddress = $(this).val();
  if ( !validateEmail(emailaddress)){
    $("#verif_email_contact").html('<i style="color: red;" class="fas fa-times fa-lg"></i>')
    verif_email_contact = false
  }else{
    $("#verif_email_contact").html('<i style="color: green;" class="fas fa-check fa-lg"></i>')
    verif_email_contact = true
  }
});

$("#name_contact").focusout(function(){
  var name = $(this).val();
  if (name.length < 3){
    $("#verif_name_contact").html('<i style="color: red;" class="fas fa-times fa-lg"></i>')
    verif_name_contact = false
  }else{
    $("#verif_name_contact").html('<i style="color: green;" class="fas fa-check fa-lg"></i>')
    verif_name_contact = true
  }
});

$("#message_contact").focusout(function(){
  var message = $(this).val();
  console.log("message : "+ message)
  if (message.length < 50){
    $("#verif_message_contact").html('<i style="color: red;" class="fas fa-times fa-lg"></i>')
    verif_message_contact = false
  }else{
    $("#verif_message_contact").html('<i style="color: green;" class="fas fa-check fa-lg"></i>')
    verif_message_contact = true
  }
});


$('#form_contact').on('submit', function(e){
  if (!verif_phone_contact || !verif_email_contact || !verif_name_contact || !verif_message_contact) {
    e.preventDefault();
    $('#error_contact').remove()
    $('#error_contact').append('Veuillez correctement remplir les champs ci-dessus.')
  }
});




////////////------ GALLERY ------////////////

popup = {
  init: function(){
    $('figure').click(function(){
      popup.open($(this));
    });
    
    $(document).on('click', '.popup img', function(){
      return false;
    }).on('click', '.popup', function(){
      popup.close();
    })
  },
  open: function($figure) {
    $('.gallery').addClass('pop');
    $popup = $('<div class="popup" />').appendTo($('body'));
    $fig = $figure.clone().appendTo($('.popup'));
    $bg = $('<div class="bg" />').appendTo($('.popup'));
    $close = $('<div class="close"><svg><use xlink:href="#close"></use></svg></div>').appendTo($fig);
    $shadow = $('<div class="shadow" />').appendTo($fig);
    src = $('img', $fig).attr('src');
    $shadow.css({backgroundImage: 'url(' + src + ')'});
    $bg.css({backgroundImage: 'url(' + src + ')'});
    setTimeout(function(){
      $('.popup').addClass('pop');
    }, 10);
  },
  close: function(){
    $('.gallery, .popup').removeClass('pop');
    setTimeout(function(){
      $('.popup').remove()
    }, 100);
  }
}

popup.init()




////////////------ JSCALENDAR ------////////////

// Get the element
var element = document.getElementById("my-calendar");
// Create the calendar
var myCalendar = jsCalendar.new(element);
// Get the buttons
var list_of_dates = []

function isInArray(value, array) {
  return array.indexOf(value) > -1;
}

myCalendar.onDateClick(function(event, date){
  if (!myCalendar.isSelected_green(date)) {
    if (!myCalendar.isSelected(date)) {
      myCalendar.select_green(date)
      list_of_dates.push(date)
      document.getElementById("dates_resa").value = list_of_dates.join();
      price = price + price_per_day
    }
  } else {
    myCalendar.unselect_green(date)
    list_of_dates.splice(list_of_dates.indexOf(date), 1);
    price = price - price_per_day
  }
  $("#price_to_change").text(price.toString())
});

error_resa = false

$('#form_resa').on('submit', function(e){
  if (list_of_dates.length == 0) {
    e.preventDefault();
    if (error_resa == false) {
      $('#error_resa').remove()
      $('#error_resa').append('Veuillez sélectionner au moins une date pour votre évènement.')
      error_resa = true
    }
  }

  if (!verif_phone_resa || !verif_email_resa || !verif_name_resa || !verif_message_resa) {
    e.preventDefault();
    $('#error_resa').remove()
    $('#error_resa').append('Veuillez correctement remplir les champs ci-dessus.')
  }
});


////////////------ QUOTES CAROUSEL ------////////////

$(document).ready(function() {
  //Set the carousel options
  $('#quote-carousel').carousel({
    pause: true,
    interval: 4000,
  });
});






////////////------ PRICE MODIFICATION WITH CHECKBOXES ------////////////

var current_radio = "fete"
var chkbox_dj = $("#label_chkbox_dj")

$( "#radio_pro" ).click(function() {
  $( "#radio_fete" ).prop('checked', false);
  current_radio = "pro"

  chkbox_dj.css({'opacity': '0', 'position': 'absolute'});
});

$( "#radio_fete" ).click(function() {
  $( "#radio_pro" ).prop('checked', false);
  if (current_radio !== "fete") {

    current_radio = "fete"

    chkbox_dj.css({'opacity': '100', 'position': 'relative'});
  }

});

$("#chkbox_video").click(function() {
  console.log("CLICKED")
  if ($("#chkbox_video").prop("checked")) {
    price = price + price_video
  } else {
    price = price - price_video
  }
  $("#price_to_change").text(price.toString())
})

$("#chkbox_sono").click(function() {
  if ($("#chkbox_sono").prop("checked")) {
    price = price + price_sono
  } else {
    price = price - price_sono
  }
  $("#price_to_change").text(price.toString())
})

$("#chkbox_dj").click(function() {
  if ($("#chkbox_dj").prop("checked")) {
    price = price + price_dj
  } else {
    price = price - price_dj
  }
  $("#price_to_change").text(price.toString())
})