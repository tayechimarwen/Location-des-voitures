from flask import Flask
from flask_cors import CORS
from models import db
from routes import voitures_bp,locataires_bp,locations_bp

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location_voitures.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)  
app.register_blueprint(voitures_bp)
app.register_blueprint(locataires_bp)
app.register_blueprint(locations_bp)



# Create database tables
with app.app_context():
    db.create_all()
    print("✅ Database created successfully!")

# Test route
@app.route('/')
def home():
    return {'message': 'Backend is running! 🚀'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
