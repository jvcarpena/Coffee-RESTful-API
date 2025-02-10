# Flask RESTful API – Cafe Finder ☕  

A RESTful API built with Flask and SQLAlchemy to manage cafes, allowing users to retrieve, add, update, and delete cafes.  

## Features  
- Get a random cafe: `GET /random`  
- Get all cafes: `GET /all`  
- Search cafes by location: `GET /search?loc=<location>`  
- Add a new cafe: `POST /add`  
- Update cafe price: `PATCH /update-price/<cafe_id>?new_price=<price>`  
- Delete a cafe (API key required): `DELETE /report-closed/<cafe_id>?api-key=<API_KEY>`  

## Setup  
1. Clone the repo:  
   ```sh
   git clone https://github.com/your-repo.git
   cd your-project
   ```  
2. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```  
3. Set environment variables (`.env` file):  
   ```
   API_KEY=your_api_key
   DB_URI=your_database_uri
   ```  
4. Run the app:  
   ```sh
   python app.py
   ```  

## Tech Stack  
- Flask, Flask-SQLAlchemy, Flask-CORS  
- SQLite/PostgreSQL  
- RESTful API principles  

