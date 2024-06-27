// Function to scroll to footer when user click About and Contact US
function scrollToFooter() {
    var footer = document.getElementById('footer');
    footer.scrollIntoView({ behavior: 'smooth' });
}

function scrollToCategory() {
    var category = document.querySelector('.category');
    category.scrollIntoView({ behavior: 'smooth' });
}

//-------------------------------------------------------------------------------------------------------------

// JS for date and time
const d = new Date();
document.getElementById("demo").innerHTML = d;

//-------------------------------------------------------------------------------------------------------------

//Display data from user input
function displayInput() {
    // Get the value entered by the user
    var email = document.getElementById("emailInput").value;

    // Display the value in an alert box
    alert("Email entered: " + email + "\nThank you for signing up!");
}

//-------------------------------------------------------------------------------------------------------------
