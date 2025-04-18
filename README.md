# 🎵 MUSA - Emotion-Based Music Recommendation & Media Playback Web App

**MUSA** is a smart web application that blends multimedia playback with AI-powered emotion detection to recommend music based on a user's mood. It supports video and audio playback from local folders, emotion-based music suggestions, lyrics display, trending music, genre exploration, and user authentication.

---

## ✨ Key Features

- 🎭 **Emotion Detection** via webcam using OpenCV & TensorFlow
- 🎧 **Spotify-Powered Recommendations** based on emotion
- 🔍 **Search & Browse** artists, genres, and albums
- 🎼 **Lyrics Display** via Genius API
- 📂 **Folder-Based Media Grouping** (e.g., WhatsApp, Camera)
- ▶️ **Media Player**: Play/pause, next/previous, progress bar
- 🧠 **Smart History Tracking**: Keeps user song history
- 🔐 **Authentication**: Sign up, log in, log out
- 🌐 **Responsive UI** built with HTML/CSS/JavaScript

---

## 📁 Project Structure

```
musa/
│
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates (Jinja2)
├── app/                 # Main Flask application
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── auth.py
│   ├── spotify.py
│   ├── genius.py
│   ├── emotion.py
│   ├── forms.py
├── config.py            # App configuration
├── requirements.txt     # Python dependencies
├── run.py               # App entry point
├── .env                 # Environment variables
└── README.md            # Project documentation
```

---

## 🛠️ Requirements

- Python 3.8+
- Virtual Environment (recommended)

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/linetgitonga/musa.git
cd musa
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_flask_secret_key
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
GENIUS_ACCESS_TOKEN=your_genius_access_token
DATABASE_URL=sqlite:///site.db
```

### 5. Initialize the database

```bash
flask db init
flask db migrate
flask db upgrade
```

---

## ▶️ Running the App

```bash
flask run
```

Then open your browser to:  
📍 http://127.0.0.1:5000

---

## 🧠 How It Works

1. **User signs up and logs in**
2. **Webcam detects user's facial emotion** using OpenCV + TensorFlow
3. **Emotion is mapped to a Spotify genre**
4. **Recommended tracks are fetched via Spotify API**
5. **Lyrics are retrieved from Genius API**
6. **User can play songs, explore folders, and track song history**

---

## 📊 API Endpoints

| Route                  | Description                               |
|------------------------|-------------------------------------------|
| `/`                    | Home Page                                 |
| `/signup`              | User Registration                         |
| `/login`               | User Login                                |
| `/logout`              | User Logout                               |
| `/emotion`             | Emotion Detection via Webcam              |
| `/get_tracks`          | Get Songs by Detected Emotion             |
| `/play_song`           | Play a Specific Song                      |
| `/profile`             | User Profile                              |
| `/history`             | User’s Song History                       |
| `/genres`              | Browse Music Genres                       |
| `/songs_by_genre`      | View Songs by Genre                       |

---

## 🧪 Usage

1. **Sign Up**: Create an account
2. **Log In**: Enter credentials
3. **Detect Emotion**: Grant webcam access
4. **Get Recommendations**: Based on your mood
5. **Play Songs**: Click any song to play
6. **View History**: Track songs you've played

---

## 💻 Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Frontend**: HTML, CSS, JavaScript, Bootstrap/Tailwind
- **ML & CV**: OpenCV, TensorFlow (for emotion recognition)
- **External APIs**:
  - [Spotify Web API](https://developer.spotify.com)
  - [Genius Lyrics API](https://docs.genius.com)

---

## 🎥 Demo

> Watch the app in action:  
> [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🤝 Contributing

Contributions are welcome!  
Please fork the repo, create a feature branch, and submit a pull request.

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature"
git push origin feature/your-feature
```

Or create an issue if you'd like to suggest something or report a bug.

---

## 📝 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 🙏 Acknowledgments

- [Spotify for Developers](https://developer.spotify.com)
- [Genius API](https://genius.com)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [TensorFlow](https://www.tensorflow.org/)

---

## 👩🏽‍💻 Author

**Linet Muthoni Gitonga**  
💌 Email: linetgitonga55@gmail.com  
🔗 GitHub: [@linetgitonga](https://github.com/linetgitonga)  
🔗 LinkedIn: [linkedin.com/in/linetgitonga](https://linkedin.com/in/linet-gitonga-453a54245)

