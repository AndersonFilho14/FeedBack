"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

// --- Interfaces ---
interface Professor {
    id: number;
    nome: string;
}
interface Aluno {
    id: number;
    nome: string;
}
interface TurmaState {
    nome: string;
    professor: Professor | null;
    alunos: Aluno[];
}

const API_BASE_URL = "http://localhost:5000";

export default function EditarTurma() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const turmaId = searchParams.get('turmaId');

    // Estado unificado para a turma
    const [turma, setTurma] = useState<TurmaState>({
        nome: "",
        professor: null,
        alunos: [],
    });

    // Estado para guardar a versão inicial da turma
    const [initialTurma, setInitialTurma] = useState<TurmaState | null>(null);

    // Listas para popular os campos de busca
    const [todosProfessores, setTodosProfessores] = useState<Professor[]>([]);
    const [todosAlunos, setTodosAlunos] = useState<Aluno[]>([]);
    
    // Filtros de busca
    const [filtroProfessor, setFiltroProfessor] = useState("");
    const [filtroAluno, setFiltroAluno] = useState("");
    
    // Estados de controle da UI
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    useEffect(() => {
        if (!turmaId) {
            setError("ID da turma não encontrado na URL.");
            setIsLoading(false);
            return;
        }

        const fetchData = async () => {
            setIsLoading(true);
            setError(null);
            try {
                const [turmasRes, professoresRes, alunosRes] = await Promise.all([
                    fetch(`${API_BASE_URL}/turmas/escola/1`),
                    fetch(`${API_BASE_URL}/professores/escola/1`),
                    fetch(`${API_BASE_URL}/alunos/escola/1`)
                ]);

                if (!turmasRes.ok || !professoresRes.ok || !alunosRes.ok) throw new Error("Falha ao carregar dados iniciais.");

                const todasAsTurmas = await turmasRes.json();
                const dataProfessores = await professoresRes.json();
                const dataAlunos = await alunosRes.json();

                setTodosProfessores(dataProfessores.professores || []);
                setTodosAlunos(dataAlunos.alunos || []);
                
                const turmaEncontrada = todasAsTurmas.find((t: any) => t.turma_id.toString() === turmaId);
                if (!turmaEncontrada) throw new Error("Turma com o ID especificado não foi encontrada.");
                
                const dadosIniciais = {
                    nome: turmaEncontrada.nome || "",
                    professor: turmaEncontrada.professores?.[0] || null,
                    alunos: turmaEncontrada.alunos || []
                };

                setTurma(dadosIniciais);
                setInitialTurma(dadosIniciais);

            } catch (err: any) {
                setError(err.message || "Ocorreu um erro desconhecido");
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [turmaId]);

    const handleNomeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTurma(prev => ({ ...prev, nome: e.target.value }));
    };

    const handleSelectProfessor = (professor: Professor) => {
        setTurma(prev => ({ ...prev, professor: professor }));
    };

    const handleRemoveProfessor = () => {
        setTurma(prev => ({ ...prev, professor: null }));
    };
    
    const handleSelectAluno = (aluno: Aluno) => {
        if (!turma.alunos.some(a => a.id === aluno.id)) {
            setTurma(prev => ({ ...prev, alunos: [...prev.alunos, aluno] }));
        }
    };

    const handleRemoveAluno = (alunoId: number) => {
        setTurma(prev => ({
            ...prev,
            alunos: prev.alunos.filter(a => a.id !== alunoId)
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!initialTurma) return;

        setIsSaving(true);
        setError(null);
        setSuccessMessage(null);

        try {
            const id_professor_atual = turma.professor?.id !== initialTurma.professor?.id ? (turma.professor?.id ?? null) : null;
            const id_professor_anterior = turma.professor?.id !== initialTurma.professor?.id ? (initialTurma.professor?.id ?? null) : null;
            
            const initialAlunosSet = new Set(initialTurma.alunos.map(a => a.id));
            const finalAlunosSet = new Set(turma.alunos.map(a => a.id));

            const ids_alunos_atuais = [...finalAlunosSet].filter(id => !initialAlunosSet.has(id));
            const ids_alunos_anteriores = [...initialAlunosSet].filter(id => !finalAlunosSet.has(id));

            const payload = {
                nome: turma.nome,
                ano_letivo: new Date().getFullYear(),
                id_professor_atual,
                id_professor_anterior,
                ids_alunos_atuais,
                ids_alunos_anteriores,
            };

            const response = await fetch(`${API_BASE_URL}/turma/${turmaId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.mensagem || "Falha ao atualizar a turma.");
            
            setSuccessMessage(result.mensagem);
            
            setInitialTurma(turma);

        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSaving(false);
        }
    };
    
    const professoresFiltrados = todosProfessores.filter(p => p.id !== turma.professor?.id && p.nome.toLowerCase().includes(filtroProfessor.toLowerCase()));
    const alunosFiltrados = todosAlunos.filter(a => !turma.alunos.some(sel => sel.id === a.id) && a.nome.toLowerCase().includes(filtroAluno.toLowerCase()));
    
    if (isLoading) return <div className="flex justify-center items-center min-h-screen bg-[#F5ECD5] font-[Jomolhari] text-2xl">Carregando...</div>;
    if (error) return <div className="flex justify-center items-center min-h-screen bg-[#F5ECD5] font-[Jomolhari] text-red-500 text-2xl">{error}</div>;

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <form onSubmit={handleSubmit} className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto h-auto p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-6xl">Editar Turma</h1>
                    
                    {successMessage && <div className="font-[Jomolhari] bg-green-200 text-green-800 p-3 rounded-lg w-full text-center">{successMessage}</div>}
                    {error && <div className="font-[Jomolhari] bg-red-200 text-red-800 p-3 rounded-lg w-full text-center">{error}</div>}

                    <h5 className="text-2xl">Nome da Turma</h5>
                    <input
                        className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                        type="text"
                        value={turma.nome}
                        onChange={handleNomeChange}
                        required
                    />
                    <div className="flex flex-wrap gap-10 justify-center items-start">
                        <div className="flex flex-col gap-4">
                            <div>
                                <h5 className="text-2xl mb-2">Procurar Professor</h5>
                                <input
                                    className="w-80 h-10 border-5 rounded-lg border-[#A4B465] bg-amber-50 shadow-md p-2"
                                    placeholder="Buscar professor disponível..."
                                    value={filtroProfessor}
                                    onChange={e => setFiltroProfessor(e.target.value)}
                                />
                                <div className="overflow-y-auto h-32 mt-2 border border-gray-300 rounded-lg bg-white/50">
                                    {professoresFiltrados.map(prof => (
                                        <div key={prof.id} onClick={() => handleSelectProfessor(prof)} className="p-2 border-b cursor-pointer hover:bg-amber-100">{prof.nome}</div>
                                    ))}
                                </div>
                            </div>
                            <div>
                                <h5 className="text-2xl mb-2">Procurar Aluno</h5>
                                <input 
                                    className="w-80 h-10 border-5 rounded-lg border-[#A4B465] bg-amber-50 shadow-md p-2" 
                                    placeholder="Buscar aluno disponível..."
                                    value={filtroAluno}
                                    onChange={e => setFiltroAluno(e.target.value)}
                                />
                                <div className="overflow-y-auto h-32 mt-2 border border-gray-300 rounded-lg bg-white/50">
                                    {alunosFiltrados.map(aluno => (
                                        <div key={aluno.id} onClick={() => handleSelectAluno(aluno)} className="p-2 border-b cursor-pointer hover:bg-amber-100">{aluno.nome}</div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="w-120">
                            <h5 className="text-2xl mb-2 text-center">Membros Atuais</h5>
                            <main className="w-full min-h-[340px] border-7 border-[#889E89] rounded-lg flex flex-col items-center gap-2 bg-amber-50 shadow-lg p-4 overflow-y-auto">
                                {turma.professor && (
                                    <div className="w-full p-2 border-4 rounded-lg border-[#A4B465] bg-green-100 flex justify-between items-center text-xl">
                                        <span>👑 {turma.professor.nome}</span>
                                        <button type="button" onClick={handleRemoveProfessor} className="p-1"><img className="w-6" src="/imagem/lixo.png" alt="Remover" /></button>
                                    </div>
                                )}
                                {(turma.professor && turma.alunos.length > 0) && <hr className="w-full my-2 border-t-2 border-gray-300"/>}
                                {turma.alunos.map(aluno => (
                                    <div key={aluno.id} className="w-full p-2 border-4 rounded-lg border-[#A4B465] flex justify-between items-center text-xl">
                                        <span>{aluno.nome}</span>
                                        <button type="button" onClick={() => handleRemoveAluno(aluno.id)} className="p-1"><img className="w-6" src="/imagem/lixo.png" alt="Remover" /></button>
                                    </div>
                                ))}
                                {!turma.professor && turma.alunos.length === 0 && (
                                    <div className="flex-grow flex items-center justify-center">
                                        <p className="text-gray-500 text-center">Nenhum membro selecionado.</p>
                                    </div>
                                )}
                            </main>
                        </div>
                    </div>
                    <div className="flex gap-4 items-center mt-4">
                        <Link className="w-34 h-12 px-4 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-lg bg-amber-50 text-xl hover:bg-gray-100" href={"/ListaTurmas"}>
                            Voltar
                        </Link>
                        <button 
                            type="submit" 
                            disabled={isSaving}
                            className="w-100 h-19 px-6 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-lg bg-amber-50 text-4xl hover:bg-amber-100 disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            {isSaving ? "Salvando..." : "Salvar"}
                        </button>
                    </div>
                </form>
            </div>
        </>
    );
}