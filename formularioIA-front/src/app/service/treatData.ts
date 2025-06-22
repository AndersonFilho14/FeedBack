import { AlunoType } from "../types/AlunoType";

export function treatData(data:AlunoType[]) {
    let arr = data.map(({sexo, notaFinal})=>{
        return {sexo, notaFinal}
    })
    return arr
}