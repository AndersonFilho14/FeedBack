from typing import Optional, List
from typing import Dict
from collections import Counter, defaultdict
from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
    Avaliacao as AvaliacaoData,
    Materia as MateriaData,
    Responsavel as ResponsavelData,
    Escola as EscolaData,
)
from domain.models import Aluno, Responsavel
from datetime import datetime


class ConsultarTurma:
    """Lida com a consulta de um único registro de professor no banco de dados."""

    def __init__(self, id_aluno: int) -> None:
        """Inicializa a classe ConsultarProfessor com o ID do professor."""
        self.__id_aluno = id_aluno

    def __consultar_no_banco(self) -> Optional[int]:
        """Consulta o banco de dados por um professor com o ID fornecido, retornando o objeto ProfessorData ou None."""
        with DBConnectionHandler() as session:
            retorno = (
                session.query(AlunoData)
                .filter(AlunoData.id == self.__id_aluno)
                .first()
            )
        if retorno:
            return retorno.id
        return None

    def get_id_turma(self):
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()
    

class AlunoRepository:
    """Repositório responsável por persistir e consultar dados relacionados alunos."""

    def criar(self, aluno: Aluno, responsavel: Responsavel) -> None:
        """Insere um novo aluno no banco."""
        aluno_orm = AlunoData(
            nome = aluno.nome,
            cpf = aluno.cpf,
            faltas = aluno.faltas,
            nota_score_preditivo = aluno.nota_score_preditivo,
            id_escola = aluno.id_escola,
            data_nascimento = aluno.data_nascimento,
            sexo = aluno.sexo,
            nacionalidade = aluno.nacionalidade,
            id_turma = aluno.id_turma, # Inicializado como 0, será atualizado na função de criação/edição de turmas
            id_responsavel = aluno.id_responsavel,  # Inicializado como 0, será atualizado após a inserção do responsável no banco
            etnia = aluno.etnia,
            educacaoPais = aluno.educacao_pais,
            tempoEstudoSemanal = aluno.tempo_estudo_semanal,
            apoioPais = aluno.apoio_pais,
            aulasParticulares = aluno.aulas_particulares,
            extraCurriculares = aluno.extra_curriculares,
            esportes = aluno.esportes,
            aulaMusica = aluno.aula_musica,
            voluntariado = aluno.voluntariado,
        )

        responsavel_orm = ResponsavelData(
            nome = responsavel.nome,
            telefone = responsavel.telefone
        )

        with DBConnectionHandler() as session:
            # Cadastra o responsável
            session.add(responsavel_orm)
            session.commit()
            session.refresh(responsavel_orm)  # garante que id está atualizado

            # Associa o id dele ao aluno e cadastra o aluno
            aluno_orm.id_responsavel = responsavel_orm.id
            session.add(aluno_orm)
            session.commit()
            session.refresh(aluno_orm)

            # Busca todas as disciplinas
            materias = session.query(MateriaData).all()

            # Para cada matéria, cria 4 avaliações para o novo aluno
            avaliacoes = []
            for materia in materias:
                for tipo in ["1Va", "2Va", "3Va", "4Va"]:
                    avaliacao = AvaliacaoData(
                        tipo_avaliacao=tipo,
                        data_avaliacao=datetime.now(),
                        nota=-1.0,
                        id_aluno=aluno_orm.id,
                        id_materia=materia.id,
                        id_professor=materia.id_professor,
                    )
                    avaliacoes.append(avaliacao)

            session.add_all(avaliacoes)
            session.commit()
    

    def listar_por_escola(self, id_escola: int) -> List[AlunoData]:
        """Retorna lista de alunos filtrados por escola."""
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).filter(AlunoData.id_escola == id_escola).all()
            return alunos
        
    def listar_por_turma(self, id_turma: int) -> List[AlunoData]:
        """Retorna lista de alunos filtrados por turma."""
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).filter(AlunoData.id_turma == id_turma).all()
            return alunos

    def atualizar(
        self,
        id_aluno: int,
        novo_nome: str,
        novo_cpf: str,
        nova_data_nascimento: str,
        novo_sexo: str,
        nova_nacionalidade: str,
        novo_nome_responsavel: str,
        novo_numero_responsavel: str,
        nova_etnia: int,
        nova_educacao_pais: int,
        novo_tempo_estudo_semanal: float,
        novo_apoio_pais: int,
        novas_aulas_particulares: int,
        novas_extra_curriculares: int,
        novos_esportes: int,
        nova_aula_musica: int,
        novo_voluntariado: int
    ) -> bool:
        """Atualiza os dados do aluno com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            aluno = (
                session.query(AlunoData)
                .filter(AlunoData.id == id_aluno)
                .first()
            )
            if not aluno:
                return False

            aluno.nome = novo_nome
            aluno.cpf = novo_cpf
            aluno.data_nascimento = nova_data_nascimento
            aluno.sexo = novo_sexo
            aluno.nacionalidade = nova_nacionalidade
            aluno.etnia = nova_etnia
            aluno.educacaoPais = nova_educacao_pais
            aluno.tempoEstudoSemanal = novo_tempo_estudo_semanal
            aluno.apoioPais = novo_apoio_pais
            aluno.aulasParticulares = novas_aulas_particulares
            aluno.extraCurriculares = novas_extra_curriculares
            aluno.esportes = novos_esportes
            aluno.aulaMusica = nova_aula_musica
            aluno.voluntariado = novo_voluntariado

            # Atualiza o responsável
            responsavel = (
                session.query(ResponsavelData)
                .filter(ResponsavelData.id == aluno.id_responsavel)
                .first()
            )
            if responsavel is not None:
                responsavel.nome = novo_nome_responsavel
                responsavel.telefone = novo_numero_responsavel
            session.commit()
            return True

    def deletar(self, id_aluno: int) -> bool:
        """Deleta o aluno pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            aluno = (
                session.query(AlunoData)
                .filter(AlunoData.id == id_aluno)
                .first()
            )
            if not aluno:
                return False

            # Exclui todas as avaliações associadas ao aluno
            session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno == id_aluno).delete()

            session.delete(aluno)
            session.commit()
            return True
        
