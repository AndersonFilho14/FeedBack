"use client";
import { FormItem } from "@/components/FormItem";
import { createEscola, editEscola, getEscola } from "@/services/escola";
import { Escola } from "@/types/Escola";
import { Button, Form, Input, Typography } from "antd";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

function Page() {
  const [form] = Form.useForm();
  const searchParams = useSearchParams();
  const [mode, setMode] = useState<"edit" | "create">("create");
  const [escola, setEscola] = useState<Escola | null>(null);
  const id = searchParams.get("id");
  const route = useRouter();
  const { Title } = Typography;

  useEffect(() => {
    if (id) {
      setMode("edit");
      getEscola({ id })
        .then((data) => {
          setEscola(data);
          form.setFieldsValue(data);
        })
        .catch(() => {
          route.back();
        });
    } else {
      setMode("create");
    }
  }, []);

  const onSubmit = () => {
    const currentEscola = form.getFieldsValue();

    if (mode === "create") {
      createEscola(currentEscola)
        .then(() => {
          console.log("tudo certo");
        })
        .catch(() => {
          console.log("error");
        });
    } else {
      if (escola && escola.senha === currentEscola.senha) {
        currentEscola.senha = undefined;
      }

      if (escola) {
        editEscola({ id: escola.id, ...currentEscola });
      }
    }
  };

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
        <form
          
          className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-full max-w-4xl h-auto p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-8 border-11"
        >
          <h1 className="text-[#EEA03D] text-6xl mb-4">
            {mode === "edit" ? "Editar Escola" : "Criar Escola"}
          </h1>

          <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
            <div className="flex flex-col gap-2">
              <h5 className="text-2xl">Nome da Escola</h5>
              <input
                className="bg-[#A7C1A8] px-3 w-full h-10 rounded"
                placeholder="Nome da escola"
               
                
                required
              />
            </div>

            <div className="flex flex-col gap-2">
              <h5 className="text-2xl">ID do Município</h5>
              <input
                type="number"
                className="bg-[#A7C1A8] px-3 w-full h-10 rounded"
                placeholder="Digite o código do município"
                
                
                required
              />
            </div>

            <div className="flex flex-col gap-2">
              <h5 className="text-2xl">Nome do Usuário</h5>
              <input
                className="bg-[#A7C1A8] px-3 w-full h-10 rounded"
                placeholder="Digite o nome do usuário"
                
                required
              />
            </div>

            <div className="flex flex-col gap-2">
              <h5 className="text-2xl">Senha</h5>
              <input
                type="password"
                className="bg-[#A7C1A8] px-3 w-full h-10 rounded"
                placeholder={
                  mode === "edit"
                    ? "Deixe em branco para não alterar"
                    : "Digite a senha do usuário"
                }
                
                required={mode === "create"}
              />
            </div>
          </div>

          <div className="w-full flex justify-center items-center gap-10 mt-8">
            <Link
              href="/escola"
              className="w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl hover:bg-gray-100 transition-colors"
            >
              Voltar
            </Link>
            <button
              type="submit"
              className="w-44 h-13 border-5 rounded-lg border-[#A4B465] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl hover:bg-amber-100 transition-colors"
            >
              Salvar
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

export default Page;
