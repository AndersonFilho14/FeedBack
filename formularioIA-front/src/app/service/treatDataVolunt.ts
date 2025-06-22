import { AlunoType } from "../types/AlunoType";

export function treatDataVolunt(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, voluntariado }) => {
    return { id, notaFinal, voluntariado };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ voluntariado }) => {
    return voluntariado == a;
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
        voluntariado: a == 1 ? "Foi voluntariado" : "Não foi voluntariado ",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
