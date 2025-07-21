"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

// 1. Definir uma interface para a avaliação para melhorar a qualidade do código
interface Avaliacao {
  id: number; // Este é o id_avaliacao
  nome_aluno: string;
  nota: number | null;
  tipo_avaliacao: string;
}

export default function EditarNotas() {
  const searchParams = useSearchParams();
  const turmaId = searchParams.get("turmaId");
  const tipo = searchParams.get("tipo");

  // 2. Tipar os estados e adicionar novos para salvar e erros
  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[]>([]);
  const [notasEditadas, setNotasEditadas] = useState<{ [id: number]: string }>({});
  const [loading, setLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAvaliacoes() {
      // 3. Assumir ID do professor como 1, conforme outros arquivos
      const professorId = 1;
      try {
        setError(null);
        setLoading(true);
        // 4. Corrigir a URL do fetch para incluir o ID do professor
        const response = await fetch(`http://localhost:5000/historico/avaliacoes/turma/${turmaId}/${professorId}`);

        if (!response.ok) {
          throw new Error("Falha ao buscar as avaliações da turma.");
        }

        const data = await response.json();

        if (data && data.avaliacoes) {
          const filtradas = data.avaliacoes.filter(
            (a: Avaliacao) => a.tipo_avaliacao === tipo
          );
          setAvaliacoes(filtradas);
        } else {
          throw new Error("Formato de dados inesperado da API.");
        }
      } catch (error: any) {
        console.error("Erro ao buscar avaliações:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    if (turmaId && tipo) {
      fetchAvaliacoes();
    } else {
      setError("ID da turma ou tipo de avaliação não especificado.");
      setLoading(false);
    }
  }, [turmaId, tipo]);

  // 5. Função para lidar com a mudança de notas nos inputs
  const handleNotaChange = (avaliacaoId: number, novaNota: string) => {
    setNotasEditadas((prev) => ({
      ...prev,
      [avaliacaoId]: novaNota,
    }));
  };

  // 6. Implementar a função para salvar as notas
  const handleSave = async () => {
    if (Object.keys(notasEditadas).length === 0) {
      alert("Nenhuma nota foi alterada para salvar.");
      return;
    }

    setIsSaving(true);
    setError(null);

    const payload = {
      notas: Object.entries(notasEditadas)
        .map(([id, nota]) => ({
          id_avaliacao: parseInt(id, 10),
          nota: parseFloat(nota.replace(",", ".")),
        }))
        .filter((item) => !isNaN(item.nota)),
    };

    try {
      const response = await fetch("http://localhost:5000/professor/atualizar_nota", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Falha ao salvar as notas.");
      }

      // Atualiza o estado 'avaliacoes' para refletir as notas salvas
      // sem precisar recarregar a página.
      setAvaliacoes((currentAvaliacoes) =>
        currentAvaliacoes.map((avaliacao) => {
          if (notasEditadas[avaliacao.id] !== undefined) {
            const novaNotaStr = notasEditadas[avaliacao.id];
            const novaNotaNum = parseFloat(novaNotaStr.replace(",", "."));
            return { ...avaliacao, nota: isNaN(novaNotaNum) ? null : novaNotaNum };
          }
          return avaliacao;
        })
      );

      alert("Notas atualizadas com sucesso!");
      setNotasEditadas({}); // Limpa as edições pendentes
    } catch (error: any) {
      console.error("Erro ao salvar notas:", error);
      setError(error.message);
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

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center h-screen">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center mt-22 gap-6 border-11">
          <h1 className="text-[#EEA03D] text-6xl">{tipo}</h1>
          {error && <p className="text-red-500 text-center -my-4">{error}</p>}

          <main className="w-310 h-137 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-30 pb-15 overflow-y-auto">
            {loading ? (
              <p>Carregando...</p>
            ) : avaliacoes.length === 0 ? (
              <p>Nenhuma nota encontrada.</p>
            ) : (
              avaliacoes.map((nota) => (
                <div
                  key={nota.id}
                  className="w-229 min-h-20 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2"
                >
                  {nota.nome_aluno}
                  <input
                    // 7. Tornar o input controlado e adicionar handlers
                    className="w-18 h-12 bg-[#A7C1A8] border-5 rounded-lg border-[#EEA03D] text-center"
                    name={`nota-${nota.id}`}
                    type="text"
                    value={notasEditadas[nota.id] ?? nota.nota ?? ""}
                    onChange={(e) => handleNotaChange(nota.id, e.target.value)}
                  />
                </div>
              ))
            )}
          </main>

          {/* 8. Adicionar onClick e estado de desabilitado */}
          <button
            onClick={handleSave}
            disabled={isSaving || loading}
            className="w-100 h-19 border-5 rounded-lg border-[#7e8855] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isSaving ? "Salvando..." : "Salvar"}
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