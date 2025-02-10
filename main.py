import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_cors import CORS
import random

# Load the .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        """Method for converting a sqlalchemy object into dict format"""
        # Empty dictionary
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2 using dictionary comprehension
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    # Convert this random_cafe object into dictionary
    return jsonify(cafe=random_cafe.to_dict())
    # return jsonify(cafe={"id": random_cafe.id,
    #                      "name": random_cafe.name,
    #                      "map_url": random_cafe.map_url,
    #                      "img_url": random_cafe.img_url,
    #                      "location": random_cafe.location,
    #                      "seats": random_cafe.seats,
    #                      "has_toilet": random_cafe.has_toilet,
    #                      "has_wifi": random_cafe.has_wifi,
    #                      "has_sockets": random_cafe.has_sockets,
    #                      "can_take_calls": random_cafe.can_take_calls,
    #                      "coffee_price": random_cafe.coffee_price
    #                      })


@app.route("/all")
def get_all_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    cafe_data_list = []  # Empty list
    for cafe in all_cafes:  # Loop through all_cafes list
        cafe_data = cafe.to_dict()  # Covert every cafe object into dictionary
        cafe_data_list.append(cafe_data)  # append the converted dict to empty list
    return jsonify(cafes=cafe_data_list)  # return all the data using jsonify
    # alternative solution, using list comprehension.
    # return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


# search?loc=Peckham
@app.route("/search")
def search_cafe():
    query_location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # There is more than 1 cafe in 1 location.
    all_cafes = result.scalars().all()
    if all_cafes:  # if all cafe is true
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])  # List comprehension
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get('name'),
        id=request.form.get('id'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('loc'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('toilet')),
        has_wifi=bool(request.form.get('wifi')),
        has_sockets=bool(request.form.get('sockets')),
        can_take_calls=bool(request.form.get('calls')),
        coffee_price=request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_data = db.session.get(Cafe, cafe_id)  # This will get the cafe data using id.
    new_price = request.args.get('new_price')
    if cafe_data:
        cafe_data.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get('api-key')
    if api_key == API_KEY:  # if api key is correct get the cafe data that will be deleted.
        cafe_data = db.session.get(Cafe, cafe_id)  # This will get the cafe data using id.
        if cafe_data:  # if cafe data is true.
            db.session.delete(cafe_data)
            db.session.commit()
            # successful
            return jsonify(response={"success": "Successfully deleted the cafe."})
        # else 404
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    # else 403
    return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=False)
