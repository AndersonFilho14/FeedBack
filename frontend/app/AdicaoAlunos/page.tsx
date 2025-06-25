"use client";
import React, { useEffect, useState } from "react";



interface Professor {
    id: number;
    nome: string;
    cpf: string;
    cargo: string;
    id_escola: number;
}

interface Aluno {
    id: number;
    nome: string;
    idade: number;
    faltas: number;
    id_turma: number;
}

interface ProfessorAlunosResponse {
    professor: Professor;
    total_alunos_vinculados: number;
    alunos_vinculados: Aluno[];
}

export default function AdicaoAlunos() {
    const [data, setData] = useState<ProfessorAlunosResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Armazene o id do professor em um estado para permitir atualização dinâmica
    const [idProfessor, setIdProfessor] = useState<string>("1");

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError(null);
            try {
                const res = await fetch(
                    `http://127.0.0.1:5000/professor/visualizar_alunos/${idProfessor}`
                );
                if (!res.ok) throw new Error("Erro ao buscar dados");
                const json = await res.json();
                setData(json);
            } catch (err: any) {
                setError(err.message);
                setData(null);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [idProfessor]);

    

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50 flex items-center justify-center">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen pt-24">
                <main className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-[32rem] min-h-[35rem] rounded-3xl shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] flex flex-col items-center border-11 px-8 py-10">
                    <h1 className="text-[#EEA03D] mt-4 mb-8 text-5xl font-bold">Professor</h1>
                    <div className="mb-8 w-full text-lg text-[#727D73]">
                        {data ? (
                            <>
                                <div><b>ID:</b> {data.professor.id}</div>
                                <div><b>Nome:</b> {data.professor.nome}</div>
                                <div><b>CPF:</b> {data.professor.cpf}</div>
                                <div>
                                    <b>Cargo:</b>{" "}
                                    {data.professor.cargo
                                        ? data.professor.cargo
                                        : <span className="text-red-500 font-semibold">Cargo não encontrado</span>
                                    }
                                </div>
                                <div><b>ID Escola:</b> {data.professor.id_escola}</div>
                            </>
                        ) : (
                            <div className="text-gray-500">Dados do professor nao foram encontrados...</div>
                        )}
                    </div>
                    <h2 className="text-2xl font-semibold mb-4 text-[#EEA03D]">
                        Total de alunos vinculados: {data ? data.total_alunos_vinculados : 0}
                    </h2>
                    <div className="mb-6 w-full flex flex-col items-start">
                        <input
                            id="professorId"
                            type="number"
                            min={1}
                            value={idProfessor}
                            onChange={e => {
                                setIdProfessor(e.target.value);
                            }}
                            className="border border-[#A7C1A8] rounded px-3 py-1 w-32"
                        />
                    </div>
                    {error === "Erro ao buscar dados" ? (
                        <div className="text-red-500 font-semibold mb-4">ID não encontrado</div>
                    ) : null}
                    <div className="overflow-x-auto w-full">
                        <table className="min-w-full border border-[#A7C1A8] bg-white rounded-xl shadow">
                            <thead className="bg-[#A7C1A8] text-[#727D73]">
                                <tr>
                                    <th className="border px-4 py-2">ID</th>
                                    <th className="border px-4 py-2">Nome</th>
                                    <th className="border px-4 py-2">Idade</th>
                                    <th className="border px-4 py-2">Faltas</th>
                                    <th className="border px-4 py-2">ID Turma</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data && data.alunos_vinculados.map((aluno) => (
                                    <tr key={aluno.id} className="text-center hover:bg-[#F5ECD5]">
                                        <td className="border px-4 py-2">{aluno.id}</td>
                                        <td className="border px-4 py-2">{aluno.nome}</td>
                                        <td className="border px-4 py-2">{aluno.idade}</td>
                                        <td className="border px-4 py-2">{aluno.faltas}</td>
                                        <td className="border px-4 py-2">{aluno.id_turma}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </main>
            </div>
        </>
    );
}
