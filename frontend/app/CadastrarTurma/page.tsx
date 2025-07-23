"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

// 1. Adicionar interfaces para tipar os dados da API
interface Professor {
    id: number;
    nome: string;
}

interface Aluno {
    id: number;
    nome: string;
}

// BOA PRÁTICA: Definir a URL base da sua API em um só lugar
const API_BASE_URL = "http://localhost:5000";

export default function CadastrarTurma() {
    const router = useRouter();

    // --- ESTADOS DO COMPONENTE ---
    // 2. Tipar os estados para garantir a segurança e o autocompletar
    const [nomeTurma, setNomeTurma] = useState("");
    const [todosProfessores, setTodosProfessores] = useState<Professor[]>([]);
    const [todosAlunos, setTodosAlunos] = useState<Aluno[]>([]);
    const [filtroProfessor, setFiltroProfessor] = useState("");
    const [filtroAluno, setFiltroAluno] = useState("");
    const [professorSelecionado, setProfessorSelecionado] = useState<Professor | null>(null);
    const [alunosSelecionados, setAlunosSelecionados] = useState<Aluno[]>([]);

    // --- EFEITO PARA BUSCAR DADOS DA API ---
    useEffect(() => {
        const id_escola = 1; // ❗ SUBSTITUA PELO ID REAL DA ESCOLA

        const fetchData = async () => {
            try {
                // Aponta para o seu backend Flask para buscar professores
                const resProfessores = await fetch(`${API_BASE_URL}/professores/escola/${id_escola}`);
                if (!resProfessores.ok) throw new Error("Falha ao buscar professores");
                const dataProfessores = await resProfessores.json();
                setTodosProfessores(dataProfessores.professores || []);

                // Aponta para o seu backend Flask para buscar alunos
                const resAlunos = await fetch(`${API_BASE_URL}/alunos/escola/${id_escola}`);
                if (!resAlunos.ok) throw new Error("Falha ao buscar alunos");
                const dataAlunos = await resAlunos.json();
                setTodosAlunos(dataAlunos.alunos || []);

            } catch (error) {
                console.error("Erro ao buscar dados:", error);
                alert("Não foi possível carregar os dados dos professores ou alunos.");
            }
        };

        fetchData();
    }, []);

    // --- FUNÇÕES DE MANIPULAÇÃO (sem alterações) ---
    const handleSelectProfessor = (professor: Professor) => {
        setProfessorSelecionado(professor);
    };

    const handleSelectAluno = (aluno: Aluno) => {
        if (!alunosSelecionados.some(a => a.id === aluno.id)) {
            setAlunosSelecionados([...alunosSelecionados, aluno]);
        }
    };

    const handleRemoveProfessor = () => {
        setProfessorSelecionado(null);
    };

    const handleRemoveAluno = (alunoId: number) => {
        setAlunosSelecionados(alunosSelecionados.filter(a => a.id !== alunoId));
    };

    // --- FUNÇÃO DE SUBMISSÃO DO FORMULÁRIO (VERSÃO CORRIGIDA) ---
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!nomeTurma || !professorSelecionado || alunosSelecionados.length === 0) {
            alert("Por favor, preencha o nome da turma, selecione um professor e adicione pelo menos um aluno.");
            return;
        }

        // Objeto de dados CORRIGIDO para corresponder ao backend
        const dadosNovaTurma = {
            nome: nomeTurma,
            escola_id: 1, // Chave 'escola_id' correta
            ids_professores: [professorSelecionado.id], // Enviado como uma lista
            ids_alunos: alunosSelecionados.map(aluno => aluno.id), // Já estava correto
            ano_letivo: new Date().getFullYear() // Adicionado o ano letivo atual
        };

        console.log("Enviando para o backend (formato corrigido):", dadosNovaTurma);

        try {
            // Rota CORRIGIDA para /turma (singular)
            const response = await fetch(`${API_BASE_URL}/turma`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dadosNovaTurma),
            });

            if (!response.ok) {
                // Tenta ler a mensagem de erro do backend para dar um alerta mais útil
                const errorData = await response.json();
                throw new Error(errorData.mensagem || 'Falha ao criar a turma');
            }

            const resultado = await response.json();
            console.log("Turma criada com sucesso:", resultado);
            alert(resultado.mensagem || "Turma criada com sucesso!");
            router.push('/ListaTurmas');

        } catch (error) {
            console.error("Erro ao criar turma:", error);
            
        }
    };


    // --- LÓGICA DE FILTRAGEM (sem alterações) ---
    const professoresFiltrados = todosProfessores.filter(p =>
        p.nome.toLowerCase().includes(filtroProfessor.toLowerCase()) && p.id !== professorSelecionado?.id
    );

    const alunosFiltrados = todosAlunos.filter(a =>
        a.nome.toLowerCase().includes(filtroAluno.toLowerCase()) && !alunosSelecionados.some(sel => sel.id === a.id)
    );

    // --- JSX (sem alterações na estrutura) ---
    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <form onSubmit={handleSubmit} className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto h-auto p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-6 border-11">
                    {/* ... todo o seu JSX continua aqui, sem alterações ... */}
                    <h1 className="text-[#EEA03D] text-6xl">Criar Turma</h1>
                    <h5 className="text-2xl">Nome da Turma</h5>
                    <input
                        className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                        type="text"
                        placeholder="Digite o nome da turma"
                        value={nomeTurma}
                        onChange={e => setNomeTurma(e.target.value)}
                        required
                    />

                    <div className="flex flex-wrap gap-10 justify-center items-start">
                        {/* Coluna da Esquerda: Busca */}
                        <div className="flex flex-col gap-4">
                            {/* Busca de Professor */}
                            <div>
                                <h5 className="text-2xl mb-2">Procurar Professor</h5>
                                <input
                                    className="w-80 h-10 border-5 rounded-lg border-[#A4B465] bg-amber-50 shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] p-2"
                                    placeholder="Digite para buscar..."
                                    value={filtroProfessor}
                                    onChange={e => setFiltroProfessor(e.target.value)}
                                />
                                <div className="overflow-y-auto h-32 mt-2 border border-gray-300 rounded-lg">
                                    {professoresFiltrados.map(prof => (
                                        <div key={prof.id} onClick={() => handleSelectProfessor(prof)} className="w-80 h-10 border-b border-[#A4B465] text-xl flex items-center pl-4 cursor-pointer hover:bg-amber-100">
                                            {prof.nome}
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Busca de Aluno */}
                            <div>
                                <h5 className="text-2xl mb-2">Procurar Aluno</h5>
                                <input
                                    className="w-80 h-10 border-5 rounded-lg border-[#A4B465] bg-amber-50 shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] p-2"
                                    placeholder="Digite para buscar..."
                                    value={filtroAluno}
                                    onChange={e => setFiltroAluno(e.target.value)}
                                />
                                <div className="overflow-y-auto h-32 mt-2 border border-gray-300 rounded-lg">
                                    {alunosFiltrados.map(aluno => (
                                        <div key={aluno.id} onClick={() => handleSelectAluno(aluno)} className="w-80 h-10 border-b border-[#A4B465] text-xl flex items-center pl-4 cursor-pointer hover:bg-amber-100">
                                            {aluno.nome}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Coluna da Direita: Selecionados */}
                        <div className="w-120">
                            <h5 className="text-2xl mb-2 text-center">Membros da Turma</h5>
                            <main className="w-full min-h-[300px] border-7 border-[#889E89] rounded-lg flex flex-col items-center gap-2 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] p-4 overflow-y-auto">
                                {/* Professor Selecionado */}
                                {professorSelecionado && (
                                    <div className="w-full h-15 border-4 rounded-lg border-[#A4B465] text-2xl flex items-center justify-between pl-4 pr-2 bg-green-100">
                                        <span>👑 {professorSelecionado.nome}</span>
                                        <button type="button" onClick={handleRemoveProfessor}>
                                            <img className="w-6" src="/imagem/lixo.png" alt="Remover" />
                                        </button>
                                    </div>
                                )}
                                
                                <hr className="w-full border-t-2 border-gray-300 my-2" />
                                
                                {/* Alunos Selecionados */}
                                {alunosSelecionados.map(aluno => (
                                    <div key={aluno.id} className="w-full h-15 border-4 rounded-lg border-[#A4B465] text-2xl flex items-center justify-between pl-4 pr-2">
                                        <span>{aluno.nome}</span>
                                        <button type="button" onClick={() => handleRemoveAluno(aluno.id)}>
                                            <img className="w-6" src="/imagem/lixo.png" alt="Remover" />
                                        </button>
                                    </div>
                                ))}
                                {alunosSelecionados.length === 0 && !professorSelecionado && (
                                    <p className="text-gray-500 mt-10">Selecione um professor e alunos...</p>
                                )}
                            </main>
                        </div>
                    </div>

                    {/* Botões de Ação */}
                    <div className="flex flex-col items-center gap-4 mt-4">
                        <button type="submit" className="w-100 h-16 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl hover:bg-amber-100 transition-colors">
                            Criar Turma
                        </button>
                        <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg hover:bg-gray-100 transition-colors" href={"/ListaTurmas"}>
                            Voltar
                        </Link>
                    </div>
                </form>
            </div>
        </>
    );
}