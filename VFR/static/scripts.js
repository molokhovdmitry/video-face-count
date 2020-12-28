// Shows filename when user uploads a file
function showFileName() {
    var name = document.getElementById('input')
    document.getElementById('inputField').innerHTML = name.files.item(0).name;
  }

// Shows a loading animation when form is submitted
function loadingAnimation() {
document.getElementById('loader').style.display = "block";
}