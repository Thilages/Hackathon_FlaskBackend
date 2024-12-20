from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from firebase_admin import credentials, auth, initialize_app
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

problems = {
    "Mental Health": {
        "title": "Mental Health",
        "description": "Develop an AI-based chatbot to offer mental health support and guidance for users.",
        "details": "This project involves creating an AI-driven chatbot designed to assist users with mental health "
                   "support. The chatbot should provide a safe, empathetic environment where users can share their "
                   "concerns. The system must be able to analyze conversations and provide helpful responses to "
                   "support mental wellness.",
        "scenario": "As mental health issues continue to rise globally, there's a need for digital tools that offer "
                    "psychological support. This project will allow users to interact with an intelligent chatbot "
                    "that can provide both emotional and practical assistance.",
        "expectedStack": ["Python", "TensorFlow", "Flask", "Dialogflow", "Firebase"],
        "pdfUrl": "https://example.com/mental_health.pdf",
    },
    "Fitness App": {
        "title": "Fitness App",
        "description": "Create an app that uses machine learning to track and optimize daily fitness goals.",
        "details": "This project focuses on developing a mobile fitness app that utilizes machine learning to provide "
                   "personalized workout recommendations based on user goals and progress. The app will collect data "
                   "from wearable devices and track physical activities.",
        "scenario": "With increasing health consciousness, people are looking for apps that help them track their "
                    "fitness progress, monitor their health metrics, and get customized workout suggestions.",
        "expectedStack": ["Python", "Keras", "Flask", "TensorFlow", "React Native", "Firebase"],
        "pdfUrl": "https://example.com/fitness_app.pdf",
    },
    "Finance Tool": {
        "title": "Finance Tool",
        "description": "Design a tool to automate personal finance management with AI-driven insights.",
        "details": "This project aims to create a tool that automates personal finance management using AI to analyze spending patterns, suggest savings plans, and provide financial insights.",
        "scenario": "Many individuals struggle with managing their finances. This tool will use AI to analyze users' spending habits and offer suggestions to improve their financial health.",
        "expectedStack": ["Python", "Flask", "TensorFlow", "React", "Firebase"],
        "pdfUrl": "https://example.com/finance_tool.pdf",
    },
    "Carbon Footprint": {
        "title": "Carbon Footprint",
        "description": "Develop an app to help users track and reduce their carbon footprint with actionable insights.",
        "details": "This project involves building an app that tracks the user's daily activities, calculates the associated carbon footprint, and offers tips for reducing it, such as energy-saving recommendations or sustainable travel options.",
        "scenario": "With climate change becoming a critical issue, individuals are increasingly looking for ways to reduce their environmental impact. This app will encourage users to make greener choices in their everyday life.",
        "expectedStack": ["Python", "Flask", "React", "Machine Learning", "Firebase"],
        "pdfUrl": "https://example.com/carbon_footprint.pdf",
    },
    "Energy Monitoring": {
        "title": "Energy Monitoring",
        "description": "Design an automated system that monitors and reduces energy consumption in homes and offices.",
        "details": "This system will provide real-time monitoring of energy consumption in households and office environments, using IoT devices to gather data and machine learning algorithms to suggest energy-saving tips.",
        "scenario": "As energy prices rise and sustainability becomes more important, this system will help individuals and organizations optimize their energy usage and reduce costs.",
        "expectedStack": ["Python", "Flask", "IoT", "Machine Learning", "React"],
        "pdfUrl": "https://example.com/energy_monitoring.pdf",
    },
    "Sustainable Farming": {
        "title": "Sustainable Farming",
        "description": "Create a platform for sustainable farming practices to help farmers improve productivity and reduce waste.",
        "details": "This project will provide a platform to offer sustainable farming tips, crop management systems, and real-time data analytics to help farmers reduce waste and increase efficiency in their farming practices.",
        "scenario": "Farmers are constantly looking for ways to increase productivity while minimizing environmental impact. This platform will assist them in adopting sustainable methods to enhance their farming processes.",
        "expectedStack": ["Python", "Flask", "Data Analytics", "React", "Machine Learning"],
        "pdfUrl": "https://example.com/sustainable_farming.pdf",
    },
    "Telemedicine App": {
        "title": "Telemedicine App",
        "description": "Build a telemedicine platform for remote health consultations and medical services.",
        "details": "This platform will connect patients with doctors for online consultations, offering features such as video calls, medical records management, and AI-driven diagnosis support.",
        "scenario": "With the rise of digital health services, this app will help provide accessible healthcare to remote and underserved areas, improving the reach of medical services globally.",
        "expectedStack": ["Python", "Flask", "React Native", "Firebase", "Twilio API"],
        "pdfUrl": "https://example.com/telemedicine_app.pdf",
    },
    "Fitness Recommendations": {
        "title": "Fitness Recommendations",
        "description": "Create a fitness app that offers personalized workout plans based on AI-driven data analysis.",
        "details": "This app will analyze the user's health data and provide personalized workout plans and nutrition recommendations tailored to their fitness goals, tracking their progress over time.",
        "scenario": "People looking to get in shape often struggle to find personalized fitness plans that suit their unique needs. This app will offer customized recommendations to help users achieve their fitness goals.",
        "expectedStack": ["Python", "Keras", "Flask", "React Native", "Firebase"],
        "pdfUrl": "https://example.com/fitness_recommendations.pdf",
    },
    "Mental Wellness": {
        "title": "Mental Wellness",
        "description": "Develop an app that helps users track their mood and mental well-being with real-time analytics.",
        "details": "This app will allow users to log their mood, track changes in their mental health over time, and provide insights based on machine learning algorithms to improve mental well-being.",
        "scenario": "With growing awareness of mental health, this app will help users better understand their emotional state and provide actionable insights to improve their mental wellness.",
        "expectedStack": ["Python", "TensorFlow", "Flask", "React", "Firebase"],
        "pdfUrl": "https://example.com/mental_wellness.pdf",
    }
}

cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

cred = credentials.Certificate(cred_path)  # Replace with your Firebase Admin SDK key
initialize_app(cred)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, unique=True)
    leader_name = db.Column(db.String(100), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)
    problem_statement = db.Column(db.String(200), nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    email1 = db.Column(db.String(100), nullable=False)
    email2 = db.Column(db.String(100), nullable=False)
    phone1 = db.Column(db.String(15), nullable=False)
    phone2 = db.Column(db.String(15), nullable=False)
    document_link = db.Column(db.String(500), nullable=False)
    video_link = db.Column(db.String(500), nullable=False)


def setup_database():
    with app.app_context():
        db.create_all()


def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = request.headers.get('Authorization')
        if not id_token:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            decoded_token = auth.verify_id_token(id_token.split('Bearer ')[-1])
            request.user_id = decoded_token['uid']
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route('/submit', methods=['POST'])
@firebase_auth_required
def submit_application():
    data = request.json
    print(request.json)

    existing_application = Application.query.filter_by(user_id=request.user_id).first()
    existing_teamname = Application.query.filter_by(team_name=data["team_name"]).first()

    if existing_application:
        return jsonify({"error": "You have already submitted the application form."}), 400
    if existing_teamname:
        return jsonify({"error": f"Team with the same name have already register."}), 400

    required_fields = [
        'leader_name', 'team_name', 'problem_statement', 'team_size',
        'email1', 'email2', 'phone1', 'phone2', 'document_link', 'video_link'
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required."}), 400

    try:
        new_application = Application(
            user_id=request.user_id,
            leader_name=data['leader_name'],
            team_name=data['team_name'],
            problem_statement=data['problem_statement'],
            team_size=data['team_size'],
            email1=data['email1'],
            email2=data['email2'],
            phone1=data['phone1'],
            phone2=data['phone2'],
            document_link=data['document_link'],
            video_link=data['video_link']
        )
        db.session.add(new_application)
        db.session.commit()
        return jsonify({"message": "Application submitted successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/problems/<title>', methods=['GET'])
@firebase_auth_required
def get_problem_details(title):
    print("works")
    # current_user = get_jwt_identity()  # Get user from JWT token
    if title in problems:
        print(problems[title])
        return jsonify(problems[title])
    else:
        return jsonify({"message": "Problem not found"}), 404


if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
