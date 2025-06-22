import { AlunoType } from "../types/AlunoType";

export function treatDataExtra(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, extraCurriculares }) => {
    return { id, notaFinal, extraCurriculares };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ extraCurriculares }) => {
    return extraCurriculares == a;
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
        extraCurriculares: a == 1 ? "Foi extraCurriculares" : "Não foi extraCurriculares ",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
