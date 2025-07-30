"use client";
import React, { useState } from "react";
import Link from "next/link";

export default function CadastrarProfessor() {
    const [password, setPassword] = useState("");
    const [Usuario, setUsuario] = useState("");
    const [nome, setNome] = useState("");
    const [data, setData] = useState("");
    const [sexo, setSexo] = useState("");
    const [cpf, setCpf] = useState("");
    const [nacionalidade, setNacionalidade] = useState("");
    const [estadoCivil, setEstadoCivil] = useState("");
    const [cargo, setCargo] = useState("");
    const [telefone, setTelefone] = useState("");
    const [mensagem, setMensagem] = useState("");

    // ✅ FUNÇÃO CORRIGIDA
    const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        let value = e.target.value;
        // 1. Remove tudo que não é dígito
        value = value.replace(/\D/g, "");
        // 2. Limita para 11 dígitos (tamanho do CPF)
        value = value.substring(0, 11);
        // 3. Aplica a máscara de forma progressiva
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        setCpf(value);
    };

    const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
          .replace(/\D/g, '') // Remove todos os caracteres não numéricos
          .replace(/^(\d{2})(\d)/, '($1) $2') // Coloca parênteses em volta dos dois primeiros dígitos
          .replace(/(\d{5})(\d)/, '$1-$2') // Coloca um hífen após os próximos cinco dígitos
          .slice(0, 15); // Limita ao tamanho máximo da máscara (XX) XXXXX-XXXX
        setTelefone(value);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMensagem(""); // Limpa mensagens anteriores

        const novoProfessor = {
            nome,
            cpf: cpf.replace(/\D/g, ''), // Remove a máscara do CPF
            cargo,
            id_escola: 1, // Assumindo um valor fixo para id_escola
            nacionalidade,
            estado_civil: estadoCivil,
            telefone: telefone.replace(/\D/g, ''), // Remove a máscara do telefone
            email: Usuario,
            senha: password,
            data_nascimento: data,
            sexo,
        };

        try {
            const response = await fetch("http://localhost:5000/professor", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(novoProfessor),
            });

            const data = await response.json();

            if (response.ok) {
                setMensagem(data.mensagem);
                setNome("");
                setCpf("");
                setTelefone("");
                // ... limpe os outros campos se desejar
            } else {
                setMensagem(data.mensagem || "Erro ao cadastrar professor.");
            }
        } catch (error) {
            setMensagem("Erro ao conectar com o servidor.");
        }
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto max-w-7xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-8 justify-center items-center border-11">
                    <h1 className="text-[#EEA03D] text-5xl">Cadastrar Novo Professor</h1>
                    
                    {/* ✅ FORMULARIO AGORA ENVOLVE OS BOTÕES */}
                    <form className="flex flex-col items-center gap-10" onSubmit={handleSubmit}>
                        <div className="flex flex-wrap justify-center items-start gap-10 md:gap-30">
                            {/* Coluna da Esquerda */}
                            <div className="flex flex-col gap-4">
                                <h5>Nome</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={nome} onChange={e => setNome(e.target.value)} required />
                                <h5>Data de Nascimento</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="date" value={data} onChange={e => setData(e.target.value)} required />
                                <h5>Sexo</h5>
                                <div className="flex gap-4 items-center">
                                    <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-md cursor-pointer hover:bg-[#8FAE91]">
                                        <input type="radio" name="sexo" checked={sexo === "masculino"} onChange={() => setSexo("masculino")} className="mr-2 accent-[#EEA03D] w-5 h-5"/>
                                        <span className="text-lg">Masculino</span>
                                    </label>
                                    <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-md cursor-pointer hover:bg-[#8FAE91]">
                                        <input type="radio" name="sexo" checked={sexo === "feminino"} onChange={() => setSexo("feminino")} className="mr-2 accent-[#EEA03D] w-5 h-5"/>
                                        <span className="text-lg">Feminino</span>
                                    </label>
                                </div>
                                <h5>CPF</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={cpf} onChange={handleCpfChange} placeholder="000.000.000-00" required />
                                <h5>Nacionalidade</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={nacionalidade} onChange={e => setNacionalidade(e.target.value)} required />
                            </div>
                            {/* Coluna da Direita */}
                            <div className="flex flex-col gap-4">
                                <h5>Estado Civil</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={estadoCivil} onChange={e => setEstadoCivil(e.target.value)} required />
                                <h5>Cargo</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={cargo} onChange={e => setCargo(e.target.value)} required />
                                <h5>Telefone</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={telefone} onChange={handleTelefoneChange} placeholder="(00) 00000-0000" required />
                                <h5> (Usuário)</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="usuario" value={Usuario} onChange={e => setUsuario(e.target.value)} required />
                                <h5>Senha para login</h5>
                                <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
                            </div>
                        </div>
                        
                        {mensagem && <p className="text-center text-lg mt-4 p-2 bg-green-100 text-green-800 rounded">{mensagem}</p>}
                        
                        {/* ✅ BOTÃO DENTRO DO FORM */}
                        <div className="flex flex-col items-center gap-4 mt-6">
                            <button type="submit" className="w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl">
                                Cadastrar
                            </button>
                            <Link className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl text-black" href={"/ListaProfessores"}>
                                Voltar
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}