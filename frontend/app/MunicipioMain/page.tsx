import React from "react";
import Link from "next/link";

export default function EscolaPage() {
  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>
      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto max-w-xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-8 border-11">
          <h1 className="text-[#EEA03D] text-5xl text-center">
            Painel do Município
          </h1>
          <main className="w-full flex flex-col justify-center items-center gap-6">
            <Link
              className="w-96 h-20 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl text-center bg-amber-50 hover:bg-amber-100 transition-colors"
              href={"/escola"}
            >
              Gerenciar Escolas
            </Link>
            <Link
              className="w-96 h-20 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl text-center bg-amber-50 hover:bg-amber-100 transition-colors"
              href={"/materia"}
            >
              Gerenciar Matérias
            </Link>
            <Link
              className="w-96 h-20 border-5 rounded-lg border-[#EEA03D] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] text-2xl text-center bg-amber-50 hover:bg-amber-100 transition-colors"
              href={"/dashboard"}
            >
              Visualizar Dashboard
            </Link>
          </main>
          <Link
            className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl mt-8 hover:bg-gray-100 transition-colors"
            href={"/Login"}
          >
            Voltar
          </Link>
        </div>
      </div>
    </>
  );
}