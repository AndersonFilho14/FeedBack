"use client";
import React, { useState } from "react";
import { useRouter } from 'next/navigation';

export default function Login() {
    const [user, setUser] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);

        try {
            const response = await fetch(`http://127.0.0.1:5000/acesso/${user}/${password}`);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => null);
                throw new Error(errorData?.mensagem || "Usuário ou senha inválidos.");
            }

            const data = await response.json();
            // 1. Validar se os dados essenciais (id_user, cargo) foram recebidos
            if (data.id_user && data.cargo) {
                // 2. Armazenar os dados do usuário no localStorage para uso em outras páginas
                localStorage.setItem('userId', data.id_user);
                localStorage.setItem('userName', data.nome);
                localStorage.setItem('userCargo', data.cargo);
                if (data.token) localStorage.setItem('authToken', data.token);

                const cargo = data.cargo.toLowerCase();
                if (cargo === "professor") {
                    router.push("/InicialProfessor");
                } else if (cargo === "escola") {
                    router.push("/EdicaoEscola"); 
                } else if (cargo === "municipio") {
                    router.push("/EdicaoMunicipio");
                } else {
                    throw new Error("Cargo de usuário não reconhecido.");
                }
            } else {
                throw new Error("Resposta do servidor não contém os dados necessários para o login.");
            }
        } catch (err: any) {
            setError(err.message || "Erro ao conectar com o servidor.");
        } finally {
            setIsSubmitting(false);
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
                        <span className="mt-4 flex flex-col items-center p-[7px] bg-[#727D73] rounded-xl shadow-[0_4px_20px_0_rgba(0,0,0,0.25)]">
                            <button 
                                type="submit" 
                                className="cursor-pointer pt-2 pb-2 pl-14 pr-14 bg-[#D0DDD0] border-[#727D73] rounded-sm disabled:bg-gray-400 disabled:cursor-not-allowed"
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? "Entrando..." : "Entrar"}
                            </button>
                        </span>
                    </form>
                    {error && (
                        <div className="mt-4 text-red-600 font-semibold">{error}</div>
                    )}
                </main>
            </div>
        </>
    );
}