"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";

// --- Interfaces ---
interface Professor {
    id: number;
    nome: string;
    id_escola?: number;
}
interface Aluno {
    id: number;
    nome: string;
}
const API_BASE_URL = "http://localhost:5000";

export default function EditarTurma() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const turmaId = searchParams.get('turmaId');

    // --- ESTADOS DO COMPONENTE ---
    const [nomeTurma, setNomeTurma] = useState("");
    const [todosProfessores, setTodosProfessores] = useState<Professor[]>([]);
    const [todosAlunos, setTodosAlunos] = useState<Aluno[]>([]);
    const [filtroProfessor, setFiltroProfessor] = useState("");
    const [filtroAluno, setFiltroAluno] = useState("");
    
    const [professoresSelecionados, setProfessoresSelecionados] = useState<Professor[]>([]);
    const [alunosSelecionados, setAlunosSelecionados] = useState<Aluno[]>([]);

    // Estados para guardar o estado inicial e calcular a diferença no momento do envio
    const [initialProfessores, setInitialProfessores] = useState<Professor[]>([]);
    const [initialAlunos, setInitialAlunos] = useState<Aluno[]>([]);

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // --- EFEITO PARA BUSCAR DADOS ---
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
                const resTurmas = await fetch(`${API_BASE_URL}/turmas/escola/1`);
                if (!resTurmas.ok) throw new Error("Falha ao buscar a lista de turmas.");
                const todasAsTurmas = await resTurmas.json();
                const turma = todasAsTurmas.find((t: any) => t.turma_id.toString() === turmaId);
                if (!turma) throw new Error("Turma com o ID especificado não foi encontrada.");

                const profsAtuais = turma.professores || [];
                const alunosAtuais = turma.alunos || [];

                setNomeTurma(turma.nome || "");
                setProfessoresSelecionados(profsAtuais);
                setAlunosSelecionados(alunosAtuais);

                // Guarda uma cópia segura do estado inicial para calcular a diferença no momento do envio.
                setInitialProfessores([...profsAtuais]);
                setInitialAlunos([...alunosAtuais]);
                
                // Busca as listas completas de professores e alunos
                const resProfessores = await fetch(`${API_BASE_URL}/professores/escola/${turma.id_escola}`);
                const dataProfessores = await resProfessores.json();
                setTodosProfessores(dataProfessores.professores || []);

                const resAlunos = await fetch(`${API_BASE_URL}/alunos/escola/${turma.id_escola}`);
                const dataAlunos = await resAlunos.json();
                setTodosAlunos(dataAlunos.alunos || []);

            } catch (err: any) {
                setError(err.message || "Ocorreu um erro desconhecido");
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, [turmaId]);

    // --- Funções de manipulação simplificadas ---
    const handleSelectProfessor = (professor: Professor) => {
        if (!professoresSelecionados.some(p => p.id === professor.id)) {
            setProfessoresSelecionados(prev => [...prev, professor]);
        }
    };
   

    const handleSelectAluno = (aluno: Aluno) => {
        if (!alunosSelecionados.some(a => a.id === aluno.id)) {
            setAlunosSelecionados(prev => [...prev, aluno]);
        }
    };
    const handleRemoveAluno = (alunoId: number) => {
        setAlunosSelecionados(prev => prev.filter(a => a.id !== alunoId));
    };

    // No seu arquivo EditarTurma.tsx

