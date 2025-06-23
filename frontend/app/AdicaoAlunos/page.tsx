"use client";
import React, { useState } from "react";



export default function AdicaoAlunos() {
    const [form, setForm] = useState({
        nome: "",
        email: "",
        matricula: "",
        curso: "",
        nota: "",
        faltas: "",
    });
    const [mensagem, setMensagem] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Aqui você pode adicionar a lógica de envio para o backend
        setMensagem("Aluno cadastrado com sucesso!");
        setForm({ nome: "", email: "", matricula: "", curso: "", nota: "", faltas: "" });
    };

    const handleVoltar = () => {
        window.location.href = "/"; // Redireciona para a página inicial/login
    };

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center h-screen">
                <main className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-96 rounded-3xl shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] flex flex-col items-center border-11 py-8 mt-24">
                    <h1 className="text-[#EEA03D] mt-8 mb-8 text-4xl text-center">
                        Adição de Aluno
                    </h1>
                    <form onSubmit={handleSubmit} className="flex flex-col items-center w-full">
                        <div className="flex flex-col items-center w-full">
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Nome</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                                    type="text"
                                    name="nome"
                                    value={form.nome}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Email</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                                    type="email"
                                    name="email"
                                    value={form.email}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Matrícula</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                                    type="text"
                                    name="matricula"
                                    value={form.matricula}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Curso</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                                    type="text"
                                    name="curso"
                                    value={form.curso}
                                    onChange={handleChange}
                                    required
                                />
                            </label>
                        </div>
                        <span className="cursor-pointer mt-4 flex flex-col items-center p-[7] bg-[#727D73] rounded-xl shadow-[0_4px_20px_0_rgba(0,0,0,0.25)]">
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Nota</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] appearance-none"
                                    type="number"
                                    name="nota"
                                    value={form.nota || ""}
                                    onChange={handleChange}
                                    min="0"
                                    max="10"
                                    step="0.01"
                                    required
                                    style={{ MozAppearance: "textfield" }}
                                />
                            </label>
                            <label className="w-4/5 mb-4 flex flex-col items-center">
                                <span className="block mb-1 self-start">Faltas</span>
                                <input
                                    className="bg-[#A7C1A8] pl-2 w-72 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)] appearance-none"
                                    type="number"
                                    name="faltas"
                                    value={form.faltas || ""}
                                    onChange={handleChange}
                                    min="0"
                                    required
                                    style={{ MozAppearance: "textfield" }}
                                />
                            </label>
                            <button
                                type="submit"
                                className="cursor-pointer pt-2 pb-2 pl-14 pr-14 bg-[#D0DDD0] border-[#727D73] rounded-sm"
                            >
                                Cadastrar
                            </button>
                        </span>
                    </form>
                    <button
                        onClick={handleVoltar}
                        className="mt-4 px-6 py-2 bg-[#EEA03D] text-white rounded shadow hover:bg-[#d18c2e] transition"
                    >
                        Voltar para o Login
                    </button>
                    {mensagem && (
                        <div className="mt-4 text-green-600">{mensagem}</div>
                    )}
                </main>
            </div>
        </>
    );
}