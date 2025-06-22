from config.logger import log

from routes import ManagerFlask
from infra import DBConnectionHandler

if __name__ == "__main__":
    DBConnectionHandler()
    log.info("Iniciando projeto")
    ManagerFlask().run_flask()
    log.info("Fim do projeto")
