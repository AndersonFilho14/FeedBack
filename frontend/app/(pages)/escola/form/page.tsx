"use client";
import { createEscola, editEscola, getEscola } from "@/services/escola";
import { Escola } from "@/types/Escola";
import { Form, Input } from "antd";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import Link from 'next/link';

function Page() {
  const [form] = Form.useForm();
  const searchParams = useSearchParams();
  const route = useRouter();
  
  const [mode, setMode] = useState<"edit" | "create">("create");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const id = searchParams.get("id");

  useEffect(() => {
    if (id) {
      setMode("edit");
      getEscola({ id })
        .then((data) => {
          form.setFieldsValue(data);
        })
        .catch(() => {
          alert("Erro ao buscar dados da escola.");
          route.back();
        });
    } else {
      setMode("create");
    }
  }, [id, form, route]);

  const onFinish = (values: Escola) => {
    setIsSubmitting(true);
    const apiCall =
      mode === "create"
        ? createEscola(values)
        : editEscola({ id, ...values, senha: values.senha?.trim() === "" ? undefined : values.senha });
    
    const successMessage = mode === "create" ? "Escola criada com sucesso!" : "Escola editada com sucesso!";
    const errorMessage = mode === "create" ? "Erro ao criar escola." : "Erro ao editar escola.";

    apiCall
      .then(() => {
        alert(successMessage);
        route.push('/escola'); 
      })
      .catch(() => {
        alert(errorMessage);
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50 flex items-center justify-center">
          IMD-IA
      </header>

      <main className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-32 px-4">
          <div className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-[90%] max-w-4xl p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col gap-6 border-11">
              <h1 className="text-[#EEA03D] text-5xl text-center">
                  {mode === 'edit' ? 'Editar Escola' : 'Cadastrar Nova Escola'}
              </h1>
              
              <Form
                  form={form}
                  onFinish={onFinish}
                  className="flex flex-col gap-8"
                  autoComplete="off"
              >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                      {/* Nome da Escola */}
                      <Form.Item name="nome" label={<h5>Nome da Escola</h5>} rules={[{ required: true, message: " " }]}>
                          <Input className="w-full h-12 bg-[#A7C1A8] rounded px-3 text-lg" />
                      </Form.Item>

                   

                      {/* Nome do Usuário */}
                      <Form.Item name="nomeUsuario" label={<h5>Nome do Usuário</h5>} rules={[{ required: true, message: " " }]}>
                          <Input className="w-full h-12 bg-[#A7C1A8] rounded px-3 text-lg" />
                      </Form.Item>

                      {/* Senha */}
                      <Form.Item name="senha" label={<h5>Senha</h5>} rules={[{ required: mode === 'create', message: " " }]}>
                          <Input.Password
                              placeholder={mode === "edit" ? "Deixe em branco para não alterar" : ""}
                              className="w-full h-12 bg-[#A7C1A8] rounded px-3 text-lg"
                          />
                      </Form.Item>
                  </div>
                  
                  <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mt-4">
                      <Link className="w-full sm:w-44 h-13 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-2xl text-black order-2 sm:order-1" href={"/escola"}>
                          Voltar
                      </Link>
                      <button type="submit" disabled={isSubmitting} className="w-full sm:w-100 h-19 border-5 rounded-lg border-[#727D73] flex justify-center items-center shadow-[0px_4px_22.5px_3px_rgba(0,0,0,0.18)] bg-amber-50 text-4xl disabled:bg-gray-400 disabled:cursor-not-allowed disabled:text-gray-600 order-1 sm:order-2">
                          {isSubmitting ? "Salvando..." : "Salvar"}
                      </button>
                  </div>
              </Form>
          </div>
      </main>
    </>
  );
}

export default Page;