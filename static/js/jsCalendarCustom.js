
var element = document.getElementById("my-calendar");

var calendar = jsCalendar.new(element, "13/02/2019",{

  // language
  language : "fr",

  // Enable/Disable date's number zero fill
  zeroFill : false,

  // Custom month string format
  // month: Month's full name "February"
  // ##: Month's number  "02"
  // #: Month's number  "2"
  // YYYY: Year  "2017"
  monthFormat : "month",

  // Custom day of the week string forma
  // day: Day's full name "Monday"
  // DDD: Day's first 3 letters "Mon"
  // DD: Day's first 2 letters "Mo"
  // D: Day's first letter  "M"
  dayFormat : "DDD",

  // 1 = monday
  firstDayOfTheWeek: 2,

  // Enable/Disable month's navigation buttons.
  navigator : true,

  // both | left | right
  navigatorPosition : "both",

  // min date
  min : "13/02/2019",

  // max date
  max : false
  
});




