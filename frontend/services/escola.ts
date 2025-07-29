/* eslint-disable @typescript-eslint/no-explicit-any */
import { EscolaAPI, EscolaInfo } from "@/entites/Escola";
import { http } from ".";
import { Escola } from "@/types/Escola";

export const createEscola = (data: Escola) =>
  http.post("/escola", EscolaAPI(data));
export const getEscola = (formData: Record<string, string>) =>
  http.get(`/escola/${formData.id}`).then(({ data }) => EscolaInfo(data));
export const getListEscolas = () =>
  http
    .get(`/escola`)
    .then(({ data }) => data.escolas.map((data: Escola) => EscolaInfo(data)));
export const editEscola = (formData: Record<string, any>) =>
  http.put(`/escola/${formData.id}`, EscolaAPI(formData));

export const deleteEscola = (formData: Record<string, any>) =>
  http.delete(`/escola/${formData.id}`);
