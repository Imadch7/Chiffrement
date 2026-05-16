import os
import sys
import importlib.util
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper function to load modules from directories with spaces
def load_module_from_path(module_name, file_path):
    if not os.path.exists(file_path):
        return None
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sym_dir = os.path.join(base_dir, 'Symmetric_Encryption')
asym_dir = os.path.join(base_dir, 'Asymmetric_Encryption')

# Load the available algorithms
aes_mod = load_module_from_path('aes_mod', os.path.join(sym_dir, 'aes.py'))
sha256_mod = load_module_from_path('sha256_mod', os.path.join(sym_dir, 'sha256_encryption.py'))
md5_mod = load_module_from_path('md5_mod', os.path.join(sym_dir, 'md5_encryption.py'))
rsa_pss_mod = load_module_from_path('rsa_pss_mod', os.path.join(asym_dir, 'rsa_pss.py'))
e0_mod = load_module_from_path('e0_mod', os.path.join(sym_dir, 'bluetooth_e0.py'))
rc4_mod = load_module_from_path('rc4_mod', os.path.join(sym_dir, 'rc4.py'))
vig_mod = load_module_from_path('vig_mod', os.path.join(sym_dir, 'vigenere.py'))
cesar_mod = load_module_from_path('cesar_mod', os.path.join(sym_dir, 'cesar.py'))
des_mod = load_module_from_path('des_mod', os.path.join(sym_dir, 'des.py'))
affine_mod = load_module_from_path('affine_mod', os.path.join(sym_dir, 'affine.py'))
hill_mod = load_module_from_path('hill_mod', os.path.join(sym_dir, 'hill.py'))
dh_mod = load_module_from_path('dh_mod', os.path.join(asym_dir, 'diffie_hellman.py'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def process_data():
    try:
        data = request.json
        input_text = data.get('input', '')
        operations = data.get('operations', [])
        
        current_data = input_text
        
        for op in operations:
            op_name = op.get('name')
            
            if op_name == 'SHA-256':
                if sha256_mod:
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    current_data = sha256_mod.sha256(current_data)
                else:
                    return jsonify({'error': 'SHA-256 module not loaded'}), 500
                    
            elif op_name == 'MD5':
                if md5_mod:
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    current_data = md5_mod.md5(current_data)
                else:
                    return jsonify({'error': 'MD5 module not loaded'}), 500
                    
            elif op_name == 'AES Encrypt':
                if aes_mod:
                    aes_instance = aes_mod.AES()
                    # AES requires 16 byte key
                    key = op.get('key', 'defaultkey123456')
                    if len(key) < 16:
                        key = key + '0' * (16 - len(key))
                    key = key[:16].encode()
                    
                    if isinstance(current_data, str):
                        try:
                            current_data = bytes.fromhex(current_data)
                        except ValueError:
                            current_data = current_data.encode()
                        
                    encrypted_bytes = aes_instance.aes_encrypt(current_data, key)
                    current_data = encrypted_bytes
                else:
                    return jsonify({'error': 'AES module not loaded'}), 500
                    
            elif op_name == 'Bluetooth E0':
                if e0_mod:
                    key_hex = op.get('key', '00112233445566778899aabbccddeeff')
                    if not key_hex:
                        key_hex = '00112233445566778899aabbccddeeff'
                    try:
                        key_int = int(key_hex, 16)
                    except ValueError:
                        return jsonify({'error': 'Bluetooth E0 key must be valid hex'}), 400
                        
                    e0 = e0_mod.E0Cipher(key_int)
                    if isinstance(current_data, str):
                        try:
                            # Try hex decode first if it looks like hex from a previous step
                            current_data = bytes.fromhex(current_data)
                        except ValueError:
                            current_data = current_data.encode()
                            
                    processed = e0.crypt(current_data)
                    current_data = processed
                else:
                    return jsonify({'error': 'Bluetooth E0 module not loaded'}), 500
                    
            elif op_name == 'RC4 Encrypt':
                if rc4_mod:
                    rc4_instance = rc4_mod.RC4()
                    key_str = op.get('key', 'secret')
                    if not key_str:
                        key_str = 'secret'
                    key = key_str.encode()
                    if isinstance(current_data, str):
                        try:
                            current_data = bytes.fromhex(current_data)
                        except ValueError:
                            current_data = current_data.encode()
                    current_data = rc4_instance.rc4_encrypt(current_data, key)
                else:
                    return jsonify({'error': 'RC4 module not loaded'}), 500
                    
            elif op_name == 'Vigenere':
                if vig_mod:
                    key = op.get('key', 'key')
                    if not key:
                        key = 'key'
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    current_data = vig_mod.VigenereCipher.cipher_vigenere(current_data, key)
                else:
                    return jsonify({'error': 'Vigenere module not loaded'}), 500
                    
            elif op_name == 'Cesar':
                if cesar_mod:
                    try:
                        shift = int(op.get('shift', '3'))
                    except ValueError:
                        shift = 3
                    cesar_inst = cesar_mod.Cesar(shift)
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    current_data = cesar_inst.encrypt(current_data)
                else:
                    return jsonify({'error': 'Cesar module not loaded'}), 500
                    
            elif op_name == 'Affine':
                if affine_mod:
                    try:
                        a = int(op.get('a', '5'))
                        b = int(op.get('b', '8'))
                    except ValueError:
                        a, b = 5, 8
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    current_data = affine_mod.Affine.cipher_affine(current_data, a, b)
                else:
                    return jsonify({'error': 'Affine module not loaded'}), 500
                    
            elif op_name == 'Hill':
                if hill_mod:
                    try:
                        k11 = int(op.get('k11', '3'))
                        k12 = int(op.get('k12', '3'))
                        k21 = int(op.get('k21', '2'))
                        k22 = int(op.get('k22', '5'))
                    except ValueError:
                        k11, k12, k21, k22 = 3, 3, 2, 5
                    key_matrix = [[k11, k12], [k21, k22]]
                    
                    if isinstance(current_data, bytes):
                        current_data = current_data.decode(errors='ignore')
                    # Hill cipher needs even length plaintext and only alphabetic characters
                    current_data = ''.join(filter(str.isalpha, current_data)).lower()
                    if not current_data:
                        current_data = 'xx'
                    if len(current_data) % 2 != 0:
                        current_data += 'x'
                    current_data = hill_mod.HillCipher.Hill_cipher(current_data, key_matrix)
                else:
                    return jsonify({'error': 'Hill module not loaded'}), 500
                    
            elif op_name == 'DES Encrypt':
                if des_mod:
                    des_inst = des_mod.DES()
                    key = op.get('key', '12345678')
                    if not key:
                        key = '12345678'
                    if len(key) < 8:
                        key = key + '0' * (8 - len(key))
                    key = key[:8].encode()
                    
                    if isinstance(current_data, str):
                        try:
                            current_data = bytes.fromhex(current_data)
                        except ValueError:
                            current_data = current_data.encode()
                    binary_str = des_inst.des_encrypt(current_data, key)
                    b_arr = bytearray()
                    for i in range(0, len(binary_str), 8):
                        b_arr.append(int(binary_str[i:i+8].ljust(8, '0'), 2))
                    current_data = bytes(b_arr)
                else:
                    return jsonify({'error': 'DES module not loaded'}), 500
                    
            elif op_name == 'RSA-PSS Sign':
                if rsa_pss_mod:
                    # Generate a 512-bit key for demonstration speed
                    public, private = rsa_pss_mod.generate_keypair(512)
                    if isinstance(current_data, str):
                        current_data = current_data.encode()
                    signature = rsa_pss_mod.rsa_pss_sign(current_data, private)
                    
                    out = f"--- RSA-PSS Signature ---\n"
                    out += f"Message: {current_data.decode(errors='ignore')}\n\n"
                    out += f"Signature (int):\n{signature}\n\n"
                    out += f"Public Key (e, n):\n{public}"
                    current_data = out
                else:
                    return jsonify({'error': 'RSA-PSS module not loaded'}), 500
                    
            elif op_name == 'Diffie-Hellman':
                if dh_mod:
                    alice = dh_mod.DiffieHellman(bits=128)
                    bob = dh_mod.DiffieHellman(p=alice.p, g=alice.g)
                    alice_shared = alice.generate_shared_secret(bob.public_key)
                    bob_shared = bob.generate_shared_secret(alice.public_key)
                    
                    out = f"--- Diffie-Hellman Exchange ---\n"
                    out += f"Prime (p): {alice.p}\nBase (g): {alice.g}\n\n"
                    out += f"Alice Private Key: {alice.private_key}\nAlice Public Key: {alice.public_key}\n\n"
                    out += f"Bob Private Key: {bob.private_key}\nBob Public Key: {bob.public_key}\n\n"
                    out += f"Alice computed Shared Secret: {alice_shared}\n"
                    out += f"Bob computed Shared Secret:   {bob_shared}\n"
                    out += f"Match: {alice_shared == bob_shared}\n\n"
                    if current_data:
                        out += f"Original Input preserved:\n{current_data}"
                    current_data = out
                else:
                    return jsonify({'error': 'Diffie-Hellman module not loaded'}), 500
            
            else:
                return jsonify({'error': f'Unsupported operation: {op_name}'}), 400
                
        if isinstance(current_data, bytes):
            current_data = current_data.hex()
            
        return jsonify({
            'success': True,
            'output': current_data
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
