# URL Shortener

A simple URL shortening service built with Flask, Postgres, and a modern HTML/JavaScript frontend. It generates unique short codes using a salted hash approach, supports dark mode, and includes a placeholder for advertisements.

## Features

- Shorten long URLs into 6-character codes (e.g., yourdomain.com/aB7kP9).
- Responsive design with light/dark mode toggle.
- Basic input validation and SQL injection protection.
- Placeholder for a 728x90 leaderboard advertisement.

## Prerequisites

- Python 3.11 (or compatible version)
- Conda (for virtual environment management)
- PostgreSQL (local database for testing)
- Git (for version control)
- Heroku CLI (for deployment)

## Running Locally

### 1. Clone the Repository

Clone the repo with: git clone https://github.com/jherberg462/url-shorten-servicer.git  
Then navigate into the directory: cd url-shorten-service

### 2. Set Up Conda Environment

Create the environment: conda create -n url-shortener-env python=3.11  
Activate it: conda activate url-shortener-env  
Install dependencies: conda install flask gunicorn psycopg2 -c conda-forge

### 3. Install Dependencies

The requirements.txt file lists dependencies for Heroku, but Conda handles them locally:  
- Flask  
- Gunicorn  
- Psycopg2-binary  

### 4. Set Up Local PostgreSQL

Install Postgres (e.g., via Homebrew on macOS): brew install postgresql  
Start the service: brew services start postgresql  
Create a database: createdb url_shortener  
Optional - create a user (default postgres works if no password is set):  
- Connect: psql -U postgres  
- Run: CREATE USER url_shortener_user WITH PASSWORD 'your_secure_password';  
- Grant access: GRANT ALL PRIVILEGES ON DATABASE url_shortener TO url_shortener_user;  
- Exit: \q  

### 5. Configure Database URL

Set the DATABASE_URL environment variable: export DATABASE_URL="postgresql://postgres@localhost/url_shortener"  
Adjust with your username/password if needed, e.g., postgresql://url_shortener_user:your_secure_password@localhost/url_shortener

### 6. Run the Application

Start the app: python app.py  
Visit http://127.0.0.1:5000 in your browser.  
Test shortening a URL and toggling dark mode.

## Deploying to Heroku

### 1. Set Up Heroku

Install the Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli  
Log in: heroku login

### 2. Create a Heroku App

Create the app: heroku create your-app-name

### 3. Add Postgres Add-on

Add the free Postgres tier: heroku addons:create heroku-postgresql:hobby-dev -a your-app-name  
This sets the DATABASE_URL environment variable automatically.

### 4. Deploy the Code

Ensure your Git repo is up-to-date:  
- Stage changes: git add .  
- Commit: git commit -m "Prepare for Heroku deployment"  
- Push to GitHub: git push origin main  
Deploy to Heroku: git push heroku main

### 5. Test the Deployment

Open the app: heroku open -a your-app-name  
The app should be live at https://your-app-name.herokuapp.com

## Advertisement Placeholder

This project includes a placeholder for a 728x90 leaderboard advertisement, located below the URL shortening form and result. It’s styled as a gray box in light mode and a darker box in dark mode, with the text "Advertisement (728x90)". To replace it with a real ad (e.g., Google AdSense), update the <div class="ad-leaderboard"> in templates/index.html with the appropriate ad script or iframe.

## Project Structure

- url-shortener/  
  - app.py             # Flask application  
  - requirements.txt   # Dependencies for Heroku  
  - Procfile           # Heroku process definition  
  - static/            # Static assets  
    - script.js        # JavaScript for copy and dark mode  
    - style.css        # CSS styling  
  - templates/         # HTML templates  
    - index.html       # Main page  
  - .gitignore         # Git ignore file  
  - README.md          # This file  

## Notes

- Local testing requires a running Postgres instance; Heroku handles this automatically.  
- The short code generation uses a salted MD5 hash with base-62 encoding.  
- Contributions or issues? Open a pull request or issue on GitHub!

---
Built with ❤️ by Jeremiah