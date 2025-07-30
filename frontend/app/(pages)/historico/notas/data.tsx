import { TableProps } from "antd";

export const columns: TableProps["columns"] = [
  {
    key: "Avaliação",
    title: "Avaliação",
    dataIndex: "tipoAvaliacao",
  },
  {
    key: "dataAvaliacao",
    title: "Dt. Avaliacao",
    dataIndex: "dataAvaliacao",
  },
  {
    key: "nomeAluno",
    title: "Nome do Aluno",
    dataIndex: "nomeAluno",
  },
  {
    key: "nota",
    title: "Nota",
    dataIndex: "nota",
  },
  {
    key: "nomeTurma",
    title: "Nome da Turma",
    dataIndex: "nomeTurma",
  },
  {
    key: "nomeProfessor",
    title: "Nome do Professor",
    dataIndex: "nomeProfessor",
  },
  {
    key: "nomeEscola",
    title: "Nome da Escola",
    dataIndex: "nomeEscola",
  },
];
