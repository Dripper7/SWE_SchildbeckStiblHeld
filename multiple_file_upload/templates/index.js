// Get the input field and the button
var videoNameInput = document.getElementById("video-name-input");
var playButton = document.getElementById("play-button");

// Get the video element
var video = document.getElementById("video");

// Add an event listener to the button
playButton.addEventListener("click", function() {
    // Get the video name
    var videoName = videoNameInput.value;
    // Construct the URL to the video file
    var videoUrl = "http://localhost:5000/videos/" + videoName;
    // Set the source of the video element
    video.src = videoUrl;
    // Play the video
    video.play();
});