// --- FUNÇÃO DE SUBMISSÃO (COM LÓGICA DE DUAS REQUISIÇÕES) ---
const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Lógica de cálculo de diferenças (continua a mesma)
    const idsProfessoresIniciais = initialProfessores.map(p => p.id);
    const idsProfessoresFinais = professoresSelecionados.map(p => p.id);
    const professoresParaAdicionar = idsProfessoresFinais.filter(id => !idsProfessoresIniciais.includes(id));
    const professoresParaRemover = idsProfessoresIniciais.filter(id => !idsProfessoresFinais.includes(id));

    const idsAlunosIniciais = initialAlunos.map(a => a.id);
    const idsAlunosFinais = alunosSelecionados.map(a => a.id);
    const alunosParaAdicionar = idsAlunosFinais.filter(id => !idsAlunosIniciais.includes(id));
    const alunosParaRemover = idsAlunosIniciais.filter(id => !idsAlunosFinais.includes(id));
    
    // --- INÍCIO DA NOVA LÓGICA ---

    // 1. Monta o payload APENAS com as alterações de nome e ALUNOS
    const payloadAlunosENome = {
        nome: nomeTurma,
        ano_letivo: new Date().getFullYear(),
        ids_alunos_atuais: alunosParaAdicionar,
        ids_alunos_anteriores: alunosParaRemover,
        // Envia as chaves de professores vazias para não acionar a lógica no backend
        ids_professores_atuais: [],
        ids_professores_anteriores: [],
    };

    // 2. Monta o payload APENAS com as alterações de PROFESSORES
    const payloadProfessores = {
        nome: nomeTurma, // O nome precisa ser enviado novamente
        ano_letivo: new Date().getFullYear(),
        ids_professores_atuais: professoresParaAdicionar,
        ids_professores_anteriores: professoresParaRemover,
        // Envia as chaves de alunos vazias
        ids_alunos_atuais: [],
        ids_alunos_anteriores: [],
    };
    
    try {
        console.log("Passo 1: Enviando atualização de alunos e nome...", payloadAlunosENome);
        // 3. Envia a PRIMEIRA requisição (alunos e nome)
        const responseAlunos = await fetch(`${API_BASE_URL}/turma/${turmaId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadAlunosENome),
        });

        if (!responseAlunos.ok) {
            const errorData = await responseAlunos.json();
            throw new Error(`Falha ao atualizar alunos: ${errorData.mensagem || 'Erro desconhecido'}`);
        }

        console.log("Passo 2: Enviando atualização de professores...", payloadProfessores);
        // 4. Se a primeira deu certo, envia a SEGUNDA requisição (professores)
        const responseProfessores = await fetch(`${API_BASE_URL}/turma/${turmaId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadProfessores),
        });

        if (!responseProfessores.ok) {
            const errorData = await responseProfessores.json();
            throw new Error(`Falha ao atualizar professores: ${errorData.mensagem || 'Erro desconhecido'}`);
        }
        
        const resultadoFinal = await responseProfessores.json();
        alert(resultadoFinal.mensagem || "Turma atualizada com sucesso!");
        router.push("/ListaTurmas");

    } catch (err: any) {
        alert(`Erro no processo de atualização: ${err.message}`);
    }
};
    
    // --- LÓGICA DE FILTRAGEM ---
    const professoresFiltrados = todosProfessores.filter(p => 
        !professoresSelecionados.some(sel => sel.id === p.id) && 
        p.nome.toLowerCase().includes(filtroProfessor.toLowerCase())
    );
    const alunosFiltrados = todosAlunos.filter(a => 
        !alunosSelecionados.some(sel => sel.id === a.id) && 
        a.nome.toLowerCase().includes(filtroAluno.toLowerCase())
    );
    
    // --- JSX (sem alterações) ---
    if (isLoading) return <p className="text-center text-2xl mt-40">Carregando...</p>;
    if (error) return <p className="text-center text-red-500 text-2xl mt-40">Erro: {error}</p>;

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <form onSubmit={handleSubmit} className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto h-auto p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-6xl">Editar Turma</h1>
                    <h5 className="text-2xl">Nome da Turma</h5>
                    <input
                        className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                        type="text"
                        value={nomeTurma}
                        onChange={e => setNomeTurma(e.target.value)}
                        required
                    />
                    <div className="flex flex-wrap gap-10 justify-center items-start">
                        <div className="flex flex-col gap-4 w-80">
                            
                            <h5 className="text-2xl">Procurar Aluno</h5>
                            <input 
                                className="w-80 h-10 border-5 rounded-lg border-[#A4B465] bg-amber-50 shadow-md p-2" 
                                placeholder="Buscar aluno disponível..."
                                value={filtroAluno}
                                onChange={e => setFiltroAluno(e.target.value)}
                            />
                            <div className="overflow-y-auto h-20 mt-2 border rounded-lg">
                                {alunosFiltrados.map(aluno => (
                                    <div key={aluno.id} onClick={() => handleSelectAluno(aluno)} className="w-full p-2 border-b cursor-pointer hover:bg-amber-100">{aluno.nome}</div>
                                ))}
                            </div>
                        </div>
                        <div className="w-120">
                            <h5 className="text-2xl mb-2 text-center">Membros Atuais</h5>
                            <main className="w-120 h-100 border-7 border-[#889E89] rounded-lg flex flex-col items-center gap-2 bg-amber-50 shadow-lg p-4 overflow-y-auto">
                                {professoresSelecionados.map(prof => (
                                    <div key={prof.id} className="w-full p-2 border-4 rounded-lg border-[#A4B465] bg-green-100 flex justify-between items-center">
                                        <span>👑 {prof.nome}</span>
                                        
                                    </div>
                                ))}
                                {(professoresSelecionados.length > 0 && alunosSelecionados.length > 0) && <hr className="w-full my-2 border-t-2"/>}
                                {alunosSelecionados.map(aluno => (
                                    <div key={aluno.id} className="w-full p-2 border-4 rounded-lg border-[#A4B465] flex justify-between items-center">
                                        <span>{aluno.nome}</span>
                                        <button type="button" onClick={() => handleRemoveAluno(aluno.id)} className="p-1"><img className="w-6" src="/imagem/lixo.png" alt="Remover" /></button>
                                    </div>
                                ))}
                            </main>
                        </div>
                    </div>
                    <div className="flex gap-4 items-center">
                        <button type="submit" className="w-100 h-19 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-lg bg-amber-50 text-4xl hover:bg-amber-100">
                            Salvar
                        </button>
                        <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-lg bg-amber-50 text-lg hover:bg-gray-100" href={"/ListaTurmas"}>
                            Voltar
                        </Link>
                    </div>
                </form>
            </div>
        </>
    );
}