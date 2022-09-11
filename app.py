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
from flask_jwt_extended import create_access_token, get_jwt, JWTManager, jwt_required
import datetime
from operator import attrgetter

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
@jwt_required()
def create_chat():
    now = datetime.datetime.now()
    id_user = str(get_jwt()["id_user"])
    try:
        dt = Data()
        data = request.json

        if "text" not in data:
            return make_response(jsonify({'description': "Data text belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)

        text = data["text"]

        if len(text) == 0:
            return make_response(jsonify({'description': "Pesan yang dikirim kosong, pastikan untuk mengisi chat terlebih dahulu", 'error': "Parameter Error", 'status_code': 400}), 400)

        if "is_group" in data:
            is_group = data["is_group"]
            if str(is_group) == "1":
                if "id_group" not in data:
                    return make_response(jsonify({'description': "Data id_group belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)
                id_group = data["id_group"]
                to_id_user = None

                # check apakah id_group terdaftar
                query_temp2 = "SELECT C.id_group, C.nama_group, M.id_member, M.id_user FROM group_chat C, group_chat_member M WHERE C.id_group = %s AND C.id_group = M.id_group AND M.id_user = %s AND M.is_delete = 0;"
                values_temp2 = (id_group, id_user,)
                data_temp2 = dt.get_data(query_temp2, values_temp2)
                if len(data_temp2) == 0:
                    return make_response(jsonify({'description': "Group yg di tuju belum register", 'error': "Defined Error", 'status_code': 401}), 401)
            else:
                id_group = None

                if "to_id_user" not in data:
                    return make_response(jsonify({'description': "Data to_id_user belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)

                to_id_user = data["to_id_user"]

                # check apakah to_id_user terdaftar
                query_temp = "SELECT id_user FROM user WHERE id_user = %s AND is_delete != 1"
                values_temp = (to_id_user, )
                data_temp = dt.get_data(query_temp, values_temp)
                if len(data_temp) == 0:
                    return make_response(jsonify({'description': "User yg di tuju belum register", 'error': "Defined Error", 'status_code': 401}), 401)
        else:
            if "id_chat" not in data:
                return make_response(jsonify({'description': "Data id_chat belum dimasukkan", 'error': "Parameter Error", 'status_code': 400}), 400)

            id_chat = data["id_chat"]

            # check apakah id_chat terdaftar
            query_temp3 = "SELECT id_chat FROM chat WHERE id_chat = %s AND is_delete != 1"
            values_temp3 = (id_chat, )
            data_temp3 = dt.get_data(query_temp3, values_temp3)
            if len(data_temp3) == 0:
                return make_response(jsonify({'description': "Id_chat yg dituju tidak ada", 'error': "Defined Error", 'status_code': 401}), 401)

            query2 = "INSERT INTO chat_reply (from_id_user, id_chat, text, datetime) VALUES (%s, %s, %s, %s)"
            values2 = (id_user, id_chat, text, now, )
            dt.insert_data(query2, values2)

            hasil = "Create chat sukses"
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)

        # create chat yang bukan reply
        query = "INSERT INTO chat (from_id_user, to_id_user, text, is_group, id_group, datetime) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (id_user, to_id_user, text, is_group, id_group, now, )
        dt.insert_data(query, values)

        hasil = "Create chat sukses"
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)

    except Exception as e:
        print("Error: " + str(e))
        hasil = {  # ini tambahan coba aja
            "status": "gagal login",
            "error": str(e)
        }


@app.route("/get_chat_user", methods=["GET"])
@jwt_required()
def get_chat_user():
    try:
        dt = Data()
        db_id_user = str(get_jwt()["id_user"])

        query_chat = """ SELECT a.* FROM chat a WHERE a.from_id_user = %s OR a.to_id_user = %s AND a.is_delete = 0 """
        values_chat = (db_id_user, db_id_user, )
        data_chat = dt.get_data(query_chat, values_chat)

        id_user = request.args.get("id_user")

        data_array = []
        if id_user:
            for i in range(len(data_chat)):
                if str(data_chat[i]["to_id_user"]) == str(id_user):
                    data_array.append(data_chat[i])
                    id_chat = data_chat[i]["id_chat"]
                    query_chat_reply = "SELECT * FROM chat_reply WHERE id_chat = %s AND is_delete = 0"
                    values_chat_reply = (id_chat, )
                    data_chat_reply = dt.get_data(
                        query_chat_reply, values_chat_reply)
                    if len(data_chat_reply) != 0:
                        for j in range(len(data_chat_reply)):
                            data_array.append(data_chat_reply[j])
                elif str(data_chat[i]["from_id_user"]) == str(id_user):
                    data_array.append(data_chat[i])
                    id_chat = data_chat[i]["id_chat"]
                    query_chat_reply = "SELECT * FROM chat_reply WHERE id_chat = %s AND is_delete = 0"
                    values_chat_reply = (id_chat, )
                    data_chat_reply = dt.get_data(
                        query_chat_reply, values_chat_reply)
                    if len(data_chat_reply) != 0:
                        for j in range(len(data_chat_reply)):
                            data_array.append(data_chat_reply[j])
        else:
            data_array = data_chat

        return make_response(jsonify({'status_code': 200, 'description': data_array}), 200)

    except Exception as e:
        print("Error: " + str(e))
        hasil = {  # ini tambahan coba aja
            "status": "gagal login",
            "error": str(e)
        }


@app.route("/get_chat_filter", methods=["GET"])
@jwt_required()
def get_chat_filter():
    try:
        dt = Data()
        db_id_user = str(get_jwt()["id_user"])

        query_chat = """ SELECT a.* FROM chat a WHERE a.from_id_user = %s OR a.to_id_user = %s AND a.is_delete = 0 ORDER BY a.id_chat DESC """
        values_chat = (db_id_user, db_id_user, )
        data_chat = dt.get_data(query_chat, values_chat)

        return make_response(jsonify({'status_code': 200, 'description': data_chat}), 200)

    except Exception as e:
        print("Error: " + str(e))
        hasil = {  # ini tambahan coba aja
            "status": "gagal login",
            "error": str(e)
        }


if __name__ == "__main__":
    app.run(debug=True)
