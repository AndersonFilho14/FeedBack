from datetime import date
from typing import Optional

class Aluno:
    def __init__(
        self,
        id: int,
        nome: str,
        data_nascimento: date,
        sexo: str,
        cpf: str,
        nacionalidade: str,
        faltas: int,
        nota_score_preditivo: str,
        id_escola: int,
        etnia: int,
        educacao_pais: int = None,
        tempo_estudo_semanal: float = None,
        apoio_pais: int = None,
        aulas_particulares: int = None,
        extra_curriculares: int = None,
        esportes: int = None,
        aula_musica: int = None,
        voluntariado: int = None,
        id_turma:  Optional[int] = None,
        id_responsavel: Optional[int] = None,
        

    ) -> None:
        """Model de aluno com validações de tipo."""

        for item in [id, faltas, id_escola]:
            if not isinstance(item, int):
                raise ValueError("Valor inválido: esperado inteiro")

        for item in [nome, cpf, sexo, nacionalidade]:
            if not isinstance(item, str):
                raise ValueError("Valor inválido: esperado string")

        if not isinstance(data_nascimento, date):
            raise ValueError("data_nascimento deve ser um objeto do tipo `date`")

        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.cpf = cpf
        self.nacionalidade = nacionalidade
        self.faltas = faltas
        self.nota_score_preditivo = nota_score_preditivo
        self.id_escola = id_escola
        self.id_turma = id_turma
        self.id_responsavel = id_responsavel
        self.etnia = etnia
        self.educacao_pais = educacao_pais
        self.tempo_estudo_semanal = tempo_estudo_semanal
        self.apoio_pais = apoio_pais
        self.aulas_particulares = aulas_particulares
        self.extra_curriculares = extra_curriculares
        self.esportes = esportes
        self.aula_musica = aula_musica
        self.voluntariado = voluntariado

    def __repr__(self):
        return (
            f"<Aluno id={self.id} | nome={self.nome} | cpf={self.cpf}"
            f"| faltas={self.faltas} | nota_score_preditivo={self.nota_score_preditivo} "
            f"| id_escola={self.id_escola} | id_turma={self.id_turma} | id_responsavel={self.id_responsavel} "
            f"| data_nascimento={self.data_nascimento} | sexo={self.sexo} | nacionalidade={self.nacionalidade} "
            f"| etnia={self.etnia} | educacao_pais={self.educacao_pais} | tempo_estudo_semanal={self.tempo_estudo_semanal} "
            f"| apoio_pais={self.apoio_pais} | aulas_particulares={self.aulas_particulares} | extra_curriculares={self.extra_curriculares} "
            f"| esportes={self.esportes} | aula_musica={self.aula_musica} | voluntariado={self.voluntariado} "
        )
