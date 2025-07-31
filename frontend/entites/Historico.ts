/* eslint-disable @typescript-eslint/no-explicit-any */
export const HistoricoInfo = (data: any) => ({
  tipoAvaliacao: data.tipo_avaliacao,
  dataAvaliacao: data.data_avaliacao,
  nota: data.nota,
  idAluno: data.id_aluno,
  nomeAluno: data.nome_aluno,
  nomeProfessor: data.nome_professor,
  nomeMateria: data.nome_materia,
  nomeTurma: data.nome_turma,
  nomeEscola: data.nome_escola,
});
