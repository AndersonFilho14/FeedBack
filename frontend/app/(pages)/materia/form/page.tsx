"use client";

import { useRouter } from "next/navigation";
import React, { useState, FormEvent } from "react";
import Link from 'next/link';

function CadastrarMateriaPage() {
    const router = useRouter();

    // Estado para o campo do formulário
    const [nome, setNome] = useState('');
    
    // Estado para controle da UI
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    // Função para lidar com o envio do formulário de criação
    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        setIsSubmitting(true);
        setError(null);
        setMessage(null);

        // O corpo da requisição envia apenas o nome, conforme a API
        const dataToCreate = { nome };

        try {
            const response = await fetch(`http://localhost:5000/materia`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToCreate)
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.mensagem || "Erro ao criar a matéria.");
            }
            // Limpa o formulário e exibe a mensagem de sucesso
            setMessage(result.mensagem || "Matéria criada com sucesso!");
            setNome(''); 
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50 flex items-center justify-center">
                IMD-IA
            </header>

            <main className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-32 px-4">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-[90%] max-w-4xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-6 border-11">
                    <h1 className="text-[#EEA03D] text-5xl text-center">Cadastrar Nova Matéria</h1>
                    
                    {error && <p className="text-red-600 bg-red-100 p-3 rounded-md text-center font-semibold">{error}</p>}
                    {message && <p className="text-green-700 bg-green-100 p-3 rounded-md text-center font-semibold">{message}</p>}

                    <form className="flex flex-col gap-8" onSubmit={handleSubmit}>
                        <fieldset>
                            {/* Nome da Matéria */}
                            <div>
                                <h5>Nome da Matéria</h5>
                                <input 
                                    className="w-full h-12 bg-[#A7C1A8] rounded px-3 text-lg" 
                                    type="text" 
                                    name="nome"
                                    value={nome} 
                                    onChange={e => setNome(e.target.value)} 
                                    required 
                                />
                            </div>
                        </fieldset>
                        
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-4">
                            <Link className="w-full sm:w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl text-black order-2 sm:order-1" href={"/materia"}>
                                Voltar
                            </Link>
                            <button type="submit" name="Cadastrar" disabled={isSubmitting} className="w-full sm:w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed disabled:text-gray-600 order-1 sm:order-2">
                                {isSubmitting ? "Cadastrando..." : "Cadastrar"}
                            </button>
                        </div>
                    </form>
                </div>
            </main>
        </>
    );
}

export default CadastrarMateriaPage;