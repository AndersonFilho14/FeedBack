"use client";
import React,{useState} from "react";
import Link from "next/link";


export default function EditarNotas() {
    
    const [aluno, setAluno] = useState("Aluno");
    const [notas, setNotas] = useState("Notas");
    const [avaliacao, setAvaliacao] = useState("Avaliação");
    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-6 border-11 ">
                     <h1 className="text-[#EEA03D] text-6xl ">{avaliacao}</h1>
                    <main className="w-310 h-137 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-65 overflow-y-auto">
                        {Array.from({ length: 8 }).map((_, idx) => (
                            <div
                                key={idx}
                                className="w-229 min-h-20  border-7 rounded-lg border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2"
                            >
                                {aluno}
                                <div className="flex gap-4">
                                    <input
                                        className="w-18 h-12 bg-[#A7C1A8] border-5 rounded-lg border-[#EEA03D]"
                                        name={`nota-${idx}`}
                                        type="text"
                                    />
                                </div>
                            </div>
                        ))}
                    </main>
                    <Link className="w-100 h-19 border-5 rounded-lg border-[#7e8855] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl" href={""}>Salvar</Link>
                    <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg " href={"/CadastrarNotas"}>Voltar</Link>
                </div>
                
            </div>

        </>
    );
}
