// playSong.js

async function playSong(track) {
    const response = await fetch('/play_song', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(track)
    });
    if (response.redirected) {
        window.location.href = response.url;
    }
}

// Export the function if using modules
export { playSong };
