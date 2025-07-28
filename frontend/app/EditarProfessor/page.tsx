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
    senha?: string; // Senha é opcional na atualização
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

    useEffect(() => {
        if (!professorId) {
            setError("ID do professor não encontrado.");
            setLoading(false);
            return;
        }

        async function fetchProfessor() {
            setLoading(true);
            try {
                // 1. Buscamos na rota que lista todos os professores, pois a rota para um professor específico não existe.
                const response = await fetch(`http://localhost:5000/professores/escola/1`); // Assumindo escola ID 1
                if (!response.ok) {
                    throw new Error("Falha ao buscar a lista de professores.");
                }
                const data = await response.json();

                // 2. Encontramos o professor correto na lista retornada pela API.
                const professor = data.professores?.find((p: any) => p.id.toString() === professorId);

                if (!professor) {
                    throw new Error("Professor com o ID especificado não foi encontrado.");
                }
 
                // 3. Preenchemos o formulário com os dados encontrados.
                setNome(professor.nome || "");
                setCpf(professor.cpf || "");
                setCargo(professor.cargo || "");
                setData(professor.data_nascimento ? professor.data_nascimento.split('T')[0] : "");
                setNacionalidade(professor.nacionalidade || "");
                setEstadoCivil(professor.estado_civil || "");
                setTelefone(professor.telefone || "");
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

    // 4. Adicionando máscaras para CPF e Telefone para consistência
    const handleCpfChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
          .replace(/\D/g, '')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
          .slice(0, 14);
        setCpf(value);
    };

    const handleTelefoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value
          .replace(/\D/g, '')
          .replace(/^(\d{2})(\d)/, '($1) $2')
          .replace(/(\d{5})(\d)/, '$1-$2')
          .slice(0, 15);
        setTelefone(value);
    };

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
            cpf: cpf.replace(/\D/g, ''), // Remove a máscara antes de enviar
            cargo,
            data_nascimento: data,
            nacionalidade,
            estado_civil: estadoCivil,
            telefone: telefone.replace(/\D/g, ''), // Remove a máscara antes de enviar
            email,
            sexo,
        };

        // Só inclua a senha no payload se ela foi alterada
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
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-330 h-200  rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col gap-8 justify-center items-center mt-22  border-11 ">
                    
                    <h1 className="text-[#EEA03D] text-5xl ">Editar cadastro professor</h1>
                    {loading && <p>Carregando dados do professor...</p>}
                    {error && <p className="text-red-500 text-center -my-4">{error}</p>}
                    {message && <p className="text-green-600 text-center -my-4">{message}</p>}

                    {!loading && !error && (
                    <form className="flex  justify-center items-center gap-30 " onSubmit={handleSave}>
                        <div className="flex flex-col gap-4">
                            <h5>Nome</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" alt="nome" value={nome} onChange={e => setNome(e.target.value)} />
                            <h5>Data</h5>
                            <input
                                className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                                type="date"
                                alt="data"
                                value={data}
                                onChange={e => setData(e.target.value)}
                            />
                            
                            <h5>Sexo</h5>
                            <div className="flex gap-4 items-center">
                                <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.10)] cursor-pointer transition-all duration-200 hover:bg-[#8FAE91]">
                                    <input
                                        type="checkbox"
                                        checked={sexo === "masculino"}
                                        onChange={() => setSexo(sexo === "masculino" ? "" : "masculino")}
                                        className="mr-2 accent-[#EEA03D] w-5 h-5 rounded focus:ring-2 focus:ring-[#EEA03D] transition-all duration-200"
                                    />
                                    <span className=" text-lg ">Masculino</span>
                                </label>
                                <label className="flex items-center bg-[#A7C1A8] px-4 py-2 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.10)] cursor-pointer transition-all duration-200 hover:bg-[#8FAE91]">
                                    <input
                                        type="checkbox"
                                        checked={sexo === "feminino"}
                                        onChange={() => setSexo(sexo === "feminino" ? "" : "feminino")}
                                        className="mr-2 accent-[#EEA03D] w-5 h-5 rounded focus:ring-2 focus:ring-[#EEA03D] transition-all duration-200"
                                    />
                                    <span className=" text-lg ">Feminino</span>
                                </label>
                            </div>
                            <h5>Cpf</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="cpf" id="" value={cpf} onChange={handleCpfChange} placeholder="000.000.000-00" />
                            <h5>Nacionalidade</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="nacionalidade" value={nacionalidade} onChange={e => setNacionalidade(e.target.value)} />
                        </div>
                        <div className="flex flex-col gap-4">
                            <h5>Estado Civil</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="Nome mae" id="" value={estadoCivil} onChange={e => setEstadoCivil(e.target.value)} />
                            <h5>Cargo</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="Nome pai" id="" value={cargo} onChange={e => setCargo(e.target.value)} />
                            <h5>Telefone </h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="Telefone responsavel" id="" value={telefone} onChange={handleTelefoneChange} placeholder="(00) 00000-0000" />
                            <h5>Usuario</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="usuario" name="usuario" id="" value={email} onChange={e => setEmail(e.target.value)} />
                            <h5>Nova Senha (deixe em branco para não alterar)</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="password" name="senha para login" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" />
                        </div>
                    </form>
                    )}
                    <button 
                        type="submit" 
                        onClick={handleSave}
                        disabled={isSaving || loading || !!error}
                        className="w-100 h-19 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed"
                    >
                        {isSaving ? "Salvando..." : "Salvar"}
                    </button>
                    <Link className=" w-44 h-13 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl " href={"/ListaProfessores"}>Voltar</Link>
                </div>
                
            </div>

        </>
    );
}
