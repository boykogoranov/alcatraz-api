from flask import Flask, jsonify
import socket

# Create Flask application
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
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
