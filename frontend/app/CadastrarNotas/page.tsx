"use client";
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

export default function CadastrarNotas() {

    const searchParams = useSearchParams();
    const turmaId = searchParams.get("turmaId");


    return (
        <>
                <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
                    IMD-IA
                </header>
                <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat  flex flex-col justify-center items-center h-screen ">
                    <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-329 h-212 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)]  flex flex-col justify-center items-center mt-22 gap-7 border-11 ">
                        <div className="flex flex-col items-center gap-1"><h1 className="text-[#EEA03D] text-6xl ">AVALIACOES</h1></div>
    
                                <main className="w-120 h-150 border-7 border-[#889E89] rounded-lg flex flex-col justify-center items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] pt-25 overflow-y-auto">
                                    
                                        <Link
                                        className="w-75 min-h-24 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center justify-center"
                                        href={{
                                            pathname: "/EditarNotas",
                                            query: { turmaId, tipo: "1Va" }
                                        }}
                                        >
                                        VA1
                                        </Link>

                                        <Link
                                        className="w-75 min-h-24 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center justify-center"
                                        href={{
                                            pathname: "/EditarNotas",
                                            query: { turmaId, tipo: "2Va" }
                                        }}
                                        >
                                        VA2
                                        </Link>
                                   
                                </main>
                            <Link className="w-34 h-10 border-5 rounded-lg border-[#727D73] flex  justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-lg " href={`/EdicaoTurma?turmaId=${turmaId}`}>Voltar</Link>
                    </div>
                        
                </div>
                    

            </>
    );
    }
