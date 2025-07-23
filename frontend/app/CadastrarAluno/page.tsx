"use client";
import React, { useState } from "react";
import Link from "next/link";

export default function CadastrarAluno() {
    // 1. Estados alinhados com a API de aluno
    const [nome, setNome] = useState("");
    const [cpf, setCpf] = useState("");
    const [data, setData] = useState("");
    const [sexo, setSexo] = useState("");
    const [nacionalidade, setNacionalidade] = useState("");
    const [nomeResponsavel, setNomeResponsavel] = useState("");
    const [telefoneResponsavel, setTelefoneResponsavel] = useState("");
    const [mensagem, setMensagem] = useState(""); // Estado para feedback

    // 2. Adicionada a máscara para o CPF
    const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
            .replace(/\D/g, '') // Remove todos os caracteres não numéricos
            .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto após o terceiro dígito
            .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto após o sexto dígito
            .replace(/(\d{3})(\d{1,2})$/, '$1-$2') // Coloca um hífen antes dos dois últimos dígitos
            .slice(0, 14); // Limita o tamanho
        setCpf(value);
    };

    const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
            .replace(/\D/g, '') // Remove todos os caracteres não numéricos
            .replace(/^(\d{2})(\d)/, '($1) $2') // Coloca parênteses em volta dos dois primeiros dígitos
            .replace(/(\d{5})(\d)/, '$1-$2') // Coloca um hífen após os próximos cinco dígitos
            .slice(0, 15); // Limita ao tamanho máximo da máscara (XX) XXXXX-XXXX
        setTelefoneResponsavel(value);
    };

    // 3. Função para submeter o formulário (handleSubmit)
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault(); // Impede o recarregamento da página
        setMensagem(""); // Limpa mensagens anteriores

        const novoAluno = {
            nome,
            cpf: cpf.replace(/\D/g, ''), // Envia o CPF sem a máscara
            data_nascimento: data,
            sexo,
            nacionalidade,
            id_escola: 1, // Valor fixo, conforme o exemplo do backend
            nome_responsavel: nomeResponsavel,
            numero_responsavel: telefoneResponsavel.replace(/\D/g, ''), // Envia o telefone sem a máscara
        };

        try {
            const response = await fetch("http://localhost:5000/aluno", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(novoAluno),
            });

            const data = await response.json();

            if (response.ok) {
                setMensagem(data.mensagem || "Aluno cadastrado com sucesso!");
                // Limpa os campos do formulário
                setNome("");
                setCpf("");
                setData("");
                setSexo("");
                setNacionalidade("");
                setNomeResponsavel("");
                setTelefoneResponsavel("");
            } else {
                setMensagem(data.mensagem || "Erro ao cadastrar aluno.");
            }
        } catch (error) {
            console.error("Erro de conexão:", error);
            setMensagem("Não foi possível conectar ao servidor. Tente novamente mais tarde.");
        }
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto max-w-6xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-8 justify-center items-center border-11">
                    <h1 className="text-[#EEA03D] text-5xl">Cadastrar Novo Aluno</h1>
                    {/* 4. Conectado o formulário à função handleSubmit */}
                    <form className="flex flex-wrap justify-center items-start gap-x-30 gap-y-4" onSubmit={handleSubmit}>
                        <div className="flex flex-col gap-4">
                            <h5>Nome</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="text" alt="nome" value={nome} onChange={e => setNome(e.target.value)} required />
                            <h5>Data de Nascimento</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="date" alt="data" value={data} onChange={e => setData(e.target.value)} required />
                            <h5>Sexo</h5>
                            <div className="flex gap-4 items-center">
                                <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.10)] cursor-pointer">
                                    <input type="checkbox" checked={sexo === "masculino"} onChange={() => setSexo(sexo === "masculino" ? "" : "masculino")} className="mr-2 accent-[#EEA03D] w-5 h-5 rounded"/>
                                    <span className="text-lg">Masculino</span>
                                </label>
                                <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.10)] cursor-pointer">
                                    <input type="checkbox" checked={sexo === "feminino"} onChange={() => setSexo(sexo === "feminino" ? "" : "feminino")} className="mr-2 accent-[#EEA03D] w-5 h-5 rounded"/>
                                    <span className="text-lg">Feminino</span>
                                </label>
                            </div>
                            <h5>CPF</h5>
                            {/* 5. Usando o handleCpfChange e placeholder correto */}
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="text" value={cpf} onChange={handleCpfChange} placeholder="000.000.000-00" required />
                            <h5>Nacionalidade</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="text" value={nacionalidade} onChange={e => setNacionalidade(e.target.value)} required />
                        </div>
                        <div className="flex flex-col gap-4">
                            <h5>Nome do Responsável</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="text" value={nomeResponsavel} onChange={e => setNomeResponsavel(e.target.value)} required />
                            <h5>Telefone do Responsável</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] px-2" type="tel" value={telefoneResponsavel} onChange={handleTelefoneChange} placeholder="(00) 00000-0000" maxLength={15} required />
                        </div>
                        {/* 6. Movido o botão para dentro do form e a mensagem de feedback para fora */}
                        <div className="w-full flex flex-col items-center gap-4 mt-6">
                            {/* 7. Botão de cadastrar alterado de Link para button type="submit" */}
                            <button type="submit" className="w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl">
                                Cadastrar
                            </button>
                            {/* Exibe a mensagem de sucesso ou erro */}
                            {mensagem && <p className="text-xl text-center font-semibold text-[#727D73]">{mensagem}</p>}
                            <Link className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl" href={"/ListaAlunos"}>
                                Voltar
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}