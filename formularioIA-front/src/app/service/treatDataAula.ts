import { AlunoType } from "../types/AlunoType";

export function treatDataAula(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, aulasParticulares }) => {
    return { id, notaFinal, aulasParticulares };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ aulasParticulares }) => {
    return aulasParticulares == a;
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
        aulasParticulares: a == 1 ? "Foi aulasParticulares" : "Não foi aulasParticulares ",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
