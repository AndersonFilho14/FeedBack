import { AlunoType } from "../types/AlunoType";

export function treatDataEsport(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, esportes }) => {
    return { id, notaFinal, esportes };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ esportes }) => {
    return esportes == a;
    });
    const countA = data.filter((e) => {
      return e.notaFinal == "A";
    }).length;
    const countB = data.filter((e) => {
      return e.notaFinal == "B";
    }).length;

    const countC = data.filter((e) => {
      return e.notaFinal == "C";
    }).length;

    const countD = data.filter((e) => {
      return e.notaFinal == "D";
    }).length;

    const countF = data.filter((e) => {
      return e.notaFinal == "F";
    }).length;


    return [
      {
        A: countA,
        B: countB,
        C: countC,
        D: countD,
        F: countF,
        esportes: a == 1 ? "Pratica esportes" : "Não pratica",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
