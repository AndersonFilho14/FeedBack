import { TableProps } from "antd";

export const columns: TableProps["columns"] = [
  {
    key: "nome",
    title: "Nome",
    dataIndex: "nome",
  },
  {
    key: "idMunicipio",
    title: "Cod. Municipio",
    dataIndex: "idMunicipio",
  },
  {
    key: "nomeUsuario",
    title: "Usuario",
    dataIndex: "nomeUsuario",
  },
];
