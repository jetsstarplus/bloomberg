let input = document.getElementById("phone"),
errorMsg = document.getElementById("error-msg"),
validMsg = document.getElementById("valid-msg")

// here, the index maps to the error code returned from getValidationError - see readme
let errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long", "Invalid number"];
iti=window.intlTelInput(input, {
  // utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.3/build/js/utils.js",
  // BUG: Use cdn utilsScript instead
  utilsScript: intlUtils,
  allowDropdown: false,
  // autoHideDialCode: false,
  autoPlaceholder: "aggressive",
  // dropdownContainer: document.body,
  // excludeCountries: ["us"],
  // formatOnDisplay: false,
  // geoIpLookup: function(callback) {
  //   $.get("http://ipinfo.io", function() {}, "jsonp").always(function(resp) {
    //     var countryCode = (resp && resp.country) ? resp.country : "";
    //     callback(countryCode);
    //   });
    // },
    // hiddenInput: "full_number",
    initialCountry: "KE",
    // localizedCountries: { 'de': 'Deutschland' },
    // nationalMode: false,
    // onlyCountries: ['us', 'gb', 'ch', 'ca', 'do'],
    // placeholderNumberType: "MOBILE",
    // preferredCountries: ['cn', 'jp'],
    separateDialCode: true,

  });
  
  
  let reset = function() {
    input.classList.remove("error");
    errorMsg.innerHTML = "";
    errorMsg.classList.add("hide");
    validMsg.classList.add("hide");
  };
  
  // on blur: validate
  input.addEventListener('blur', () => {
    reset();
    if (input.value.trim()) {
      if (iti.isValidNumber()) {
        validMsg.classList.remove("hide");
      } else {
        input.classList.add("error");
        var errorCode = iti.getValidationError();
        errorMsg.innerHTML = errorMap[errorCode];
        errorMsg.classList.remove("hide");
      }
    }
  });
 
// on keyup / change flag: reset
input.addEventListener('change', reset);
input.addEventListener('keyup', reset);

// on blur: validate
input.addEventListener('blur', function() {
    reset();
    if (input.value.trim()) {
      if (iti.isValidNumber()) {
        validMsg.classList.remove("hide");
      } else {
        input.classList.add("error");
        var errorCode = iti.getValidationError();
        errorMsg.innerHTML = errorMap[errorCode];
        errorMsg.classList.remove("hide");
      }
    }
  });


