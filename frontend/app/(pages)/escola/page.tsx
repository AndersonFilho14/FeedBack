"use client";
import React, { useState } from "react";
import Link from "next/link";

export default function ListaEscolas() {
  // O estado controla a visibilidade do modal de confirmação
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  // Dados de exemplo para exibir a estrutura da lista
  const escolasMock = [
    { id: 1, nome: "Escola Municipal Exemplo 1" },
    { id: 2, nome: "Escola Estadual Exemplo 2" },
    { id: 3, nome: "Centro Educacional Exemplo 3" },
  ];

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
        <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto max-w-4xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-6 border-11">
          <h1 className="text-[#EEA03D] text-6xl">Gerenciamento de Escolas</h1>

          <main className="w-full max-w-3xl h-137 border-7 border-[#889E89] rounded-lg flex flex-col items-center gap-4 bg-amber-50 shadow-[0_16px_7.8px_2px_rgba(0,0,0,0.25)] p-4 overflow-y-auto">
            {/* A lista agora usa dados de exemplo (mock) */}
            {escolasMock.map((escola) => (
                <div
                  key={escola.id}
                  className="w-full h-15 border-7 rounded-lg border-[#A4B465] text-2xl flex items-center justify-between pl-4 pr-2"
                >
                  <span>{escola.nome}</span>
                  <div className="flex gap-4 items-center">
                    <Link href={`/escola/form?id=${escola.id}`}>
                      <img
                        className="w-10 h-10"
                        src="/imagem/editar.png"
                        alt="Editar"
                      />
                    </Link>
                    <button
                      type="button"
                      className="focus:outline-none"
                      onClick={() => setShowDeleteModal(true)}
                    >
                      <img
                        className="w-10 h-10"
                        src="/imagem/lixo.png"
                        alt="Excluir"
                      />
                    </button>
                  </div>
                </div>
              ))}
          </main>
          <div className="flex w-full justify-between items-center mt-4 max-w-3xl">
            <Link
              className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl hover:bg-gray-100 transition-colors"
              href={"/MunicipioMain"}
            >
              Voltar
            </Link>
            <Link
              className="w-100 h-19 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl hover:bg-amber-100 transition-colors"
              href={"/escola/form"}
            >
              Cadastrar Escola
            </Link>
          </div>
        </div>
      </div>

      {/* O modal é exibido com base no estado 'showDeleteModal' */}
      {showDeleteModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-[rgba(0,0,0,0.32)] z-50">
          <div className="bg-[#ECF0EC] rounded-lg shadow-[0px_19px_4px_4px_rgba(0,0,0,0.25)] p-8 flex flex-col gap-15 items-center justify-center w-[502px] h-[484px] border-[7px] border-[#889E89]">
            <div className="w-[406px] h-[91px] bg-[#EEA03D] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px] text-center text-2xl text-black font-[Hammersmith_One] flex items-center justify-center p-2">
              VOCÊ ESTÁ EXCLUINDO UMA <br /> ESCOLA
            </div>
            <span className="font-[Jomolhari] text-4xl mb-4 text-center">
              Tem certeza que deseja Excluir?
            </span>
            <div className="flex flex-col items-center gap-4">
              <button
                className="font-[Jomolhari] text-3xl w-[206px] h-[61px] bg-[#ECF0EC] border-6 border-[#EEA03D] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px]"
                onClick={() => setShowDeleteModal(false)} // Apenas fecha o modal
              >
                Confirmar
              </button>
              <button
                className="font-[Jomolhari] w-[122px] h-[37px] bg-[#ECF0EC] border-[7px] border-[#727D73] shadow-[0_4px_22.5px_3px_rgba(0,0,0,0.18)] rounded-[4px]"
                onClick={() => setShowDeleteModal(false)} // Apenas fecha o modal
              >
                Voltar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}