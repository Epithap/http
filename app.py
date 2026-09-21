import os
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify
import psycopg2
import boto3

app = Flask(__name__)

# Ambil konfigurasi dari Environment Variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Password123!')
S3_BUCKET = os.getenv('S3_BUCKET', 'lks-app-bucket-unik123')

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Aplikasi Python Flask berjalan di Ubuntu Container!",
        "server": "AWS EC2 Auto Scaling"
    })

@app.route('/db-check')
def db_check():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3
        )
        conn.close()
        return jsonify({"database": "Connected successfully!"})
    except Exception as e:
        return jsonify({"database_error": str(e)}), 500

@app.route('/s3-check')
def s3_check():
    try:
        s3 = boto3.client('s3')
        # Tes list objects di bucket
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        return jsonify({
            "s3_bucket": S3_BUCKET,
            "status": "Accessible",
            "file_count": response.get('KeyCount', 0)
        })
    except Exception as e:
        return jsonify({"s3_error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)