class AlunoIARepository:
    """Classe responsável por acessar dados de score preditivo dos alunos."""

    def contar_notas_ia_por_escola(id_escola: int) -> Dict[str, int]:
        """
        Conta quantos alunos possuem cada nota preditiva (A, B, C, D, E, F) para a escola informada.
        Mesmo que uma nota não esteja presente, ela será incluída com valor 0.
        """
        categorias = ["A", "B", "C", "D", "E", "F"]

        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .filter(AlunoData.id_escola == id_escola, AlunoData.nota_score_preditivo != None)
                .all()
            )
            notas = [aluno.nota_score_preditivo for aluno in alunos]
            contagem = dict(Counter(notas))
            return {categoria: contagem.get(categoria, 0) for categoria in categorias}


    def contar_notas_ia_geral() -> Dict[str, int]:
        """
        Conta a distribuição geral das notas preditivas no banco (sem filtro de escola).
        Mesmo que uma nota não esteja presente, ela será incluída com valor 0.
        """
        categorias = ["A", "B", "C", "D", "E", "F"]

        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .filter(AlunoData.nota_score_preditivo != None)
                .all()
            )
            notas = [aluno.nota_score_preditivo for aluno in alunos]
            contagem = dict(Counter(notas))
            return {categoria: contagem.get(categoria, 0) for categoria in categorias}

        
    def contar_notas_ia_por_sexo_escola(id_escola: Optional[int] = None) -> Dict[str, Dict[str, int]]:
        """
        Retorna a contagem de notas IA por sexo, filtrando por escola (se fornecida).
        Mesmo que uma nota não esteja presente, ela será incluída com valor 0.
        """
        categorias = ["A", "B", "C", "D", "E", "F"]

        with DBConnectionHandler() as session:
            query = session.query(AlunoData).filter(AlunoData.nota_score_preditivo != None)

            if id_escola is not None:
                query = query.filter(AlunoData.id_escola == id_escola)

            alunos = query.all()

            distribuicao = defaultdict(list)
            for aluno in alunos:
                if aluno.sexo:
                    distribuicao[aluno.sexo].append(aluno.nota_score_preditivo)

            resultado: Dict[str, Dict[str, int]] = {}
            for sexo, notas in distribuicao.items():
                contagem = dict(Counter(notas))
                resultado[sexo] = {categoria: contagem.get(categoria, 0) for categoria in categorias}

            return resultado

            
    def contar_notas_ia_por_sexo_geral() -> Dict[str, Dict[str, int]]:
        """
        Retorna a contagem de notas IA por sexo em todas as escolas (sem filtro).
        Mesmo que uma nota não esteja presente, ela será incluída com valor 0.
        """
        categorias = ["A", "B", "C", "D", "E", "F"]

        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .filter(AlunoData.nota_score_preditivo != None)
                .all()
            )

            distribuicao = defaultdict(list)
            for aluno in alunos:
                if aluno.sexo:
                    distribuicao[aluno.sexo].append(aluno.nota_score_preditivo)

            resultado: Dict[str, Dict[str, int]] = {}
            for sexo, notas in distribuicao.items():
                contagem = dict(Counter(notas))
                resultado[sexo] = {categoria: contagem.get(categoria, 0) for categoria in categorias}

            return resultado
        
    def contar_alunos_por_esporte_geral() -> Dict[str, int]:
        """
        Conta quantos alunos participam ou não de esportes (sem filtro de escola).

        Exemplo de retorno:
        {
            "Participa": 15,
            "Não participa": 9
        }
        """
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).all()

            contagem = {"Participa": 0, "Não participa": 0}
            for aluno in alunos:
                if aluno.esportes == 1:
                    contagem["Participa"] += 1
                else:
                    contagem["Não participa"] += 1

            return contagem

    def contar_alunos_por_esporte_escola(id_escola: Optional[int] = None) -> Dict[str, int]:
        """
        Conta quantos alunos de uma escola participam ou não de esportes.

        Exemplo de retorno:
        {
            "Participa": 7,
            "Não participa": 3
        }
        """
        with DBConnectionHandler() as session:
            query = session.query(AlunoData)
            if id_escola is not None:
                query = query.filter(AlunoData.id_escola == id_escola)

            alunos = query.all()

            contagem = {"Participa": 0, "Não participa": 0}
            for aluno in alunos:
                if aluno.esportes == 1:
                    contagem["Participa"] += 1
                else:
                    contagem["Não participa"] += 1

            return contagem
        
    def contar_alunos_por_extracurriculares_geral() -> Dict[str, int]:
        """
        Conta quantos alunos fazem ou não fazem aulas extracurriculares (sem filtro de escola).

        Exemplo de retorno:
        {
            "Faz": 12,
            "Não faz": 18
        }
        """
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.extraCurriculares == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem

    def contar_alunos_por_extracurriculares_escola(id_escola: Optional[int] = None) -> Dict[str, int]:
        """
        Conta quantos alunos de uma escola fazem ou não fazem aulas extracurriculares.

        Exemplo de retorno:
        {
            "Faz": 5,
            "Não faz": 7
        }
        """
        with DBConnectionHandler() as session:
            query = session.query(AlunoData)
            if id_escola is not None:
                query = query.filter(AlunoData.id_escola == id_escola)

            alunos = query.all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.extraCurriculares == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem
    
    def contar_alunos_por_aula_musica_geral() -> Dict[str, int]:
        """
        Conta quantos alunos fazem ou não fazem aula de música (sem filtro de escola).

        Exemplo de retorno:
        {
            "Faz": 14,
            "Não faz": 16
        }
        """
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.aulaMusica == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem

    def contar_alunos_por_aula_musica_escola(id_escola: Optional[int] = None) -> Dict[str, int]:
        """
        Conta quantos alunos de uma escola fazem ou não fazem aula de música.

        Exemplo de retorno:
        {
            "Faz": 7,
            "Não faz": 9
        }
        """
        with DBConnectionHandler() as session:
            query = session.query(AlunoData)
            if id_escola is not None:
                query = query.filter(AlunoData.id_escola == id_escola)

            alunos = query.all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.aulaMusica == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem

    def contar_alunos_por_aulas_particulares_geral() -> Dict[str, int]:
        """
        Conta quantos alunos fazem ou não fazem aulas particulares (sem filtro de escola).

        Exemplo de retorno:
        {
            "Faz": 12,
            "Não faz": 18
        }
        """
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.aulasParticulares == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem

    def contar_alunos_por_aulas_particulares_escola(id_escola: Optional[int] = None) -> Dict[str, int]:
        """
        Conta quantos alunos de uma escola fazem ou não fazem aulas particulares.

        Exemplo de retorno:
        {
            "Faz": 5,
            "Não faz": 11
        }
        """
        with DBConnectionHandler() as session:
            query = session.query(AlunoData)
            if id_escola is not None:
                query = query.filter(AlunoData.id_escola == id_escola)

            alunos = query.all()

            contagem = {"Faz": 0, "Não faz": 0}
            for aluno in alunos:
                if aluno.aulasParticulares == 1:
                    contagem["Faz"] += 1
                else:
                    contagem["Não faz"] += 1

            return contagem


