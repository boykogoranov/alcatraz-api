from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route('/api/ping', methods=['GET'])
def ping():
    """
    Pong endpoint
    """
    try:
        hostname = socket.gethostname()
        return jsonify({
            "message": "pong",
            "hostname": hostname
        })
    except Exception as e:
        return jsonify({
            "error": "Failed to get hostname",
            "message": str(e)
        }), 500

@app.route('/', methods=['GET'])
def health_check():
    """
    Basic health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    })

if __name__ == '__main__':
    # SSL certificate paths (will be mounted by Docker)
    cert_file = '/run/secrets/ssl_cert'
    key_file = '/run/secrets/ssl_key'
    
    # Alternative path if using bind mounts instead of secrets
    if not os.path.exists(cert_file):
        cert_file = '/app/certs/cert.pem'
        key_file = '/app/certs/key.pem'
    
    ssl_context = None
    if os.path.exists(cert_file) and os.path.exists(key_file):
        ssl_context = (cert_file, key_file)
        print(f"SSL enabled using certificates from {cert_file}")
    else:
        print("SSL certificates not found, running without SSL")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        ssl_context=ssl_context
    )
