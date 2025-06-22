import { AlunoType } from "../types/AlunoType";

export function treatDataForM(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, sexo }) => {
    return { id, notaFinal, sexo };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ sexo }) => {
    return sexo == a;
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
        sexo: a == 1 ? "Feminino" : "Masculino",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
