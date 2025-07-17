from flask import Flask
from flask_cors import CORS  # Adicione este import

from routes.routes.routes import user_rout_bp

class ManagerFlask:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # Habilita CORS para todas as rotas
        self.app.register_blueprint(blueprint=user_rout_bp)

    def run_flask(self) -> None:
        self.app.run()