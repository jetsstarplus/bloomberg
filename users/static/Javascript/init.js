 function getWordCount(wordString) {
  var words = wordString.split(" ");
  words = words.filter(function(words) {
    return words.length > 0
  }).length;
  return words;
}

//add the custom validation method

function countWords(self) {
    let words = getWordCount(self.value)
    // console.log(words)
    statement = words==1 ? ' Word':' Words'
    document.getElementById("essay-counter").innerHTML = words + statement;
}

function reload(){
  location.reload(true)
  return false;
}


`An high level function for retrieving cookies`
function getCookie(name) {
  // A method for getting a csrftoken
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
// toggle the dropdown
function toggle(id) {
  let element = document.getElementById(id)
  if(element.getAttribute('aria-expanded') === 'true'){
    element.classList.add('hide')
    element.setAttribute('aria-expanded', 'false')
  }
  else{
    // automatically hide all dropdowns
    hideDropdown()
    // procceed with showing the dropdown
    element.classList.remove('hide')
    element.setAttribute('aria-expanded', 'true')

}
}


// A function for finding time difference in a date scenareo
function timeDifference(current, previous) {
  const milliSecondsPerMinute = 60 * 1000
  const milliSecondsPerHour = milliSecondsPerMinute * 60
  const milliSecondsPerDay = milliSecondsPerHour * 24
  const milliSecondsPerMonth = milliSecondsPerDay * 30
  const milliSecondsPerYear = milliSecondsPerDay * 365

  const elapsed = current - previous

  if (elapsed < milliSecondsPerMinute / 3) {
    return 'just now'
  }

  if (elapsed < milliSecondsPerMinute) {
    return 'less than 1 min ago'
  } else if (elapsed < milliSecondsPerHour) {
    return Math.round(elapsed / milliSecondsPerMinute) + ' min ago'
  } else if (elapsed < milliSecondsPerDay) {
    return Math.round(elapsed / milliSecondsPerHour) + ' hr ago'
  } else if (elapsed < milliSecondsPerMonth) {
    let time=Math.round(elapsed/milliSecondsPerDay)
    let data
    if(time===1){
      data=time + ' day ago'
    }
    else{
      data=time + ' days ago'
    }
    return data
  } else if (elapsed < milliSecondsPerYear) {
    return Math.round(elapsed / milliSecondsPerMonth) + ' mon ago'
  } else {
    let time = Math.round(elapsed / milliSecondsPerYear)
    let data
    if(time===1){
      data=time + ' yr ago'
    }
    else{
      data=time + ' yrs ago'
    }
    return data
  }
}

function timeDifferenceForDate(date) {
  const now = new Date().getTime()
  const updated = new Date(date).getTime()
  return timeDifference(now, updated)
}


// A method for disabling buttons once clicked and nothing has changed in the inputs
const disableButton = () =>{
let formInputs = document.getElementsByClassName('form-input')
  let confirmBtn = document.getElementById('confirmBtn')
  for(let i=0; i<formInputs.length; i++){
    formInputs[i].addEventListener('keyup', (e) =>{
      confirmBtn.classList.remove('disabled')
    })
  }
  if(confirmBtn){
    confirmBtn.addEventListener('mouseup', (e) =>{
      confirmBtn.classList.add('disabled')
    })
  }
}
disableButton()