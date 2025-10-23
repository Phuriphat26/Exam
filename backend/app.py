from flask import Flask
from flask_cors import CORS
from api.signup import register_bp
from api.login import login_bp
from api.planner import planner_bp
from api.profile import profile_bp
from api.subject import subject_bp
#from api.exam_plan import exam_plan_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'


CORS(app, supports_credentials=True, origins=['http://localhost:5173'])  # React port


app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(planner_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(subject_bp)
#app.register_blueprint(exam_plan_bp)
if __name__ == "__main__":
    app.run(port=5000, debug=True)
from flask import Flask, session, jsonify
from flask_cors import CORS



@app.route("/check")
def check():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session.get("username")})
    return jsonify({"logged_in": False})
##fg
