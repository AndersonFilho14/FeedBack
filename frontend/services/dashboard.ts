import { http } from ".";

export const getDSMunicipio = (formData: Record<string, string>) =>
  http.get(`/dashboard/municipio/${formData.id}`);

export const getDSEscola = (formData: Record<string,string>) =>
  http.get(`/dashboard/escola/${formData.id}`);