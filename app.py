from flask import Flask
from flask_cors import CORS
from routes.auth import auth_bp
from routes.profile import profile_bp
from routes.predict import predict_bp

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = "your_super_secret_key"

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(profile_bp, url_prefix="/profile")
app.register_blueprint(predict_bp, url_prefix="/predict")

if __name__ == "__main__":
    app.run(debug=True)
