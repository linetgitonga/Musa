
document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('video');
    const emotionResult = document.getElementById('emotion-result');

    const updateEmotionResult = () => {
        fetch('/emotion')
            .then(response => response.json())
            .then(data => {
                emotionResult.innerHTML = `Emotion: ${data.emotion}`;
            })
            .catch(error => {
                console.error('Error fetching emotion:', error);
            });
    };

    const updateVideo = () => {
        fetch('/video_feed')
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                video.src = url;
                video.onload = () => {
                    URL.revokeObjectURL(url); // free memory
                }
            })
            .catch(error => {
                console.error('Error fetching video feed:', error);
            });
    };

    // Update the emotion result every second
    setInterval(updateEmotionResult, 10000);

    // Update the video feed every second
    setInterval(updateVideo, 10000);
});


    // Update the emotion result in real-time
    // const updaeEmotionResult = () => {
    //     fetch('/video_feed')
    //         .then(response => response)
    //         .then(response => {
    //             console.log(response);
    //             emotionResult.innerHTML = response;
    //         })
    //         .catch(error => {
    //             console.error('Error fetching emotion:', error);
    //         });
    // };

    // Update the emotion result every second




