import os
import sys

from loguru import logger
from loguru._logger import Logger


class LogHandler:
    """Manipula o gerenciamento de logs"""
    def __init__(
        self
    ):
        """Inicia o LogHandler com as configurações padrão."""
        self.log_file = "./log/app.log"
        self.log_level_file = "TRACE"
        self.log_level_cmd = "INFO"
        self.rotation_file = "10 MB"
        self.retention_file = "1 year"
        self.colorize = False
        self.backtrace_file = True
        self.backtrace_cmd = False

    def configure_level(self, **kwargs):
        """Permite modificar os níveis de log tanto do arquivo quanto do cmd.
        os parâmetros de kwargs podem ser: file, cmd
        """
        LEVELS_ACCEPTED = [
            'TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'
        ]

        if 'file' in kwargs:
            level = kwargs['file'].upper()
            if level in LEVELS_ACCEPTED:
                self.log_level_file = level
            else:
                raise ValueError(f"Os parâmetros aceitos para log são: {LEVELS_ACCEPTED}")

        if 'cmd' in kwargs:
            level = kwargs['cmd'].upper()
            if level in LEVELS_ACCEPTED:
                self.log_level_cmd = level
            else:
                raise ValueError(f"Os parâmetros aceitos para log são: {LEVELS_ACCEPTED}")

    def configure_file(self, **kwargs):
        """Permite a configuração do arquivo .log
        Manipula os parametros:

            * path [str]: Caminho do arquivo .log. Default: log/app.log
            * rotation [str]: Tempo que o arquivo vai ser rotacionado. Default: 10 MB
            * retention [str]: por quanto tempo os arquivos devem ser mantidos. Default: 1 year
        """
        if 'path' in kwargs:
            self.log_file = kwargs["path"]

        if 'rotation' in kwargs:
            self.rotation_file = kwargs["rotation"]

        if 'retention' in kwargs:
            self.retention_file = kwargs["retention"]

    def configure_log_display(self, **kwargs):
        """Configura pametros relacionados a exibição de logs

            * colorize [bool]: configura a exibição ou não de cores nos logs. Default: True
            * backtrace_file [bool]: configura a
            * backtrace_cmd [bool]: configura a
        """
        if 'colorize' in kwargs:
            self.colorize = kwargs["colorize"]

        if 'backtrace_file' in kwargs:
            self.backtrace_file = kwargs["backtrace_file"]

        if 'backtrace_cmd' in kwargs:
            self.backtrace_cmd = kwargs["backtrace_cmd"]

    def start(self):
        """Inicia a geração de logs
        """
        logger.remove()  # Remove handlers antigos

        # Cria diretório se não existir
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Adiciona handler para arquivo
        logger.add(
            self.log_file,
            level=self.log_level_file,
            format="{level: <8} | {time:DD/MM/YYYY HH:mm:ss} | {elapsed} | {file: >20}:{line: <5} | {module: >20}.{function: <20} | {message}",
            rotation=self.rotation_file,
            retention=self.retention_file,
            backtrace=self.backtrace_file,
            compression="zip",
        )

        # Adiciona handler para terminal
        logger.add(
            sys.stderr,
            level=self.log_level_cmd,
            colorize=self.colorize,
            backtrace=self.backtrace_cmd,
            format="<lg>{time:DD/MM/YYYY HH:mm:ss}</lg> | <le><bold>{file}:{line} {module}.{function}</bold></le> | <y>{elapsed}</y> | <level>{level}</level> | {message}",
        )

    def get_logger(self) -> Logger:
        """Inicializa o logger se ainda não estiver iniciado e retorna a instância do logger.
        :return: A instância do logger.
        :rtype: logger
        """
        self.start()
        return logger
