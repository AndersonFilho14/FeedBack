"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";

interface Professor {
    id: number;
    nome: string;
}

export default function ListaProfessores() {
    const [professores, setProfessores] = useState<Professor[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [professorParaDeletar, setProfessorParaDeletar] = useState<number | null>(null);

    useEffect(() => {
        async function fetchProfessores() {
            try {
                const response = await fetch("http://localhost:5000/professores/escola/1");
                if (!response.ok) {
                    throw new Error("Falha ao buscar a lista de professores.");
                }
                const data = await response.json();
                if (data && Array.isArray(data.professores)) {
                    setProfessores(data.professores);
                } else {
                    throw new Error("Formato de dados inesperado da API.");
                }
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchProfessores();
    }, []);

    const handleDelete = async () => {
        if (professorParaDeletar === null) return;
        try {
            const response = await fetch(`http://localhost:5000/professor/${professorParaDeletar}`, { method: 'DELETE' });
            const data = await response.json();
            if (!response.ok) throw new Error(data.mensagem || "Erro ao deletar professor.");
            setProfessores(prev => prev.filter(p => p.id !== professorParaDeletar));
            alert(data.mensagem);
        } catch (err: any) {
            alert(`Erro: ${err.message}`);
        } finally {
            setProfessorParaDeletar(null);
        }
    };
    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center h-screen">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center mt-22 gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-6xl">Lista de Professores</h1>
                    <main className="w-310 h-137 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-15 overflow-y-auto">
                        {loading ? <p>Carregando...</p> :
                         error ? <p className="text-red-500">{error}</p> :
                         professores.length === 0 ? <p>Nenhum professor encontrado.</p> :
                         professores.map((professor) => (
                            <div key={professor.id} className="w-229 h-15 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                {professor.nome}
                                <div className="flex gap-4 items-center">
                                    <Link href={`/EditarProfessor?id=${professor.id}`}>
                                        <img className="w-10 h-10" src="/imagem/editar.png" alt="Editar" />
                                    </Link>
                                    <button type="button" onClick={() => setProfessorParaDeletar(professor.id)} className="focus:outline-none">
                                        <img className="w-10 h-10" src="/imagem/lixo.png" alt="Excluir" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </main>
                    <Link className="w-100 h-19 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl" href="/CadastrarProfessor">
                        Cadastrar Professor
                    </Link>
                    <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg" href="/EdicaoEscola">
                        Voltar
                    </Link>
                </div>

                {professorParaDeletar !== null && (
                    <div className="fixed inset-0 flex items-center justify-center bg-[rgba(0,0,0,0.32)] z-50">
                        <div className="bg-[#ECF0EC] rounded-lg shadow-[0px_19px_4px_4px_rgba(0,0,0,0.25)] p-8 flex flex-col gap-15 items-center justify-center w-[502px] h-[484px] border-[7px] border-[#889E89]">
                            <div className="w-[406px] h-[91px] bg-[#EEA03D] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px] text-center text-2xl text-black font-[Hammersmith_One]">
                                VOCÊ ESTÁ EXCLUINDO UM <br /> PROFESSOR
                            </div>
                            <span className="font-[Jomolhari] text-4xl mb-4 text-center">
                                Tem certeza que deseja Excluir?
                            </span>
                            <div className="flex flex-col items-center gap-4">
                                <button
                                    className="font-[Jomolhari] text-3xl w-[206px] h-[61px] bg-[#ECF0EC] border-6 border-[#EEA03D] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px]"
                                    onClick={handleDelete}
                                >
                                    Confirmar
                                </button>
                                <button
                                    className="font-[Jomolhari] w-[122px] h-[37px] bg-[#ECF0EC] border-[7px] border-[#727D73] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px]"
                                    onClick={() => setProfessorParaDeletar(null)}
                                >
                                    Voltar
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
