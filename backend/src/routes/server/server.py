from flask import Flask

from routes.routes.routes import user_rout_bp

class ManagerFlask:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(blueprint= user_rout_bp)

    def run_flask(self)->None:
        self.app.run()
