export default function convertsToPercentage(data:any[]) {
  const arr = data.map(({ notaFinal, id }) => {
    return { id, notaFinal };
  });

  const countA = arr.filter((e) => {
    return e.notaFinal == "A";
  }).length;

  const countB = arr.filter((e) => {
    return e.notaFinal == "B";
  }).length;

  const countC = arr.filter((e) => {
    return e.notaFinal == "C";
  }).length;

  const countD = arr.filter((e) => {
    return e.notaFinal == "D";
  }).length;

  const countF = arr.filter((e) => {
    return e.notaFinal == "F";
  }).length;

  const countTotal = countA + countB + countC + countD + countF;
  const calcPorcentage = (nota: number) => {
    return (nota * 100) / countTotal;
  };
  let result = [
    { label: "A", value: countA },
    { label: "B", value: countB },
    { label: "C", value: countC },
    { label: "D", value: countD },
    { label: "F", value: countF },
  ];
  
  const teste = result.map(({ label, value }) => {
    return { label, value: Number(calcPorcentage(value).toFixed(2)) };
  });
  return teste
}
