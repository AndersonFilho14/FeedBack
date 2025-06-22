import { AlunoType } from "../types/AlunoType";

export function treatDataMusic(data: AlunoType[]) {
  let arr = data.map(({ notaFinal, id, aulaMusica }) => {
    return { id, notaFinal, aulaMusica };
  });

  const ForM = (a: number) => {
    let data = arr.filter(({ aulaMusica }) => {
    return aulaMusica == a;
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
        aulaMusica: a == 1 ? "Sem aula de música" : "Com aula de música",
      },
    ];
  }
    return[...ForM(0), ...ForM(1)]
}
