"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

interface Aluno {
  id: number;
  nome: string;
  faltas: number;
  id_turma: number;
}

export default function CadastrarPresenca() {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Estado para armazenar as faltas editadas
  const [isSaving, setIsSaving] = useState(false);
  const [faltasEditadas, setFaltasEditadas] = useState<{ [alunoId: number]: number }>({});
  const searchParams = useSearchParams();
  const turmaId = searchParams.get("turmaId");
  const [turma, setTurma] = useState<string | null>(null);

  useEffect(() => {
    if (turmaId) {
      const fetchData = async () => {
        try {
          setLoading(true);
          const response = await fetch(`http://127.0.0.1:5000/professor/visualizar_alunos/1`);
          if (!response.ok) {
            throw new Error("Falha ao buscar dados dos alunos");
          }
          const data = await response.json();
          if (data && data.alunos_vinculados) {
            const alunosDaTurma = data.alunos_vinculados.filter(
              (aluno: Aluno) => aluno.id_turma.toString() === turmaId
            );
            setAlunos(alunosDaTurma);
            setTurma(`Turma ${turmaId}`);
          } else {
            throw new Error("Dados de alunos não encontrados na resposta da API");
          }
        } catch (err: any) {
          setError(err.message);
          console.error(err);
        } finally {
          setLoading(false);
        }
      };
      fetchData();
    } else {
      setError("ID da turma não encontrado na URL.");
      setLoading(false);
    }
  }, [turmaId]);

  const handleFaltasChange = (alunoId: number, novasFaltas: string) => {
    const valorNumerico = parseInt(novasFaltas, 10);
    if (!isNaN(valorNumerico) && valorNumerico >= 0) {
      setFaltasEditadas(prev => ({
        ...prev,
        [alunoId]: valorNumerico,
      }));
    }
  };
  
  const handleSave = async () => {
    if (Object.keys(faltasEditadas).length === 0) {
      alert("Nenhuma alteração para salvar.");
      return;
    }

    setIsSaving(true);

    const lista_faltas = Object.entries(faltasEditadas).map(
      ([alunoId, faltas]) => ({
        id_aluno: parseInt(alunoId, 10),
        faltas: faltas,
      })
    );

    // Assumindo que o ID do professor é "1", como na busca de dados.
    const payload = {
      id_professor: "1",
      faltas: lista_faltas,
    };

    try {
      const response = await fetch("http://localhost:5000/professor/atualizar_faltas_turma", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.message || "Falha ao salvar as faltas.");
      }

      // Atualiza o estado local dos alunos para refletir as novas faltas
      setAlunos(currentAlunos =>
        currentAlunos.map(aluno =>
          faltasEditadas[aluno.id] !== undefined
            ? { ...aluno, faltas: faltasEditadas[aluno.id] }
            : aluno
        )
      );

      alert("Faltas atualizadas com sucesso!");
      setFaltasEditadas({}); // Limpa as edições pendentes
    } catch (error: any) {
      console.error("Erro ao salvar faltas:", error);
      alert(`Erro ao salvar: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>
      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex flex-col justify-center items-center h-screen ">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-7 border-11 ">
          <div className="flex flex-col items-center gap-1"><h1 className="text-[#EEA03D] text-6xl ">Faltas</h1><h3>{turma}</h3></div>
          <main className="w-300 h-150 border-7 border-[#889E89] rounded-lg flex flex-col items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] py-4 px-2 overflow-y-auto">
            {loading ? (
              <p>Carregando alunos...</p>
            ) : error ? (
              <p className="text-red-500">{error}</p>
            ) : (
              alunos.map((aluno) => (
                <div key={aluno.id} className="w-full min-h-16 border-7 rounded-lg border-[#A4B465] text-xl flex items-center justify-between px-4">
                  <span className="flex-1 truncate">{aluno.nome}</span>
                  <div className="flex items-center gap-2">
                    <label htmlFor={`faltas-${aluno.id}`} className="text-lg">Faltas:</label>
                    <input
                      id={`faltas-${aluno.id}`}
                      type="number"
                      value={faltasEditadas[aluno.id] ?? aluno.faltas}
                      onChange={(e) => handleFaltasChange(aluno.id, e.target.value)}
                      className="w-20 h-10 text-center bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                    />
                  </div>
                </div>
              ))
            )}
          </main>
          <button 
            onClick={handleSave} 
            disabled={isSaving}
            className="w-100 h-19 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isSaving ? "Salvando..." : "Salvar"}
          </button>
          <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg mb-2" href={`/EdicaoTurma?turmaId=${turmaId}`}>Voltar</Link>
        </div>
      </div>
    </>
    );
}
