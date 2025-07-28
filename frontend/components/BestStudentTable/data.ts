import { TableProps } from "antd";

export const columns: TableProps["columns"] = [
  {
    title: "Media",
    dataIndex: "media",
    key: "media",
  },
  {
    title: "Nome",
    dataIndex: "nome_aluno",
    key: "nome_aluno",
  },
  {
    title: "qtd. Avaliações",
    dataIndex: "quantidade_avaliacoes",
    key: "quantidade_avaliacoes",
  },
  {
    title: "Escola",
    dataIndex: "nome_escola",
    key: "nome_escola",
  },
  {
    title: "Turma",
    dataIndex: "nome_turma",
    key: "nome_turma",
  },
];
