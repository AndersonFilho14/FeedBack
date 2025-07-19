"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

export default function EditarNotas() {
  const searchParams = useSearchParams();
  const turmaId = searchParams.get("turmaId");
  const tipo = searchParams.get("tipo");

  const [avaliacoes, setAvaliacoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchAvaliacoes() {
      try {
        const response = await fetch(`http://localhost:5000/historico/avaliacoes/turma/${turmaId}`);
        const data = await response.json();
        
        // Filtro por tipo de avaliação (ex: "1Va", "2Va")
        const filtradas = data.avaliacoes.filter(
          (a: any) => a.tipo_avaliacao === tipo
        );
        setAvaliacoes(filtradas);
      } catch (error) {
        console.error("Erro ao buscar avaliações:", error);
      } finally {
        setLoading(false);
      }
    }

    if (turmaId && tipo) {
      fetchAvaliacoes();
    }
  }, [turmaId, tipo]);

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center h-screen">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center mt-22 gap-6 border-11">
          <h1 className="text-[#EEA03D] text-6xl">{tipo}</h1>

          <main className="w-310 h-137 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-30 pb-15 overflow-y-auto">
            {loading ? (
              <p>Carregando...</p>
            ) : avaliacoes.length === 0 ? (
              <p>Nenhuma nota encontrada.</p>
            ) : (
              avaliacoes.map((nota: any) => (
                <div
                  key={nota.id}
                  className="w-229 min-h-20 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2"
                >
                  {nota.nome_aluno}
                  <input
                    className="w-18 h-12 bg-[#A7C1A8] border-5 rounded-lg border-[#EEA03D] text-center"
                    name={`nota-${nota.id}`}
                    type="text"
                    defaultValue={nota.nota}
                  />
                </div>
              ))
            )}
          </main>

          <button
            className="w-100 h-19 border-5 rounded-lg border-[#7e8855] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl"
            
            >
            Salvar
            </button>


          <Link
            className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg"
            href={`/CadastrarNotas?turmaId=${turmaId}`}
          >
            Voltar
          </Link>
        </div>
      </div>
    </>
  );
}
