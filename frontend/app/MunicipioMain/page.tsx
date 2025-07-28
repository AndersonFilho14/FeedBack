"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from 'next/navigation';

// --- Tipos de Dados ---
interface Escola {
    id_escola: number;
    nome: string;
    id_municipio: number;
    nome_usuario: string;
}

interface Materia {
    id_materia: number;
    nome: string;
    id_disciplina: number;
    id_professor: number;
}

export default function PainelMunicipio() {
    // --- Estados para Escolas ---
    const [escolas, setEscolas] = useState<Escola[]>([]);
    const [escolaEditando, setEscolaEditando] = useState<Escola | null>(null);
    const [nomeEscola, setNomeEscola] = useState("");
    const [idMunicipio, setIdMunicipio] = useState("");
    const [nomeUsuario, setNomeUsuario] = useState("");
    const [senha, setSenha] = useState("");

    // --- Estados para Matérias ---
    const [materias, setMaterias] = useState<Materia[]>([]);
    const [materiaEditando, setMateriaEditando] = useState<Materia | null>(null);
    const [nomeMateria, setNomeMateria] = useState("");
    const [idDisciplina, setIdDisciplina] = useState("");
    const [idProfessor, setIdProfessor] = useState("");
    const [idProfessorFiltro, setIdProfessorFiltro] = useState("1"); // Filtro inicia com o professor de ID 1

    // --- Estados de UI (Interface do Usuário) ---
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmittingEscola, setIsSubmittingEscola] = useState(false);
    const [isSubmittingMateria, setIsSubmittingMateria] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const router = useRouter();
    const API_URL = "http://127.0.0.1:5000";

    // =============================================
    // Funções do CRUD de ESCOLAS
    // =============================================
    const fetchEscolas = async () => {
        try {
            const response = await fetch(`${API_URL}/escola`);
            if (!response.ok) throw new Error("Falha ao buscar escolas.");
            const data = await response.json();
            setEscolas(data.escolas || []);
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleSubmitEscola = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsSubmittingEscola(true);
        setError(null);
        const url = escolaEditando ? `${API_URL}/escola/${escolaEditando.id_escola}` : `${API_URL}/escola`;
        const method = escolaEditando ? 'PUT' : 'POST';
        const body: any = { nome: nomeEscola, nome_usuario: nomeUsuario, senha: senha };
        if (!escolaEditando) {
            body.id_municipio = parseInt(idMunicipio, 10);
        }
        try {
            const response = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            const data = await response.json();
            if (!response.ok) throw new Error(data.mensagem || "Ocorreu um erro.");
            alert(data.mensagem);
            resetarFormularioEscola();
            fetchEscolas();
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSubmittingEscola(false);
        }
    };

    const handleDeletarEscola = async (id: number) => {
        if (!window.confirm("Tem certeza que deseja deletar esta escola?")) return;
        setError(null);
        try {
            const response = await fetch(`${API_URL}/escola/${id}`, { method: 'DELETE' });
            const data = await response.json();
            if (!response.ok) throw new Error(data.mensagem || "Erro ao deletar escola.");
            alert(data.mensagem);
            fetchEscolas();
        } catch (err: any) {
            setError(err.message);
        }
    };
    
    const iniciarEdicaoEscola = (escola: Escola) => {
        setEscolaEditando(escola);
        setNomeEscola(escola.nome);
        setNomeUsuario(escola.nome_usuario);
        setIdMunicipio(escola.id_municipio.toString());
        setSenha('');
        document.getElementById('form-escola')?.scrollIntoView({ behavior: 'smooth' });
    };

    const resetarFormularioEscola = () => {
        setEscolaEditando(null);
        setNomeEscola("");
        setIdMunicipio("");
        setNomeUsuario("");
        setSenha("");
    };

    // =============================================
    // Funções do CRUD de MATÉRIAS
    // =============================================
    const fetchMaterias = async (professorId: string) => {
        if (!professorId) {
            setMaterias([]);
            return;
        }
        try {
            const response = await fetch(`${API_URL}/materia/professor/${professorId}`);
            if (!response.ok) {
                // Se a resposta não for OK, limpa a lista e mostra um erro (mas não quebra a página)
                setMaterias([]);
                throw new Error(`Nenhuma matéria encontrada para o professor ID ${professorId} ou o serviço está indisponível.`);
            }
            const data = await response.json();
            setMaterias(data.materias || []);
        } catch (err: any) {
            setError(err.message);
            setMaterias([]);
        }
    };

    const handleSubmitMateria = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsSubmittingMateria(true);
        setError(null);
        const url = materiaEditando ? `${API_URL}/materia/${materiaEditando.id_materia}` : `${API_URL}/materia`;
        const method = materiaEditando ? 'PUT' : 'POST';
        const body = {
            nome: nomeMateria,
            id_disciplina: parseInt(idDisciplina, 10),
            id_professor: parseInt(idProfessor, 10)
        };
        try {
            const response = await fetch(url, { method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            const data = await response.json();
            if (!response.ok) throw new Error(data.mensagem || "Ocorreu um erro na operação com matéria.");
            alert(data.mensagem);
            resetarFormularioMateria();
            fetchMaterias(idProfessor); // Recarrega a lista do professor que acabou de ser editado/criado
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSubmittingMateria(false);
        }
    };

    const handleDeletarMateria = async (id: number) => {
        if (!window.confirm("Tem certeza que deseja deletar esta matéria?")) return;
        setError(null);
        try {
            const response = await fetch(`${API_URL}/materia/${id}`, { method: 'DELETE' });
            const data = await response.json();
            if (!response.ok) throw new Error(data.mensagem || "Erro ao deletar matéria.");
            alert(data.mensagem);
            fetchMaterias(idProfessorFiltro); // Recarrega a lista do filtro atual
        } catch (err: any) {
            setError(err.message);
        }
    };

    const iniciarEdicaoMateria = (materia: Materia) => {
        setMateriaEditando(materia);
        setNomeMateria(materia.nome);
        setIdDisciplina(materia.id_disciplina.toString());
        setIdProfessor(materia.id_professor.toString());
        document.getElementById('form-materia')?.scrollIntoView({ behavior: 'smooth' });
    };

    const resetarFormularioMateria = () => {
        setMateriaEditando(null);
        setNomeMateria("");
        setIdDisciplina("");
        setIdProfessor("");
    };

    // =============================================
    // useEffect com a correção para não travar a tela
    // =============================================
    useEffect(() => {
        const carregarDados = async () => {
            setIsLoading(true);
            setError(null);

            // Buscamos os dados separadamente para que um erro não bloqueie o outro.
            await fetchEscolas(); 
            await fetchMaterias(idProfessorFiltro);
            
            // Ao final de tudo, removemos o "Carregando..."
            setIsLoading(false);
        };
        carregarDados();
    }, []);

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] min-h-screen pt-32 pb-16 flex flex-col items-center">
                <main className="font-[Jomolhari] bg-white border-[#A7C1A8] w-11/12 max-w-4xl p-8 rounded-3xl shadow-lg border-4 flex flex-col items-center">
                    <div className="w-full flex justify-between items-center mb-8">
                        <h1 className="text-[#EEA03D] text-5xl">Painel do Município</h1>
                        <Link href="/dashboard" className="py-2 px-6 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition-colors text-lg">Ver Dashboard</Link>
                    </div>

                    {error && <div className="w-full mb-4 p-4 bg-red-200 text-red-800 rounded-lg">{error}</div>}
                    
                    {/* --- Seção de Escolas --- */}
                    <div id="form-escola" className="w-full">
                        <h2 className="text-[#EEA03D] text-4xl mb-6 text-center">{escolaEditando ? `Editando Escola: ${escolaEditando.nome}` : "Adicionar Nova Escola"}</h2>
                        <form onSubmit={handleSubmitEscola} className="w-full flex flex-col items-center">
                            <div className="w-full md:w-3/4 grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div><h5 className="mb-px text-gray-700">Nome da Escola</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="text" value={nomeEscola} onChange={e => setNomeEscola(e.target.value)} required /></div>
                                <div><h5 className="mb-px text-gray-700">ID do Município</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded disabled:bg-gray-300" type="number" value={idMunicipio} onChange={e => setIdMunicipio(e.target.value)} required disabled={!!escolaEditando} /></div>
                                <div><h5 className="mb-px text-gray-700">Nome de Usuário</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="text" value={nomeUsuario} onChange={e => setNomeUsuario(e.target.value)} required /></div>
                                <div><h5 className="mb-px text-gray-700">Senha</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="password" value={senha} onChange={e => setSenha(e.target.value)} placeholder={escolaEditando ? "Deixe em branco para não alterar" : ""} required={!escolaEditando} /></div>
                            </div>
                            <div className="flex gap-4 mt-6">
                                <span className="flex flex-col items-center p-2 bg-[#727D73] rounded-xl shadow-md">
                                    <button type="submit" className="cursor-pointer py-2 px-10 bg-[#D0DDD0] rounded-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled={isSubmittingEscola}>{isSubmittingEscola ? "Salvando..." : (escolaEditando ? "Salvar Alterações" : "Adicionar Escola")}</button>
                                </span>
                                {escolaEditando && (<button type="button" onClick={resetarFormularioEscola} className="cursor-pointer py-2 px-10 bg-gray-300 rounded-lg shadow-md">Cancelar Edição</button>)}
                            </div>
                        </form>
                        <hr className="w-full my-10 border-t-2 border-[#A7C1A8]" />
                        <h2 className="text-[#EEA03D] text-4xl mb-6 text-center">Escolas Cadastradas</h2>
                        <div className="w-full">{isLoading ? <p>Carregando escolas...</p> : escolas.length === 0 ? <p>Nenhuma escola cadastrada.</p> : escolas.map(escola => (<div key={escola.id_escola} className="flex justify-between items-center bg-gray-100 p-4 rounded-lg shadow-sm mb-4"><div><p className="font-bold text-lg text-gray-800">{escola.nome}</p><p className="text-sm text-gray-600">Usuário: {escola.nome_usuario} | Município ID: {escola.id_municipio}</p></div><div className="flex gap-3"><button onClick={() => iniciarEdicaoEscola(escola)} className="py-1 px-4 bg-blue-500 text-white rounded hover:bg-blue-600">Editar</button><button onClick={() => handleDeletarEscola(escola.id_escola)} className="py-1 px-4 bg-red-500 text-white rounded hover:bg-red-600">Deletar</button></div></div>))}</div>
                    </div>

                    <hr className="w-full my-12 border-t-4 border-double border-[#727D73]" />

                    {/* --- Seção de Matérias --- */}
                    <div id="form-materia" className="w-full">
                        <h2 className="text-[#EEA03D] text-4xl mb-6 text-center">{materiaEditando ? `Editando Matéria` : "Adicionar Nova Matéria"}</h2>
                        <form onSubmit={handleSubmitMateria} className="w-full flex flex-col items-center">
                            <div className="w-full md:w-3/4 grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div><h5 className="mb-px text-gray-700">Nome da Matéria</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="text" value={nomeMateria} onChange={e => setNomeMateria(e.target.value)} required /></div>
                                <div><h5 className="mb-px text-gray-700">ID da Disciplina</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="number" value={idDisciplina} onChange={e => setIdDisciplina(e.target.value)} required /></div>
                                <div><h5 className="mb-px text-gray-700">ID do Professor</h5><input className="bg-[#A7C1A8] pl-2 w-full h-10 rounded" type="number" value={idProfessor} onChange={e => setIdProfessor(e.target.value)} required /></div>
                            </div>
                            <div className="flex gap-4 mt-6">
                                <span className="flex flex-col items-center p-2 bg-[#727D73] rounded-xl shadow-md">
                                    <button type="submit" className="cursor-pointer py-2 px-10 bg-[#D0DDD0] rounded-sm disabled:bg-gray-400 disabled:cursor-not-allowed" disabled={isSubmittingMateria}>{isSubmittingMateria ? "Salvando..." : (materiaEditando ? "Salvar Alterações" : "Adicionar Matéria")}</button>
                                </span>
                                {materiaEditando && (<button type="button" onClick={resetarFormularioMateria} className="cursor-pointer py-2 px-10 bg-gray-300 rounded-lg shadow-md">Cancelar Edição</button>)}
                            </div>
                        </form>
                        <hr className="w-full my-10 border-t-2 border-[#A7C1A8]" />
                        <h2 className="text-[#EEA03D] text-4xl mb-6 text-center">Matérias Cadastradas</h2>
                        <div className="w-full flex justify-center items-center gap-4 mb-6">
                            <label htmlFor="filtro-prof" className="text-gray-700">Exibir matérias do Professor (ID):</label>
                            <input id="filtro-prof" className="bg-gray-200 pl-2 w-24 h-10 rounded" type="number" value={idProfessorFiltro} onChange={e => setIdProfessorFiltro(e.target.value)} />
                            <button onClick={() => fetchMaterias(idProfessorFiltro)} className="py-2 px-5 bg-green-600 text-white rounded hover:bg-green-700">Buscar</button>
                        </div>
                        <div className="w-full">{isLoading ? <p>Carregando matérias...</p> : materias.length === 0 ? <p>Nenhuma matéria encontrada para este professor.</p> : materias.map(materia => (<div key={materia.id_materia} className="flex justify-between items-center bg-gray-100 p-4 rounded-lg shadow-sm mb-4"><div><p className="font-bold text-lg text-gray-800">{materia.nome}</p><p className="text-sm text-gray-600">Disciplina ID: {materia.id_disciplina} | Professor ID: {materia.id_professor}</p></div><div className="flex gap-3"><button onClick={() => iniciarEdicaoMateria(materia)} className="py-1 px-4 bg-blue-500 text-white rounded hover:bg-blue-600">Editar</button><button onClick={() => handleDeletarMateria(materia.id_materia)} className="py-1 px-4 bg-red-500 text-white rounded hover:bg-red-600">Deletar</button></div></div>))}</div>
                    </div>
                </main>
            </div>
        </>
    );
}