class Responsavel:
    def __init__(
        self,
        id: int,
        nome: str,
        telefone: str
    ) -> None:
        """
        Modelo de domínio para um responsável pelo aluno.

        :param id: Identificador único do responsável.
        :param nome: Nome completo do responsável.
        :param telefone: Telefone de contato do responsável.
        :raises ValueError: Se algum campo for inválido.
        """

        if not isinstance(id, int):
            raise ValueError("O ID deve ser um número inteiro.")
        if not isinstance(nome, str):
            raise ValueError("O nome deve ser uma string.")
        if telefone is not None and not isinstance(telefone, str):
            raise ValueError("O telefone deve ser uma string ou None.")

        self.id = id
        self.nome = nome
        self.telefone = telefone

    def __repr__(self) -> str:
        return f"<Responsavel id={self.id} nome={self.nome} telefone={self.telefone}>"
