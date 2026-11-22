# URL Shortener Backend

A simple URL Shortener API built with Python, Flask, and SQLite as part of my Backend Development Internship.

## Features

- Shortens long URLs into 6-character codes
- Validates URLs
- Stores URLs in SQLite database
- Redirects short URLs to original URLs
- Retrieves URL information through API
- Tracks the number of clicks

## Technologies Used

- Python
- Flask
- SQLite
- REST API

## Installation

1. Clone the repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd codealpha_URL_shortner
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

The server will run at:

`http://127.0.0.1:5000`

## API Endpoints

### 1. Home

**GET /**

Checks whether the application is running.

### 2. Shorten URL

**POST /shorten**

Request body:

```json
{
  "url": "https://www.google.com"
}
```

### 3. Redirect

**GET /&lt;short_code&gt;**

Redirects the user to the original URL and increases the click count.

### 4. Get URL Information

**GET /api/urls/&lt;short_code&gt;**

Returns the original URL, short code, short URL, and click count.

## Database

SQLite is used to store:

- ID
- Original URL
- Short code
- Click count

## Project Status

Completed as a Backend Development Internship project.