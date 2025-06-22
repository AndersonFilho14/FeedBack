import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });

const desempenho = {
  async listar() {
    return api
      .get("")
      .then(({ data }) => data)
      .catch(() => {
        console.log("Error em listar");
      });
  },
  async criar(aluno: any) {
    api
      .post("", aluno)
      .then((data) => data)
      .catch(() => {
        console.log("Error em criar");
      });
  },
  async encontrar(id?: number | string | string[]) {
    return await api
      .get(`/${id}`)
      .then(({data}) => data)
      .catch(() => {
        console.log("Error em encontrar");
      });
  },
};
export default desempenho;
