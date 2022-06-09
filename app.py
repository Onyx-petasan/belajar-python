#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

#import library flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os
#inisiasi object flask
app = Flask(__name__)

#inisiasi object Flask_restful
api = Api(app)

#inisiasi object flask_cors
CORS(app)

#inisialisasi object flask sqlalchemy
db = SQLAlchemy(app)

#mengkonfigurasu database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# Membuat database model
class ModelDatabase(db.Model):
    
    # membuat field/kolom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    notel = db.Column(db.Integer) # field tambahan
    alamat = db.Column(db.TEXT) # field tambahan

    # membuat mothode untuk menyimpan data agar lebih simple
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# mencreate database
db.create_all()

#inisiasi variabel kosong bertipe dictionary
identitas ={} #variabel global , dictionary = json

#membuat class resource
class ContohResource(Resource):
    #method get dan post
    def get(self):
        # response = kurung kurawal
        # "msg":"Hallo dunia, ini appp restfull ku"
        # kurung kurawal
        return identitas  #response

    def post(self):
        dataNama = request.form["nama"]
        dataEmail = request.form["email"]
        dataNotel = request.form["notel"]
        dataAlamat = request.form["alamat"]

        #masukan data kedalam database model
        model = ModelDatabase(nama=dataNama, email=dataEmail, notel=dataNotel, alamat=dataAlamat)
        model.save()
        
        response = {
            "msg": "Data Berhasil bosku",
            "code": 200
        }
        return response, 200


# setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)