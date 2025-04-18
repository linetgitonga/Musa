const audio = document.querySelector('audio');
const playButton = document.getElementById('play');
const nextButton = document.getElementById('next');
const prevButton = document.getElementById('prev');
const progressBar = document.getElementById('progress-bar');

// Play/Pause toggle
playButton.addEventListener('click', () => {
    if (audio.paused) {
        audio.play();
        playButton.textContent = 'Pause';
    } else {
        audio.pause();
        playButton.textContent = 'Play';
    }
});

// Update progress bar
audio.addEventListener('timeupdate', () => {
    const progress = (audio.currentTime / audio.duration) * 100;
    progressBar.value = progress;
});

// Next and Previous song logic (this can be updated with real song data)
nextButton.addEventListener('click', () => {
    // Logic for playing the next song
});

prevButton.addEventListener('click', () => {
    // Logic for playing the previous song
});
