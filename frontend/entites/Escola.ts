/* eslint-disable @typescript-eslint/no-explicit-any */
import { Escola } from "@/types/Escola";

export const EscolaAPI = ({ nome, idMunicipio, nomeUsuario, senha }: any) => ({
  nome: nome,
  id_municipio: idMunicipio,
  nome_usuario: nomeUsuario,
  senha: senha,
});

export const EscolaInfo = (data: any): Escola => ({
  id: data.id,
  nome: data.nome,
  idMunicipio: data.id_municipio,
  nomeUsuario: data.nome_usuario,
  senha: data.senha,
});
