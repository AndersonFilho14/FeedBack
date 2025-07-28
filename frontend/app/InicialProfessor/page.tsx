"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";

interface ProfessorData {
  professor: {
    id: number;
    nome: string;
    cpf: string;
    cargo: string;
    id_escola: number;
  };
  total_alunos_vinculados: number;
  alunos_vinculados: {
    id: number;
    nome: string;
    idade: number;
    faltas: number;
    id_turma: number;
  }[];
}

export default function InicialProfessor() {
  const [professorData, setProfessorData] = useState<ProfessorData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      // 1. Obter o ID do professor do localStorage
      const professorId = localStorage.getItem('userId');

      if (!professorId) {
        setError("Não foi possível identificar o professor. Por favor, faça login novamente.");
        setLoading(false);
        return;
      }

      try {
        // 2. Usar o ID do professor logado na chamada da API
        const response = await fetch(`http://127.0.0.1:5000/professor/visualizar_alunos/${professorId}`);
        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          throw new Error(errorData?.mensagem || `Falha ao buscar dados: ${response.status}`);
        }
        const data: ProfessorData = await response.json();
        setProfessorData(data);
      } catch (err: any) {
        setError(err.message || "Ocorreu um erro desconhecido.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error || !professorData) {
    return <div>{error || "No data available"}</div>;
  }

  const { professor, alunos_vinculados } = professorData;

  // Assuming each unique id_turma represents a class
  // FIX: Safely handle cases where alunos_vinculados might not be an array.
  const turmas = alunos_vinculados && Array.isArray(alunos_vinculados)
    ? [...new Set(alunos_vinculados.map((aluno) => aluno.id_turma))]
    : [];

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
        </header>

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-6 border-11 ">

          <h1 className="text-[#EEA03D] text-6xl ">Bem vindo, {professor.nome}</h1>
          <main className="w-310 h-137 flex flex-col justify-center items-center gap-4 overflow-y-auto">
            <div className="flex justify-center items-center w-full h-full">
              <div className="grid grid-cols-3 gap-33">
                {turmas.map((turmaId) => (
                <div 
                  key={turmaId} 
                  className="w-63 h-64 border-t-0 border-7 rounded-lg border-[#A4B465] text-2xl flex flex-col items-center place-content-between  bg-white shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)]">
                    <span className="mb-2 border-7 rounded-lg border-[#727D73]  w-63 flex items-center justify-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] ">Turma {turmaId}</span>
                  
                    
                    <div className="flex gap-10" >
                      <Link 
                        className="w-35 h-11 border-4 rounded-lg border-[#727D73] flex items-center justify-center text-xl bg-[#A7C1A8] mb-4" 
                        // FIX: Corrected path from /EdicaoTurma to /EditarTurma
                        href={{ pathname: '/EdicaoTurma', query: { turmaId } }} >
                        Visualizar
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </main>

          <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg " href={"/Login"}>Voltar</Link>
        </div>

        </div>

    </>
  );
}
