import typer
from pathlib import Path
from utils.file_handler import load_json_file

from crypto.caesar import process_text
from crypto.affine import encrypt_text, decrypt_text
from crypto.hill import hill_cipher
from crypto.playfair import playfair_cipher
from crypto.vigenere import vigenere_cipher

app = typer.Typer(help="Cryptography CLI tool")

@app.command()
def caesar(
    config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    """Run a Caesar cipher using a JSON config file"""

    data = load_json_file(config_path)
    result = process_text(data.get("plain_text"), data.get("offset"), encode=not decrypt)
    typer.secho(f"Result: {result}", fg=typer.colors.GREEN)

@app.command()
def affine(
    config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    """Run an Affine cipher using a JSON config file"""

    data = load_json_file(config_path)

    if not decrypt:
        result = encrypt_text(data.get("plain_text"), data.get("a"), data.get("b"))
    else:
        result = decrypt_text(data.get("plain_text"), data.get("a"), data.get("b"))

    typer.secho("Result: ", fg=typer.colors.GREEN)
    typer.secho(f"{result}", fg=typer.colors.BLUE)

@app.command()
def hill(
    config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    """Run a Hill cipher using a JSON config file"""

    data = load_json_file(config_path)
    result = hill_cipher(data.get("plain_text"), data.get("matrix"), encode=not decrypt)
    typer.secho(f"Result: {result}", fg=typer.colors.GREEN)

@app.command()
def playfair(
    config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    """Run a Playfair cipher using a JSON config file"""

    data = load_json_file(config_path)
    result = playfair_cipher(data.get("plain_text"), data.get("key"), encode=not decrypt)
    typer.secho(f"Result: {result}", fg=typer.colors.GREEN)

@app.command()
def vigenere(
    config_path: Path = typer.Argument(..., help="Path to the JSON config file"),
    decrypt: bool = typer.Option(False, "--decrypt", "-d", help="Decrypt instead of encrypt")
):
    """Run a Vigenere cipher using a JSON config file"""

    data = load_json_file(config_path)
    result = vigenere_cipher(data.get("plain_text"), data.get("key"), encode=not decrypt)
    typer.secho(f"Result: {result}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()