"use client";
import React,{useState} from "react";
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
        setTelefone(value);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMensagem(""); // Limpa mensagens anteriores

        const novoProfessor = {
            nome,
            cpf: cpf.replace(/\D/g, ''), // Remove a máscara do CPF
            cargo,
            id_escola: 1, // Assumindo um valor fixo para id_escola por enquanto
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
                setMensagem(data.mensagem); // Exibe a mensagem de sucesso do backend
                // Opcional: Limpar os campos após o cadastro
                setNome("");
                setCpf("");
                // ... limpa os outros campos também
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
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-330 h-200  rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col gap-8 justify-center items-center mt-22  border-11 ">
                    <h1 className="text-[#EEA03D] text-5xl ">Cadastrar Novo Professor</h1>
                    <form className="flex  justify-center items-center gap-30 " onSubmit={handleSubmit}>
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
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="Usuario" name="Usuario" id="" value={Usuario} onChange={e => setUsuario(e.target.value)} />
                            <h5>Senha para login</h5>
                            <input className="w-80 h-10 bg-[#A7C1A8] rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]" type="password" name="senha para login" value={password} onChange={e => setPassword(e.target.value)} />
                        </div>
                    </form>
                    {mensagem && <p>{mensagem}</p>}
                    <button type="submit" onClick={handleSubmit} className="w-100 h-19 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl">Cadastrar</button>
                    <Link className=" w-44 h-13 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl " href={"/ListaProfessores"}>Voltar</Link>
                </div>
                
            </div>

        </>
    );
}
