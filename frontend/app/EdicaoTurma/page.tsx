"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from 'next/navigation';

export default function EdicaoTurma() {
  const searchParams = useSearchParams();
  const turmaId = searchParams.get('turmaId');
  const [turma, setTurma] = useState<string | null>(null);

  useEffect(() => {
    if (turmaId) {
      setTurma(`Turma ${turmaId}`);
    }
  }, [turmaId]);

  
  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>
      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-330 h-200  rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22  border-11 ">
          <h1 className="text-[#EEA03D] text-6xl mb-4">{turma || "Selecione uma Turma"}</h1>

          <main className="w-126 h-120 border-5 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-10 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)]" >
            <Link className="w-80 h-24 border-5 rounded-lg border-[#A4B465] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl" href={`/CadastrarPresenca?turmaId=${turmaId}`}>Gerenciar Faltas</Link>
            <Link className="w-80 h-24 border-5 rounded-lg border-[#EEA03D] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl" href={`/CadastrarNotas?turmaId=${turmaId}`}>Cadastrar Notas</Link>
            <Link 
              className="w-80 h-24 border-5 rounded-lg border-[#A4B465] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl" 
              href={{ pathname: '/VisualizarAlunos', query: { turmaId } }}>Visualizar Alunos
            </Link>
          </main>
          <Link className=" w-44 h-13 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl mt-16" href={"/InicialProfessor"}>Voltar</Link>
        </div>

      </div>

    </>
  );
}
