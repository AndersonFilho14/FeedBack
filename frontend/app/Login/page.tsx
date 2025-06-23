"use client";
import React,{useState} from "react";
import Link from "next/link";
import { link } from "fs";

export default function Login() {
    const [user, setUser] = useState("");
    const [password, setPassword] = useState("");
    const [mensagem, setMensagem] = useState("");

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
        const response = await fetch(`http://127.0.0.1:5000/acesso/${user}/${password}`);
        if (!response.ok) {
            setMensagem("Usuário ou senha inválidos.");
            return;
        }
        const data = await response.json();
        if (data.nome) {
            window.location.href = "/AdicaoAlunos";
        } else {
            setMensagem("Usuário ou senha inválidos.");
        }
    } catch {
        setMensagem("Erro ao processar resposta do servidor.");
    }
};

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex justify-center items-center h-screen ">
                <main className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-96 h-140  rounded-3xl shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)]  flex flex-col items-center border-11 ">
                    <h1 className="text-[#EEA03D]  mt-16 mb-16 text-6xl ">Bem Vindo!</h1>
                    <form onSubmit={handleLogin} className="flex flex-col items-center w-full">
                        <h5 className="mb-px">Usuario</h5>
                        <input
                            className="bg-[#A7C1A8] mb-4 pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                            type="text"
                            name="User"
                            value={user}
                            onChange={e => setUser(e.target.value)}
                            required
                        />
                        <h5>Senha</h5>
                        <input
                            className=" bg-[#A7C1A8] mb-4 pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                            type="password"
                            name="password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            required
                        />
                        <span className=" cursor-pointer mt-4 flex flex-col items-center p-[7] bg-[#727D73] rounded-xl shadow-[0_4px_20px_0_rgba(0,0,0,0.25)]">
                            <button type="submit" className=" cursor-pointer pt-2 pb-2 pl-14 pr-14 bg-[#D0DDD0] border-[#727D73] rounded-sm">Entrar</button>
                        </span>
                    </form>
                    <Link
                        href="/CordenacaoCadastro"
                        className="mt-4 px-6 py-2 bg-[#EEA03D] text-white rounded shadow hover:bg-[#d18a2c] transition"
                    >
                        Registrar-se
                    </Link>                  
                    {mensagem && (
                        <div className="mt-4 text-red-600">{mensagem}</div>
                    )}
                </main>
            </div>
        </>
    );
}