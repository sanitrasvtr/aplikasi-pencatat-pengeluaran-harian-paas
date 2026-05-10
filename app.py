from flask import Flask, jsonify, request

app = Flask(__name__)

pengeluaran = []

@app.route('/')
def home():
    return jsonify({
        'pesan': 'Aplikasi Pencatat Pengeluaran Harian',
        'status': 'aktif'
    })

@app.route('/pengeluaran', methods=['GET'])
def get_pengeluaran():
    return jsonify(pengeluaran)

@app.route('/tambah', methods=['POST'])
def tambah_pengeluaran():
    data = request.json
    pengeluaran.append(data)

    return jsonify({
        'pesan': 'Pengeluaran berhasil ditambahkan',
        'data': data
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'sehat'
    })

if __name__ == '__main__':
    app.run(debug=True)