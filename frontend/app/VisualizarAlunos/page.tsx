"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

interface Aluno {
    id: number;
    nome: string;
    idade: number;
    faltas: number;
    id_turma: number;
}

export default function VisualizarAlunos() {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [professor, setProfessor] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const turmaId = searchParams.get("turmaId");

  useEffect(() => {
    if (turmaId) {
      const fetchData = async () => {
        try{
          setLoading(true);
          const response = await fetch(`http://127.0.0.1:5000/professor/visualizar_alunos/1`);
          if (!response.ok) {
            throw new Error("Failed to fetch alunos");
          }
          const data = await response.json();
          if(data && data.alunos_vinculados){
              const alunosDaTurma = data.alunos_vinculados.filter((aluno: Aluno) => aluno.id_turma === parseInt(turmaId));
              setAlunos(alunosDaTurma);
              setProfessor(data.professor.nome);
          } else {
            throw new Error("Dados de alunos não encontrados");
          }
        }catch (err) {
          setError("Error fetching alunos");
          console.error(err);
        } finally {
          setLoading(false);
        }
      }
      fetchData(); 
    }else{
      setError("Turma não especificada");
      setLoading(false);
    }
  }, [turmaId]);
  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>
      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-6 border-11 ">
          <h1 className="text-[#EEA03D] text-6xl ">Lista de Alunos - {professor}</h1>
          {loading ? (
            <div>Loading...</div>
          ) : error ? (
            <div>{error}</div>
          ) : (
            <main className="w-310 h-137 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-10  overflow-y-auto">
              {alunos.map((aluno) => (
                <div key={aluno.id} className=" w-229 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                  {aluno.nome} 
                </div>
              ))}
            </main>
          )}
          <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg " href={`/EdicaoTurma?turmaId=${turmaId}`}>Voltar</Link>
        </div>
      </div>
    </>
  );
}
