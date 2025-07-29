/* eslint-disable @typescript-eslint/no-explicit-any */

export const MateriaAPI = ({ nome, idDisciplina, idProfessor }: any) => ({
  nome: nome,
  id_disciplina: idDisciplina,
  id_professor: idProfessor,
});

export const MateriaInfo = (data: any) => ({
  id: data.id,
  nome: data.nome,
  idDisciplina: data.id_disciplina,
  idProfessor: data.id_professor,
});
