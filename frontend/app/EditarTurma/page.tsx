"use client";
import React,{useState} from "react";
import Link from "next/link";


export default function CadastrarTurma() {
    
    const [turma, setTurmas] = useState("Turma");
    const [professor, setProfessor] = useState("Professor");
    const [aluno, setAluno] = useState("Aluno");

    return (
        <>
            <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                IMD-IA
            </header>
            <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex  justify-center items-center h-screen ">
                <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-6 border-11 ">
                    <h1 className="text-[#EEA03D] text-6xl ">Editar Turma</h1>
                    <h5 className="text-2xl">Nome da Turma</h5>
                    <input
                            className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded inset-shadow-[0_2px_1.8px_1px_rgba(0,0,0,0.25)]"
                            type="text"
                            name="User"
                            value={turma}
                            onChange={e => setTurmas(e.target.value)}
                            required
                    />
                    
                    <div className="flex gap-100 justify-center items-center">
                        <div className="flex flex-col gap-4">
                            <h5 className="text-2xl">Procurar Professor</h5>
                            <div>
                                <input className="w-80 h-10 border-5 rounded-lg border-[#A4B465]  bg-amber-50 text-4xl shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)]" name="" id="" />
                                <div className="overflow-y-auto h-20">
                                        <div className=" w-80 h-10 border-5 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {professor}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                    <div className=" w-80 h-10 border-5  rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {professor}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                    <div className=" w-80 h-10 border-5  rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {professor}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                </div>
                                
                            </div>
                            <h5 className="text-2xl">Procurar Aluno</h5>
                               <div>
                                <input className="w-80 h-10 border-5 rounded-lg border-[#A4B465]  bg-amber-50 text-4xl shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)]" name="" id="" />
                               <div className="overflow-y-auto h-20">
                                        <div className=" w-80 h-10 border-5 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {aluno}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                    <div className=" w-80 h-10 border-5  rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {aluno}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                    <div className=" w-80 h-10 border-5  rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                        {aluno}
                                        <div className="flex gap-4">
                                            <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                           
                        </div>
                        <div>
                            <main className="w-120 h-100 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-30  overflow-y-auto" >
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {professor}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                                <div className=" w-100 h-15 border-7 rounded-lg  border-[#A4B465] text-2xl flex items-center place-content-between pl-4 pr-2">
                                    {aluno}
                                    <div className="flex gap-4">
                                        <Link href={""}><img className="w-6" src="/imagem/lixo.png" alt="Lixo" /></Link>
                                    </div>
                                </div>
                            </main>
                        </div>
                    </div>
                    <Link className="w-100 h-19 border-5 rounded-lg border-[#A4B465] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl" href={"/CadastrarTurma"}>Salvar</Link>
                    <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg " href={"/ListaTurmas"}>Voltar</Link>
                </div>
                
            </div>

        </>
    );
}
