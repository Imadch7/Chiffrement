import typer
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_handler import load_json_file, save_to_json_file

from crypto.caesar import caesar_cipher
from crypto.affine import affine_encrypt, affine_decrypt
from crypto.hill import hill_cipher
from crypto.playfair import playfair_cipher
from crypto.vigenere import vigenere_cipher
from crypto.otp import otp_encode, otp_decode

app = Flask(__name__)
CORS(app)

users = dict()
mailbox = dict()

@app.route("/encrypt/<cipher_type>", methods=["POST"])
def encrypt_route(cipher_type: str):
    data = request.json
    message = data.get("message")
    key = data.get("key")
    encode = data.get("encode")

    if cipher_type == "caesar":
        result = caesar_cipher(message, key, encode)

    elif cipher_type == "affine":
        a = data.get("a")
        b = data.get("b")
        if encode:
            result = affine_encrypt(message, a, b)
        else:
            result = affine_decrypt(message, a, b)

    elif cipher_type == "hill":
        result = hill_cipher(message, key, encode)

    elif cipher_type == "playfair":
        result = playfair_cipher(message, key, encode)

    elif cipher_type == "vigenere":
        result = vigenere_cipher(message, key, encode)

    elif cipher_type == "otp":
        if encode:
            result = otp_encode(message)
        else:
            result = otp_decode(message)

    return jsonify({"cipherType": cipher_type, result: result})

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    to_user = data.get("to_user")

    mailbox[to_user].append({
        "from": data.get("from"),
        "cipher": data.get("cipher"),
        "cipherText": data.get("cipherText")
    })

    return jsonify({"message": "sent"}), 200

# @app.command()
# def caesar(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run a Caesar cipher using a JSON config file, and save the result to a output/caesar_res.json file"""

#     data = load_json_file(config_path)
#     text = caesar_cipher(data.get("text"), data.get("key"), encode=not decrypt)
#     typer.secho("Result: ", fg=typer.colors.GREEN)
#     typer.secho(f"{text}", fg=typer.colors.BLUE)
#     save_to_json_file("output/caesar_res.json", { "date": datetime.now(), "text": text })

# @app.command()
# def affine(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run an Affine cipher using a JSON config file, and save the result to a output/affine_res.json file"""

#     data = load_json_file(config_path)

#     if not decrypt:
#         text = affine_encrypt(data.get("text"), data.get("a"), data.get("b"))
#     else:
#         text = affine_decrypt(data.get("text"), data.get("a"), data.get("b"))

#     save_to_json_file("output/affine_res.json", { "date": datetime.now(), "text": text })
#     typer.secho("Result: ", fg=typer.colors.GREEN)
#     typer.secho(f"{text}", fg=typer.colors.BLUE)

# @app.command()
# def hill(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run a Hill cipher using a JSON config file, and save the result to a output/hill_res.json file"""

#     data = load_json_file(config_path)
#     text = hill_cipher(data.get("text"), data.get("matrix"), encode=not decrypt)
#     save_to_json_file("output/affine_res.json", { "date": datetime.now(), "text": text })
#     typer.secho("Result: ", fg=typer.colors.GREEN)
#     typer.secho(f"{text}", fg=typer.colors.BLUE)

# @app.command()
# def playfair(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run a Playfair cipher using a JSON config file, and save the result to a output/playfair_res.json file"""

#     data = load_json_file(config_path)
#     text = playfair_cipher(data.get("text"), data.get("key"), encode=not decrypt)
#     save_to_json_file("output/affine_res.json", { "date": datetime.now(), "text": text })
#     typer.secho("Result: ", fg=typer.colors.GREEN)
#     typer.secho(f"{text}", fg=typer.colors.BLUE)

# @app.command()
# def vigenere(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run a Vigenere cipher using a JSON config file, and save the result to a output/vigenere_res.json file"""

#     data = load_json_file(config_path)
#     text = vigenere_cipher(data.get("text"), data.get("key"), encode=not decrypt)
#     save_to_json_file("output/affine_res.json", { "date": datetime.now(), "text": text })
#     typer.secho("Result: ", fg=typer.colors.GREEN)
#     typer.secho(f"{text}", fg=typer.colors.BLUE)

# @app.command()
# def otp(
#     config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
#     decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
# ):
#     """Run an OTP cipher using a JSON config file, and save the result to a output/vigenere_res.json file"""

#     data = load_json_file(config_path)

#     if not decrypt:
#         result, key = otp_encode(data.get("text"))
#         save_to_json_file("output/otp_text.json", { "text": result, "pad": key })
#     else:
#         result = otp_decode(data.get("text"), data.get("pad"))
#         save_to_json_file("output/otp_dec.json", { "text": result })

#     typer.secho("Result is: ", fg=typer.colors.GREEN)
#     typer.secho(f"{result}", fg=typer.colors.BLUE)

if __name__ == "__main__":
    app.run(debug=True, port=5000)