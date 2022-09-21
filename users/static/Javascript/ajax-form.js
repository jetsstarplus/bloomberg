(function ($) {
  "use strict";
  let ferror = false;
  let form = $("#ajax-form");
  var status = $("#status");
  let location = document.getElementById("progress-home");
  $('<div id="upload-progress" class="upload-progress"></div>')
    .appendTo(location)
    .append(
      `<div class="progress-container">
        <div class="progress-info" id="progress-info"></div>
        <div class="progress-bar-container" id='progress-bar-container'>
        <p class="progress-bar-info" id="progress-bar-info"></p>
        <div class="progress-bar" id="progress-bar">
        </div>
      </div></div>`
    );

  // Validation for login form
  form.validate({
    rules: {
      phone: {
        number: true,
        required: true,
        minlength: 9,
        maxlength: 13,
      },
      trans: {
        required: true,
        minlength: 5,
      },
      username: {
        required: true,
      },
      amount:{
        required: true,
        minlength: 1,
        maxlength: 6
      }

    },
    messages: {
      phone: {
        number: "Phone must be a number!",
        required: "Enter Your Safaricom Mobile Phone Number!",
        minlength: "Your Phone Number Should be atleast 9 characters!",
        maxlength: "The Phone Number is too Long!",
      },
      trans: {
        required: "Please enter The Transaction Id You Just Received!",
        minlength: "Please enter a valid Transaction Id!",
      },
      content: {
        required: "Please Write Something Here!",
        minlength: "Too Short!",
      },
      username: {
        required: "Please Select A User",
      },
      title: {
        required: "The title field is required",
      },
      date_due:{
        required: "Please select a date",
      },
      amount:{
        required: "Enter The Amount to Transact",
      }
    },

    errorPlacement: function (error, element) {
      error.insertAfter(element.parent());
      ferror = true;
    },
  });

  form.submit((e) => {
    e.preventDefault();
    if ($.data(form, 'submitted')) return false;
    if (ferror) {
      ferror = false;
      return false;
    }
    var form_data = new FormData(document.getElementById("ajax-form"));

    // let str = form.serialize();
    // form_data.append(str)
    let action = form.attr("action");
    // console.log(form.serialize())
    // This method gets the csrf token from the cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          let cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    let csrftoken = getCookie("csrftoken");

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    // This implementation uses ajax forms library from jquery.
    $.ajax({
      beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      },
      data:form_data,
      url: action,
      type: "POST",
      processData: false,
      contentType: false,
      cache: false,
      dataType: "json",
      statusCode: {
        403: function (responseObject, textStatus) {
          let text="Not Permitted! " + textStatus
          alert(text)
          // alert("Not Permitted!"+' '+textStatus)
        },
        404: function (responseObject, textStatus) {
          let text="Not Found! " + textStatus
          alert(text)
        },
        500: function (responseObject, textStatus) {
          let text="Internal Server 500! " + textStatus
          alert(text)
        },
      },
      success: function (data) {
        // console.log(data.message)
        if (data.status === 200) {
          alert(data.message)
          if (data.url != null){
            if(data.update != null  && data.update === false){              
              window.location.replace(data.url)
            }
          }
        } else {
          alert(data.message)

        }

      },
      error: () => {
        alert( "There was an error in your submission")        
      },
    });
    // $.data(form, 'submitted', true); // mark form as submitted.
  });

})(jQuery);
