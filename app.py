import json
import re
import os
import datetime
from flask import Flask, render_template, request, url_for, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from util import levenshtein, valid_plate_num, get_time_stamp
from flask_swagger_ui import get_swaggerui_blueprint


# app and db configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "German Number Plates"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT)


# routes and api methods
@app.route('/plate', methods=["GET", "POST"])
def plate():
    if request.method == "POST":
        plate_num = request.json.get("plate")
        if not plate_num:
            return Response(f"Not a valid request/plate field not found", status=400)
        if valid_plate_num(plate_num):
            try:
                num_plate = NumberPlate.query.filter_by(plate_num=plate_num).first()
                if num_plate:
                    num_plate.created_at = datetime.datetime.utcnow()
                else:
                    num_plate = NumberPlate(plate_num=plate_num)
                db.session.add(num_plate)
                db.session.commit()
            except Exception as error:
                print(error)
                return Response(f"Oops something went wrong", status=500)
            timestamp = get_time_stamp(num_plate.created_at)
            r_json = json.dumps({"plate": num_plate.plate_num, "timestamp": timestamp})
            return Response(r_json, status=200, mimetype='application/json')
        else:
            return Response(f"Not a valid Plate Number", status=422)
    elif request.method == "GET":
        r_dict = {"plates": []}
        try:
            plates = NumberPlate.query.all()
        except Exception as error:
            print(error)
            return Response(f"Oops something went wrong", status=500)
        for plate in plates:
            t_dict = {"plate": plate.plate_num}
            # created_date = plate.created_at
            t_dict["timestamp"] = get_time_stamp(plate.created_at)
            r_dict["plates"].append(t_dict)
        r_json = json.dumps(r_dict)
        return Response(r_json, status=200, mimetype='application/json')


@app.route('/search-plate', methods=["GET"])
def search_plate():
    if request.method == "GET":
        search_key = request.args.get("key","")
        distance = request.args.get("levenshtein", "0")
        if search_key and distance.isnumeric():
            try:
                plates = NumberPlate.query.all()
            except Exception as error:
                print(error)
                return Response(f"Oops something went wrong", status=500)
            valid_plates = []
            for plate in plates:
                plate_num = "".join(plate.plate_num.split("-"))
                if levenshtein(search_key.upper(), plate_num.upper()) <= int(distance):
                    created_at = plate.created_at
                    time_stamp = created_at.strftime("%Y-%m-%d") + "T" + created_at.strftime("%H:%M:%S") + "Z"
                    valid_plates.append({'plate' : plate_num, "timestamp": time_stamp })
            r_json = json.dumps({f"{search_key.upper()}": valid_plates})
            return Response(r_json, status=200, mimetype='application/json')
        else:
            return Response(f"Given search-key format or distance format is Incorrect", status=400)


# db models
class NumberPlate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_num = db.Column(db.String(10), nullable=False)
    # to be reviewed for timezone
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<NumberPlate: {self.plate_num}>'


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