class ConsultaDadosAluno:
    """Consulta dados relacionados ao aluno: responsável, turma e escola."""

    def __init__(self, id_aluno: int):
        self.id_aluno = id_aluno

    def nome_responsavel(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_responsavel:
                responsavel = session.query(ResponsavelData).filter(ResponsavelData.id == aluno.id_responsavel).first()
                if responsavel:
                    return responsavel.nome
            return None

    def nome_turma(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_turma:
                turma = session.query(TurmaData).filter(TurmaData.id == aluno.id_turma).first()
                if turma:
                    return turma.nome
            return None

    def nome_escola(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_escola:
                escola = session.query(EscolaData).filter(EscolaData.id == aluno.id_escola).first()
                if escola:
                    return escola.nome
            return None
        
    def numero_responsavel(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_responsavel:
                responsavel = session.query(ResponsavelData).filter(ResponsavelData.id == aluno.id_responsavel).first()
                if responsavel:
                    return responsavel.telefone
            return None

class ConsultaAlunoBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_aluno_por_id(self, id_aluno: int) -> Optional[AlunoData]:
        """Busca um aluno pelo ID. Retorna o objeto AlunoData se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(AlunoData).filter_by(id=id_aluno).first()


    def buscar_por_cpf(self, cpf: str) -> Optional[AlunoData]:
        """Busca um aluno pelo CPF. Retorna o objeto AlunoData se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(AlunoData).filter_by(cpf=cpf).first()
        
    def buscar_por_cpf_e_id(self, cpf: str, id: int) -> bool:
        """Verifica se o CPF já está cadastrado em outro professor com ID diferente, e retorna um booleano com base nisso.."""
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter_by(cpf=cpf).first()
            return aluno is not None and aluno.id != id