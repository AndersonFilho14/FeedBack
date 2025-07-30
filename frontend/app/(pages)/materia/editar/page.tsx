"use client";

import { useSearchParams, useRouter } from "next/navigation";
import React, { useEffect, useState, FormEvent } from "react";
import Link from 'next/link';

// Interface para os dados da matéria
interface Materia {
    id: number;
    nome: string;
    id_disciplina: number;
    id_professor: number;
}

function EditarMateriaPage() {
    const router = useRouter();
    const searchParams = useSearchParams();

    // Estado para os campos do formulário
    const [nome, setNome] = useState('');
    const [idDisciplina, setIdDisciplina] = useState('');
    const [idProfessor, setIdProfessor] = useState('');
    
    // Estado para controle da UI (carregamento, erros, etc.)
    const [materiaId, setMateriaId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    // Efeito para carregar os dados da matéria ao iniciar a tela
    useEffect(() => {
        const id = searchParams.get('materiaId');
        if (!id) {
            alert("ID da matéria não fornecido.");
            router.push('/materia'); // Volta para a lista se não houver ID
            return;
        }

        setMateriaId(id);
        setLoading(true);
        
        fetch(`http://localhost:5000/materia/${id}`)
            .then(res => {
                if (!res.ok) throw new Error("Falha ao carregar os dados da matéria.");
                return res.json();
            })
            .then((data: Materia) => {
                setNome(data.nome);
                setIdDisciplina(String(data.id_disciplina));
                setIdProfessor(String(data.id_professor));
            })
            .catch(err => {
                setError(err.message);
            })
            .finally(() => {
                setLoading(false);
            });
    }, [searchParams, router]);

    // Função para salvar as alterações
    const handleSave = async (event: FormEvent) => {
        event.preventDefault();
        if (!materiaId) return;

        setIsSaving(true);
        setError(null);
        setMessage(null);

        // Somente o campo 'nome' é enviado, conforme a definição da sua API
        const dataToUpdate = {
            nome,
            // Adicione outros campos aqui se a API os aceitar
            // id_disciplina: Number(idDisciplina), 
            // id_professor: Number(idProfessor),
        };

        try {
            const response = await fetch(`http://localhost:5000/materia/${materiaId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToUpdate)
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.mensagem || "Erro ao salvar as alterações.");
            }
            setMessage(result.mensagem || "Alterações salvas com sucesso!");
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50 flex items-center justify-center">
                IMD-IA
            </header>

            <main className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-32 px-4">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-[90%] max-w-4xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-5xl text-center">Editar Matéria</h1>
                    
                    {loading && <p className="text-center text-lg text-[#727D73]">Carregando dados da matéria... ⏳</p>}
                    {error && <p className="text-red-600 bg-red-100 p-3 rounded-md text-center font-semibold">{error}</p>}
                    {message && <p className="text-green-700 bg-green-100 p-3 rounded-md text-center font-semibold">{message}</p>}

                    {!loading && !error && (
                        <form className="flex flex-col gap-8" onSubmit={handleSave}>
                           
                                <div>
                                    <h5>Nome da Matéria</h5>
                                    <input 
                                        className="w-full h-12 bg-[#A7C1A8] rounded px-3 text-lg" 
                                        type="text" 
                                        value={nome} 
                                        onChange={e => setNome(e.target.value)} 
                                        required 
                                    />
                                </div>
                                
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-4">
                                <Link className="w-full sm:w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl text-black order-2 sm:order-1" href={"/materia"}>
                                    Voltar
                                </Link>
                                <button type="submit" disabled={isSaving || loading} className="w-full sm:w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed disabled:text-gray-600 order-1 sm:order-2">
                                    {isSaving ? "Salvando..." : "Salvar Alterações"}
                                </button>
                            </div>
                        </form>
                    )}
                </div>
            </main>
        </>
    );
}

export default EditarMateriaPage;