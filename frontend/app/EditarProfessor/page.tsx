"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

interface ProfessorData {
    nome: string;
    cpf: string;
    cargo: string;
    data_nascimento: string;
    nacionalidade: string;
    estado_civil: string;
    telefone: string;
    email: string;
    sexo: string;
    senha?: string;
}

export default function EditarProfessor() {
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [nome, setNome] = useState("");
    const [data, setData] = useState("");
    const [sexo, setSexo] = useState("");
    const [cpf, setCpf] = useState("");
    const [nacionalidade, setNacionalidade] = useState("");
    const [estadoCivil, setEstadoCivil] = useState("");
    const [cargo, setCargo] = useState("");
    const [telefone, setTelefone] = useState("");

    const searchParams = useSearchParams();
    const professorId = searchParams.get("id");

    const [loading, setLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    // ✅ FUNÇÃO DE MÁSCARA DE CPF CORRIGIDA E REUTILIZÁVEL
    const formatCpf = (cpfStr: string) => {
        let value = cpfStr.replace(/\D/g, "").substring(0, 11);
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d)/, "$1.$2");
        value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        return value;
    };

    // ✅ FUNÇÃO DE MÁSCARA DE TELEFONE REUTILIZÁVEL
    const formatTelefone = (telStr: string) => {
        return telStr
            .replace(/\D/g, '')
            .replace(/^(\d{2})(\d)/, '($1) $2')
            .replace(/(\d{5})(\d)/, '$1-$2')
            .slice(0, 15);
    };

    const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCpf(formatCpf(e.target.value));
    };

    const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTelefone(formatTelefone(e.target.value));
    };

    useEffect(() => {
        if (!professorId) {
            setError("ID do professor não encontrado.");
            setLoading(false);
            return;
        }

        async function fetchProfessor() {
            setLoading(true);
            try {
                const response = await fetch(`http://localhost:5000/professores/escola/1`);
                if (!response.ok) throw new Error("Falha ao buscar a lista de professores.");
                
                const data = await response.json();
                const professor = data.professores?.find((p: any) => p.id.toString() === professorId);

                if (!professor) throw new Error("Professor não encontrado.");

                // Preenche o formulário com os dados formatados
                setNome(professor.nome || "");
                setCpf(formatCpf(professor.cpf || "")); // Aplica a máscara
                setCargo(professor.cargo || "");
                setData(professor.data_nascimento ? professor.data_nascimento.split('T')[0] : "");
                setNacionalidade(professor.nacionalidade || "");
                setEstadoCivil(professor.estado_civil || "");
                setTelefone(formatTelefone(professor.telefone || "")); // Aplica a máscara
                setEmail(professor.email || "");
                setSexo(professor.sexo || "");

            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchProfessor();
    }, [professorId]);

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!professorId) {
            setError("Não é possível salvar sem um ID de professor.");
            return;
        }

        setIsSaving(true);
        setError(null);
        setMessage(null);

        const professorData: ProfessorData = {
            nome,
            cpf: cpf.replace(/\D/g, ''),
            cargo,
            data_nascimento: data,
            nacionalidade,
            estado_civil: estadoCivil,
            telefone: telefone.replace(/\D/g, ''),
            email,
            sexo,
        };

        if (password) {
            professorData.senha = password;
        }

        try {
            const response = await fetch(`http://localhost:5000/professor/${professorId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(professorData),
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.mensagem || "Falha ao atualizar o professor.");
            setMessage(result.mensagem);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto max-w-7xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-8 justify-center items-center border-11">
                    <h1 className="text-[#EEA03D] text-5xl">Editar Cadastro do Professor</h1>
                    
                    {loading && <p>Carregando dados do professor...</p>}
                    {error && <p className="text-red-500 text-center -my-4">{error}</p>}
                    {message && <p className="text-green-600 text-center -my-4">{message}</p>}

                    {!loading && !error && (
                        <form className="flex flex-col items-center gap-10" onSubmit={handleSave}>
                            <div className="flex flex-wrap justify-center items-start gap-10 md:gap-30">
                                {/* Coluna da Esquerda */}
                                <div className="flex flex-col gap-4">
                                    <h5>Nome</h5>
                                    <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="text" value={nome} onChange={e => setNome(e.target.value)} required />
                                    <h5>Data de Nascimento</h5>
                                    <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="date" value={data} onChange={e => setData(e.target.value)} required />
                                    <h5>Sexo</h5>
                                    <div className="flex gap-4 items-center">
                                        {/* ✅ CAMPO DE SEXO CORRIGIDO PARA RADIO */}
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
                                    <h5>Usuário(obrigatorio)</h5>
                                    <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="usuario" value={email} onChange={e => setEmail(e.target.value)} required />
                                    <h5>Nova Senha (obrigatorio)</h5>
                                    <input className="w-80 h-10 bg-[#A7C1A8] rounded px-3 shadow-inner" type="password" value={password} onChange={e => setPassword(e.target.value)} required/>
                                </div>
                            </div>
                            
                            {/* ✅ BOTÕES DENTRO DO FORM */}
                            <div className="flex flex-col items-center gap-4 mt-6">
                                <button
                                    type="submit"
                                    disabled={isSaving || loading || !!error}
                                    className="w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed"
                                >
                                    {isSaving ? "Salvando..." : "Salvar Alterações"}
                                </button>
                                <Link className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl text-black" href={"/ListaProfessores"}>
                                    Voltar
                                </Link>
                            </div>
                        </form>
                    )}
                </div>
            </div>
        </>
    );
}