/* eslint-disable @typescript-eslint/no-explicit-any */
import { http } from ".";
import { MateriaAPI, MateriaInfo } from "@/entites/Materia";
import { Materia } from "@/types/Materia";

export const createMateria = (data: Materia) =>
  http.post("/materia", MateriaAPI(data));
export const getMateria = (formData: Record<string, string>) =>
  http.get(`/materia/${formData.id}`).then(({ data }) => MateriaInfo(data));
export const getListMaterias = () =>
  http
    .get(`/materia/`)
    .then(({ data }) => data.escolas.map((data: Materia) => MateriaInfo(data)));
export const editMateria = (formData: Record<string, any>) =>
  http.put(`/materia/${formData.id}`, MateriaAPI(formData));
