from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_restful.representations import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# ini adalah pertemuan 3
@app.route('/')
def hello_world():
    return 'Selamat datang'


@app.route('/admin/')
def admin_page():
    return 'Ini adalah halaman admin'


# materi pertemuan 3 berakhir di sini


# ini adalah materi pertemuan 4
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/helloworld')

# materi pertemuan 4 berakhir di sini
# # ini adalamat materi pertemuan 5
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     @staticmethod
#     def get_all_users():
#         return User.query.all()
#
#
# class UserSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('username', 'email')
#
#
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)
#
#
# @app.route("/user", methods=["GET","POST"])
# def get_user():
#     all_users = User.get_all_users()
#     result = users_schema.dump(all_users)
#     return jsonify(result)
# # materi pertemuan 5 berakhir di sini
#awal  pertemuan 6
class Mhs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True)
    nama = db.Column(db.String(20))
    kelas = db.Column(db.String(20))
    alamat= db.Column(db.String(20))

    def __init__(self, nim, nama, kelas, alamat):
        self.nim = nim
        self.nama = nama
        self.kelas = kelas
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mhs.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'nama', 'kelas', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/mahasiswa', methods=['POST'])
def add_user():
    nim = request.json['nim']
    nama = request.json['nama']
    kelas = request.json['kelas']
    alamat = request.json['alamat']

    new_mhs = Mhs(nim, nama, kelas, alamat)

    db.session.add(new_mhs)
    db.session.commit()

    return user_schema.jsonify(new_mhs)

@app.route('/mahasiswa', methods=['GET'])
def get_users():
    all_users = Mhs.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/mahasiswa/<id>', methods=['GET'])
def get_user(id):
  mahasiswa = Mhs.query.get(id)
  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<id>', methods=['PUT'])
def update_user(id):
  mahasiswa = Mhs.query.get(id)

  nim = request.json['nim']
  nama = request.json['nama']
  kelas = request.json['kelas']
  alamat = request.json['alamat']

  mahasiswa.nim = nim
  mahasiswa.nama = nama
  mahasiswa.kelas = kelas
  mahasiswa.alamat = alamat

  db.session.commit()

  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<id>', methods=['DELETE'])
def delete_product(id):
  mahasiswa = Mhs.query.get(id)
  db.session.delete(mahasiswa)
  db.session.commit()

  return user_schema.jsonify(mahasiswa)
# materi pertemuan 6 berakhir di sini
if __name__ == '__main__':
    app.run()
