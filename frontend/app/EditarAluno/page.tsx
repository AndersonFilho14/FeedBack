"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

interface AlunoData {
    nome: string;
    cpf: string;
    data_nascimento: string;
    sexo: string;
    nacionalidade: string;
    nome_responsavel: string;
    numero_responsavel: string;
}

export default function EditarAluno() {
    const [nome, setNome] = useState("");
    const [data, setData] = useState("");
    const [sexo, setSexo] = useState("");
    const [cpf, setCpf] = useState("");
    const [nacionalidade, setNacionalidade] = useState("");
    const [nomeResponsavel, setNomeResponsavel] = useState("");
    const [telefoneResponsavel, setTelefoneResponsavel] = useState("");

    const searchParams = useSearchParams();
    const alunoId = searchParams.get("id");

    const [loading, setLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [message, setMessage] = useState<string | null>(null);

    useEffect(() => {
        if (!alunoId) {
            setError("ID do aluno não encontrado.");
            setLoading(false);
            return;
        }

        async function fetchAluno() {
            setLoading(true);
            try {
                // Buscamos na rota que lista todos os alunos
                const response = await fetch(`http://localhost:5000/alunos/escola/1`);
                if (!response.ok) {
                    throw new Error("Falha ao buscar a lista de alunos.");
                }
                const data = await response.json();

                // Encontramos o aluno correto na lista
                const aluno = data.alunos?.find((a: any) => a.id.toString() === alunoId);

                if (!aluno) {
                    throw new Error("Aluno com o ID especificado não foi encontrado.");
                }

                // Preenchemos o formulário com os dados encontrados
                setNome(aluno.nome || "");
                setCpf(aluno.cpf || "");
                setData(aluno.data_nascimento ? aluno.data_nascimento.split('T')[0] : "");
                setSexo(aluno.sexo || "");
                setNacionalidade(aluno.nacionalidade || "");
                setNomeResponsavel(aluno.nome_responsavel || "");
                setTelefoneResponsavel(aluno.numero_responsavel || "");

            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchAluno();
    }, [alunoId]);

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

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!alunoId) {
            setError("Não é possível salvar sem um ID de aluno.");
            return;
        }

        setIsSaving(true);
        setError(null);
        setMessage(null);

        const alunoData: AlunoData = {
            nome,
            cpf: cpf.replace(/\D/g, ''),
            data_nascimento: data,
            sexo,
            nacionalidade,
            nome_responsavel: nomeResponsavel,
            numero_responsavel: telefoneResponsavel.replace(/\D/g, ''),
        };

        try {
            const response = await fetch(`http://localhost:5000/aluno/${alunoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(alunoData),
            });

            const result = await response.json();
            if (!response.ok) throw new Error(result.mensagem || "Falha ao atualizar o aluno.");
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
                    <h1 className="text-[#EEA03D] text-5xl ">Editar Cadastro do Aluno</h1>
                    {loading && <p>Carregando dados do aluno...</p>}
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
                            <h5>Nome do responsavel</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="text" name="Nome do responsavel" id="" value={nomeResponsavel} onChange={e => setNomeResponsavel(e.target.value)} />
                            
                            <h5>Telefone do responsavel</h5>
                            <input 
                                className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" 
                                type="tel" 
                                name="Telefone responsavel" 
                                id="" value={telefoneResponsavel} 
                                onChange={handleTelefoneChange} 
                                placeholder="(XX) XXXXX-XXXX" 
                                maxLength={15} />
                            
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
                    <Link className=" w-44 h-13 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl " href={"/ListaAlunos"}>Voltar</Link>
                </div>
                
            </div>

        </>
    );
}
