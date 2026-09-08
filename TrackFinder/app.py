from flask import Flask, render_template

app = Flask(__name__)

site_name = "Track Finder"
tracks = [ 
    {"name": "Mount Eden Loop", "length": 2.0, "grade": "Easy"},
    {"name": "Coast to Coast Walkway", "length": 16.0, "grade": "Medium"},
    {"name": "Karekare Falls", "length": 3.5, "grade": "Easy"},
    {"name": "Hillary Trail", "length": 70.0, "grade": "Hard"}
]

@app.route("/")
def home():
    return render_template("home.html", site_name=site_name, count=len(tracks))

@app.route("/tracks")
def tracks_page():
    return render_template("tracks.html", site_name=site_name, tracks=tracks)

@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)