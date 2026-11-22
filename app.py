from flask import Flask, request, jsonify, redirect
from urllib.parse import urlparse
import string
import random
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_code TEXT NOT NULL UNIQUE,
        clicks INTEGER DEFAULT 0
    )
    """)

    # Check if clicks column already exists
    cursor.execute("PRAGMA table_info(urls)")
    columns = [column[1] for column in cursor.fetchall()]

    if "clicks" not in columns:
        cursor.execute("ALTER TABLE urls ADD COLUMN clicks INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

# Generate a random short code
def generate_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

# Validate URL
def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)

@app.route("/")
def home():
    return "URL Shortener Backend is Running!"

# API endpoint to shorten a URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]

    if not isinstance(original_url, str) or not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    while True:
        short_code = generate_code()

        cursor.execute(
            "SELECT short_code FROM urls WHERE short_code = ?",
            (short_code,)
        )

        if cursor.fetchone() is None:
            break

    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "original_url": original_url,
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:5000/{short_code}"
    })

# Redirect to original URL
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    )

    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )

        conn.commit()
        conn.close()

        return redirect(row[0])

    conn.close()
    return jsonify({"error": "URL not found"}), 404

@app.route("/api/urls/<short_code>", methods=["GET"])
def get_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute(
    "SELECT original_url, short_code, clicks FROM urls WHERE short_code = ?",
    (short_code,)
)

    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "original_url": row[0],
            "short_code": row[1],
            "clicks": row[2],
            "short_url": f"http://127.0.0.1:5000/{row[1]}"
        })

    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)