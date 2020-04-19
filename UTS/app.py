from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/helloworld')

class Mhs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique=True)
    nama = db.Column(db.String(100))
    alamat= db.Column(db.Text)

    def __init__(self, nim, nama, alamat):
        self.nim = nim
        self.nama = nama
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mhs.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nim', 'nama', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/mahasiswa', methods=['POST'])
def add_user():
    nim = request.json['nim']
    nama = request.json['nama']
    alamat = request.json['alamat']

    new_mhs = Mhs(nim, nama, alamat)

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
  alamat = request.json['alamat']

  mahasiswa.nim = nim
  mahasiswa.nama = nama
  mahasiswa.alamat = alamat

  db.session.commit()

  return user_schema.jsonify(mahasiswa)

@app.route('/mahasiswa/<id>', methods=['DELETE'])
def delete_product(id):
  mahasiswa = Mhs.query.get(id)
  db.session.delete(mahasiswa)
  db.session.commit()

  return user_schema.jsonify(mahasiswa)


if __name__ == '__main__':
    app.run()