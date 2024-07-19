# Musa - Emotion-Based Music Recommendation System

Musa is a web application that uses facial emotion detection to recommend music tracks. The application integrates with Spotify to fetch songs based on the detected emotion and provides features for user authentication and song history tracking.

## Features

- **Emotion Detection**: Uses a webcam to detect the user's facial expression and determine their emotion.
- **Music Recommendation**: Recommends songs based on the detected emotion using Spotify's API.
- **User Authentication**: Allows users to sign up, log in, and log out.
- **Song History**: Tracks the history of songs played by each user.
- **Genre-Based Browsing**: Users can browse and play songs from specific genres.

## Requirements

- Python 3.8+
- Virtual environment (recommended)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/musa.git
    cd musa
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your Spotify API credentials:
    ```env
    CLIENT_ID=your_spotify_client_id
    CLIENT_SECRET=your_spotify_client_secret
    SECRET_KEY=your_flask_secret_key
    ```

5. **Initialize the database**:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Running the Application

To run the application locally, execute the following command:


flask run```


The application will be accessible at http://127.0.0.1:5000.

API Endpoints
Home Page: /
Sign Up: /signup
Log In: /login
Log Out: /logout
Emotion Detection: /emotion
Get Tracks by Emotion: /get_tracks
Play Song: /play_song
User Profile: /profile
Song History: /history
Genres: /genres
Songs by Genre: /songs_by_genre
Usage
Sign Up: Create a new account using the sign-up page.
Log In: Log in with your credentials.
Detect Emotion: Allow access to your webcam to detect your facial expression.
Get Music Recommendations: Based on the detected emotion, get a list of recommended songs.
Play Songs: Click on any recommended song to play it.
View History: Check the history of songs you have played in your profile.


### Technologies Used
Flask: Web framework for Python.
Flask-SQLAlchemy: SQL toolkit for Flask.
Flask-Bcrypt: Password hashing for Flask.
Flask-Login: User session management for Flask.
TensorFlow: Machine learning framework for emotion detection.
OpenCV: Computer vision library for real-time emotion detection.
Spotify API: To fetch music tracks and playlists.
HTML/CSS/JavaScript: For the front-end interface.
Contributing
Contributions are welcome! Please submit a pull request or create an issue for any feature requests or bug reports.

Demo Video
Check out this demo video to see Musa in action:

http://127.0.0.1:5000.


Contributing
Contributions are welcome! Please submit a pull request or create an issue for any feature requests or bug reports.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Spotify for Developers for the Spotify API.
Flask for the web framework.
OpenCV for the computer vision library.