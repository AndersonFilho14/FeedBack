/* eslint-disable @typescript-eslint/no-explicit-any */
import { HistoricoInfo } from "@/entites/Historico";
import { http } from ".";

export const getHistoricoNotasList = (formData: any) =>
  http
    .get(`/historico/avaliacoes/escola/${formData.id}`)
    .then(({ data }) => data.avaliacoes.map((data: any) => HistoricoInfo(data)));
