console.log('Ashley for the WIN$$$$$$$')

"https://smtpjs.com/v3/smtp.js"

function sendEmail(){
    Email.send({
        Host : "smtp.gmail.com",
        Username : "******",
        Password : "***********",
        To : '***********',
        From : document.getElementById("email").value,
        Subject : "Royal Doggie Inquiry",
        Body : "Name: " + document.querySelectorAll("#first_name, #last_name").values
        + "<br> Email: " + document.getElementById("email").value
        + "<br> State: " + document.getElementById("state").value
        + "<br> Phone Number: " + document.getElementById("telephone").value
        + "<br> Questions: " + document.getElementById("question").value

}).then(
  message => alert("Thank You, We will respond soon!")
);
}


// function myFunction() {
//     let x = document.getElementById("myNavbar");
//     if (x.className === "nav-bar") {
//       x.className += " responsive";
//     } else {
//       x.className = "nav-bar";
//     }
//   }