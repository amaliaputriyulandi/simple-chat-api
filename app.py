from crypt import methods
from multiprocessing.sharedctypes import Value
from os import access
from flask import Flask, jsonify, request, make_response
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
from flask_cors import CORS
import config as CFG
import hashlib
from data import Data
from flask_jwt_extended import create_access_token, get_jwt, JWTManager
import datetime

# Create an instance of Flask
app = Flask(__name__)
CORS(app)

# Create an instance of Flask RESTful API
api = Api(app)

# Flask JWT Extended Configuration
app.config['SECRET_KEY'] = CFG.JWT_SECRET_KEY
app.config['JWT_HEADER_TYPE'] = CFG.JWT_HEADER_TYPE
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
    days=2)  # 2 hari token JWT expired
jwt = JWTManager(app)


# region ================================= API WELCOME ===============================================================
@app.route('/', methods=['GET'])
def default():
    response = {"status": "sudah masuk"}
    return jsonify(response)

# endregion ================================= API WELCOME ===============================================================


# region ================================= API USER ===============================================================
@app.route('/register_user', methods=['POST'])
def register_user():
    hasil = {"status": "gagal insert data siswa"}

    try:
        data = request.json

        if "username" not in data:
            return make_response(jsonify({'description': "Data username belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)
        if "no_hp" not in data:
            return make_response(jsonify({'description': "Data no_hp belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)
        if "password" not in data:
            return make_response(jsonify({'description': "Data password belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)

        username = data["username"]
        no_hp = data["no_hp"]
        password = data["password"]

        # check apakah data no_hp sebelumnya sudah di register

        pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()

        dt = Data()
        query = "INSERT INTO user(username, no_hp, password) VALUES(%s,%s,%s)"
        values = (username, no_hp, pass_ency,)
        dt.insert_data(query, values)
        hasil = jsonify(
            {'description': "Data user berhasil di register", 'status_code': 200})
        hasil.status_code = 200

    except Exception as e:
        print("Error: " + str(e))
        hasil = {
            "status": "gagal insert data siswa",
            "error": str(e)
        }

    return hasil


@app.route('/get_user', methods=['GET'])
def get_user():

    dt = Data()
    query = "SELECT * FROM user"
    values = ()

    username = request.args.get("username")
    no_hp = request.args.get("nomor_hp")

    if username:
        query += " AND username=%s "
        values += (username,)
    if no_hp:
        query += " AND no_hp LIKE %s "
        values += ("%"+no_hp+"%", )

    data = dt.get_data(query, values)
    return make_response(jsonify(data), 200)

# region ================================= LOGIN USER ===============================================================


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if "no_hp" not in data:
            return make_response(jsonify({'description': "Data no_hp belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)
        if "password" not in data:
            return make_response(jsonify({'description': "Data password belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)

        no_hp = data["no_hp"]
        password = data["password"]

        pass_enc = hashlib.md5(password.encode('utf-8')).hexdigest()

        # check
        query = """ SELECT id_user, password, no_hp, username FROM user WHERE no_hp = %s AND is_delete = 0 """
        values = (no_hp, )
        dt = Data()
        data_user = dt.get_data(query, values)
        if len(data_user) == 0:
            return make_response(jsonify({'description': "Nomer Hp belum di register", 'error': "Defined Error", 'status_code': 401}), 401)
        data_user = data_user[0]
        db_id_user = data_user["id_user"]
        db_username = data_user["username"]
        db_password = data_user["password"]
        db_no_hp = data_user["no_hp"]

        if pass_enc != db_password:
            return make_response(jsonify({'description': "Password salah", 'error': "Defined Error", 'status_code': 401}), 401)

        jwt_payload = {
            "id_user": db_id_user,
        }

        access_token = create_access_token(
            db_username, additional_claims=jwt_payload)

        return jsonify(access_token=access_token)

    except Exception as e:
        print("Error: " + str(e))
        hasil = {  # ini tambahan coba aja
            "status": "gagal login",
            "error": str(e)
        }

# region ================================= CHAT ===============================================================


@app.route("/create_chat", methods=["POST"])
def create_chat():
    try:
        data = request.json
    except Exception as e:
        print("Error: " + str(e))
        hasil = {  # ini tambahan coba aja
            "status": "gagal login",
            "error": str(e)
        }


if __name__ == "__main__":
    app.run(debug=True)
