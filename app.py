from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import requests
import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Define the SongHistory model
class SongHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer)
    title = db.Column(db.String(150))
    artist = db.Column(db.String(150))
    emotion = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
       
       
# FavoriteSong model
class FavoriteSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150), nullable=False)


class Track(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(150), nullable=False)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)

class PlaylistSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)
    song_id = db.Column(db.String(50), db.ForeignKey('track.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_favorite_songs(user_id):
    return FavoriteSong.query.filter_by(user_id=user_id).all()

# Initialize the database
with app.app_context():
    db.create_all()
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))


@app.route('/is_logged_in')
def is_logged_in():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})



# Load the trained model
model = load_model('utils/emotion_model.h5')

# Define emotions
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize webcam
camera = cv2.VideoCapture(0)

# Spotify API credentials
CLIENT_ID = 'a162a1e3371d4d41b8ab9ccef69dfce3'
CLIENT_SECRET = '20b571da473b4fb4b171a4f6693e2ea5'

# Get access token
auth_response = requests.post('https://accounts.spotify.com/api/token', {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

headers = {
    'Authorization': f'Bearer {access_token}'
}

current_song = {}


def get_tracks(emotion, offset=0, limit=20):
    search_url = 'https://api.spotify.com/v1/search'
    params = {
        'q': emotion,
        'type': 'track',
        'limit': limit,
        'offset': offset
    }
    response = requests.get(search_url, headers=headers, params=params)
    tracks = response.json()['tracks']['items']
    return [{
        'id': track['id'],
        'title': track['name'],
        'artist': track['artists'][0]['name'],
        'image': track['album']['images'][0]['url'],
        'preview_url': track['preview_url']
    } for track in tracks]


@app.route('/get_tracks', methods=['POST'])
def get_tracks_endpoint():
    data = request.json
    emotion = data.get('emotion')
    offset = data.get('offset', 0)
    limit = data.get('limit', 20)
    tracks = get_tracks(emotion, offset, limit)
    return jsonify(tracks)


# def log_song_to_history(song_id, title, artist, emotion):
#     conn = sqlite3.connect('songs.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO song_history (song_id, title, artist, emotion)
#         VALUES (?, ?, ?, ?)
#     ''', (song_id, title, artist, emotion))
#     conn.commit()
#     conn.close()

def log_song_to_history(user_id, song_id, title, artist, emotion):
    new_song_history = SongHistory(user_id=user_id, song_id=song_id, title=title, artist=artist, emotion=emotion)
    db.session.add(new_song_history)
    db.session.commit()

@app.route('/index')
def index():
    return render_template('index.html')


def detect_emotion(frame):
    # Preprocess the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (48, 48))
    normalized = resized / 255.0
    reshaped = np.reshape(normalized, (1, 48, 48, 1))

    # Predict emotion
    prediction = model.predict(reshaped)
    emotion_label = emotions[np.argmax(prediction)]

    return emotion_label


def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Detect emotion in the frame
            emotion = detect_emotion(frame)

            # Display emotion on the frame
            cv2.putText(frame, emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    logging.debug("Video feed requested.")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/emotion')
def emotion():
    success, frame = camera.read()
    if success:
        emotion = detect_emotion(frame)
        return jsonify({'emotion': emotion})
    return jsonify({'emotion': 'N/A'})




@app.route('/song/<song_id>', methods=['GET'])
def song(song_id):
    song = current_song.get(song_id)
    return render_template('song.html', song=song)



@app.route('/play_song', methods=['POST'])
def play_song():
    if not current_user.is_authenticated:
        return jsonify({'message': 'User not logged in!'}), 401
    
    data = request.json
    song_id = data.get('id')
    current_song[song_id] = data
    return redirect(url_for('song', song_id=song_id))
    
   


@app.route('/history')
@login_required
def history():
    if current_user.is_authenticated:
        user_id = current_user.id
        history = SongHistory.query.filter_by(user_id=user_id).order_by(SongHistory.timestamp.desc()).all()
        return render_template('history.html', history=history)
    else:
        flash('You need to log in to view your history.')
        return redirect(url_for('login'))


@app.route('/genres')
def genres():
    return render_template('genres.html')

def get_available_genres():
    url = 'https://api.spotify.com/v1/recommendations/available-genre-seeds'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('genres', [])
    else:
        print(f"Error: {response.status_code}")
        return []
    
def get_genre_playlists(category_id):
    playlists_url = f'https://api.spotify.com/v1/browse/categories/{category_id}/playlists'
    response = requests.get(playlists_url, headers=headers)
    playlists = response.json()['playlists']['items']
    return playlists

def get_tracks_from_playlist(playlist_id):
    playlist_tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    response = requests.get(playlist_tracks_url, headers=headers)
    tracks = response.json()['items']
    return [{
        'id': track['track']['id'],
        'title': track['track']['name'],
        'artist': track['track']['artists'][0]['name'],
        'image': track['track']['album']['images'][0]['url'],
        'preview_url': track['track']['preview_url']
    } for track in tracks]

@app.route('/songs_by_genre', methods=['POST'])
def songs_by_genre():
    data = request.json
    genre = data.get('genre').lower()
    limit = data.get('limit', 40)

    # Get all categories
    browse_url = 'https://api.spotify.com/v1/browse/categories'
    response = requests.get(browse_url, headers=headers)
    categories = response.json()['categories']['items']
    
    # Match user genre to Spotify category
    category_id = next((category['id'] for category in categories if category['name'].lower() == genre), None)
    
    if category_id:
        playlists = get_genre_playlists(category_id)
        if playlists:
            playlist_id = playlists[0]['id']
            tracks = get_tracks_from_playlist(playlist_id)
            return jsonify(tracks[:limit])
    
    return jsonify([])

# @app.route('/songs_by_genre', methods=['POST'])
# def songs_by_genre():
#     data = request.json
#     genre = data.get('genre')
#     offset = data.get('offset', 0)
#     limit = data.get('limit', 10)
#     tracks = genre_get_tracks(genre, offset, limit)
#     return jsonify(tracks)


# def genre_get_tracks(query, offset=0, limit=10):
#     search_url = 'https://api.spotify.com/v1/search'
#     params = {
#         'q': query,
#         'type': 'track',
#         'limit': limit,
#         'offset': offset
#     }
#     response = requests.get(search_url, headers=headers, params=params)
#     tracks = response.json()['tracks']['items']
#     return [{
#         'id': track['id'],
#         'title': track['name'],
#         'artist': track['artists'][0]['name'],
#         'image': track['album']['images'][0]['url'],
#         'preview_url': track['preview_url']
#     } for track in tracks]

@app.route('/trending')
def trending():
    trending_songs = get_trending_tracks()
    return render_template('trending.html', songs=trending_songs)

def get_trending_tracks(limit=30):
    # Get trending songs globally
    url = 'https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks'  # Spotify's Global Top 50 playlist
    params = {
        'limit': limit
    }
    response = requests.get(url, headers=headers, params=params)
    tracks = response.json()['items']
    return [{
        'id': track['track']['id'],
        'title': track['track']['name'],
        'artist': track['track']['artists'][0]['name'],
        'image': track['track']['album']['images'][0]['url'],
        'preview_url': track['track']['preview_url']
    } for track in tracks]
    
    

@app.route('/profile')
@login_required

def profile():
    user = User.query.get(current_user.id)
    favorite_songs = get_favorite_songs(user.id)  # Function to fetch favorite songs
    return render_template('profile.html', user=user, favorite_songs=favorite_songs)




@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.bio = request.form.get('bio')
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        if check_password_hash(current_user.password, current_password):
            current_user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('profile'))
        else:
            flash('Current password is incorrect.')
    return render_template('change_password.html')


current_song = {}
user_history = {}
user_likes = {}
user_playlists = {}


@app.route('/song/<song_id>', methods=['GET'])
def song_page(song_id):
    song = Track.query.get(song_id)
    if song:
        # Fetch additional details from Spotify if necessary
        track_details = fetch_additional_track_details(song_id)
        song_details = {**song.__dict__, **track_details}
        return render_template('song.html', song=song_details)
    return "Song not found", 404



@app.route('/like_song/<song_id>', methods=['POST'])
@login_required
def like_song(song_id):
    user_id = current_user.id
    if not FavoriteSong.query.filter_by(user_id=user_id, song_id=song_id).first():
        song = Track.query.get(song_id)
        if song:
            favorite_song = FavoriteSong(user_id=user_id, song_id=song_id, title=song.title, artist=song.artist)
            db.session.add(favorite_song)
            db.session.commit()
            return jsonify({'message': 'Song liked!'})
        return jsonify({'message': 'Song not found!'}), 404
    return jsonify({'message': 'Song already liked!'})

@app.route('/add_to_playlist', methods=['POST'])
@login_required
def add_to_playlist():
    user_id = current_user.id
    data = request.json
    playlist_name = data.get('playlist_name')
    song_id = data.get('song_id')

    if not playlist_name or not song_id:
        return jsonify({'message': 'Missing data!'}), 400

    playlist = Playlist.query.filter_by(user_id=user_id, name=playlist_name).first()
    if not playlist:
        playlist = Playlist(user_id=user_id, name=playlist_name)
        db.session.add(playlist)
        db.session.commit()

    if not PlaylistSong.query.filter_by(playlist_id=playlist.id, song_id=song_id).first():
        playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        return jsonify({'message': 'Song added to playlist!'})
    
    return jsonify({'message': 'Song already in playlist!'})

@app.route('/liked_songs', methods=['GET'])
@login_required
def liked_songs():
    user_id = current_user.id
    liked_songs = FavoriteSong.query.filter_by(user_id=user_id).all()
    return render_template('liked_songs.html', songs=[Track.query.get(song.song_id) for song in liked_songs])

@app.route('/playlists', methods=['GET'])
@login_required
def playlists():
    user_id = current_user.id
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    return render_template('playlists.html', playlists=playlists)

@app.route('/playlist/<playlist_name>', methods=['GET'])
@login_required
def view_playlist(playlist_name):
    user_id = current_user.id
    playlist = Playlist.query.filter_by(user_id=user_id, name=playlist_name).first()
    if not playlist:
        return "Playlist not found", 404
    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist.id).all()
    songs = [Track.query.get(song.song_id) for song in playlist_songs]
    return render_template('playlist.html', playlist_name=playlist_name, songs=songs)


@app.route('/search')
def search():
    search_url = 'https://api.spotify.com/v1/search'
    query = request.args.get('query')
    emotion = request.args.get('emotion')  # If you need to handle emotion
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return render_template('search_results.html', query=query, results=[])

    params = {
        'q': query,
        'type': 'track',
        'limit': limit,
        'offset': offset
    }
    response = requests.get(search_url, headers=headers, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Spotify API'}), response.status_code

    tracks = response.json()['tracks']['items']
    results = [{
        'id': track['id'],
        'title': track['name'],
        'artist': track['artists'][0]['name'],
        'image': track['album']['images'][0]['url'],
        'preview_url': track['preview_url']
    } for track in tracks]

    return render_template('search_results.html', query=query, results=results)

@app.route('/')
def landing_page():
    return render_template('landingpage.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')
if __name__ == '__main__':
    app.run(debug=True)