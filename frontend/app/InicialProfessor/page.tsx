"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

// A interface permanece a mesma, pois representa o caso ideal
interface ProfessorDashboardData {
  id: number;
  nome: string;
  cpf: string;
  cargo: string;
  id_escola: number;
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
  const [dashboardData, setDashboardData] = useState<ProfessorDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleLogout = () => {
    try {
      localStorage.removeItem('userId');
      // O Link já fará o redirecionamento para /Login
    } catch (e) {
      console.error("Erro ao fazer logout (limpar armazenamento local):", e);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      // Usando um try/catch no localStorage para evitar erros no lado do servidor, embora o useEffect já ajude
      let professorId;
      try {
        professorId = localStorage.getItem('userId');
      } catch (e) {
        setError("Erro ao acessar o armazenamento local.");
        setLoading(false);
        return;
      }

      if (!professorId) {
        setError("Não foi possível identificar o professor. Por favor, faça login novamente.");
        setLoading(false);
        return;
      }

      try {
        const response = await fetch(`http://127.0.0.1:5000/professor/visualizar_alunos/${professorId}`);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ mensagem: "Erro desconhecido no servidor." }));
          throw new Error(errorData.mensagem || `Falha ao buscar dados: ${response.status}`);
        }
        const data: ProfessorDashboardData = await response.json();
        setDashboardData(data);
      } catch (err: any) {
        setError(err.message);
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center min-h-screen">Carregando...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center min-h-screen text-red-500">{error}</div>;
  }
  
  const alunos = dashboardData?.alunos_vinculados ?? [];
  const turmas = [...new Set(alunos.map((aluno) => aluno.id_turma))];

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>
      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center h-screen">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto h-auto p-10 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center mt-22 gap-6 border-11">
       
          <h1 className="text-[#EEA03D] text-6xl ">Bem-vindo(a), {dashboardData?.nome ?? 'Professor(a)'}</h1>
          
          <main className="w-full max-w-4xl h-auto flex flex-col justify-center items-center gap-4">
            <div className="flex justify-center items-center w-full h-full">
              <div className="flex flex-wrap justify-center gap-8">
                {turmas.length > 0 ? (
                  turmas.map((turmaId) => (
                    <div
                      key={turmaId}
                      className="w-64 h-64 rounded-xl border-4 border-[#A4B465] bg-white shadow-lg flex flex-col justify-between items-center p-4 transition-transform hover:scale-105"
                    >
                      <span className="text-2xl font-semibold text-[#4A5A4F] border-2 border-[#727D73] rounded-md px-4 py-2 shadow-md">
                        Turma {turmaId}
                      </span>
                      <div className="flex gap-4">
                        <Link
                          href={{ pathname: '/EdicaoTurma', query: { turmaId: turmaId.toString() } }}
                          className="px-6 py-2 bg-[#A7C1A8] border-2 border-[#727D73] rounded-md text-lg font-medium text-[#2F3E2F] hover:bg-[#91B094] transition-shadow shadow-md"
                        >
                          Visualizar
                        </Link>
                      </div>
                    </div>
                  ))
                ) : (
             
                  <p className="text-xl text-gray-600">Nenhuma turma encontrada.</p>
                )}
              </div>
            </div>
          </main>
          <Link 
            className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg" 
            href={"/Login"}
            onClick={handleLogout}
          >Sair</Link>
        </div>
      </div>
    </>
  );
}