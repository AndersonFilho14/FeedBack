"use client";
import FooterForm from "@/components/FooterForm";
import { FormItem } from "@/components/FormItem";
import { createEscola, editEscola, getEscola } from "@/services/escola";
import { Escola } from "@/types/Escola";
import {Form, Input, Typography } from "antd";
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
    const currentEscola = form.getFieldsValue() as Escola;

    if (mode === "create") {
      createEscola(currentEscola)
        .then(() => {
          console.log("tudo certo");
        })
        .catch(() => {
          console.log("error");
        });
    } else {
      if (currentEscola.senha?.trim() == "") {
        currentEscola.senha = undefined;
      }
      if (id) currentEscola.id = id
      editEscola({ id, ...currentEscola});
    }
  };

  return (
    <>
      <header className="font-[InknutAntiqua] bg-[#727D73] border-[#A4B465] text-[#EEA03D] border-7 h-21 text-center text-7xl fixed top-0 left-0 w-full z-50">
        IMD-IA
      </header>

      <div className="bg-[#F5ECD5] bg-[url('/imagem/backgroundloginimage.png')] bg-cover bg-center bg-no-repeat flex justify-center items-center min-h-screen py-28">
        <Form
          form={form}
          onFinish={onSubmit}
          className="font-[Jomolhari] bg-[#F5ECD5] border-[#A7C1A8] w-auto h-auto p-8 rounded-3xl shadow-[0_19px_4px_4px_rgba(0,0,0,0.25)] flex flex-col justify-center items-center gap-6 border-11"
        >
          <Title className="text-[#EEA03D] text-6xl">
            {mode === "edit" ? "Editar Escola" : "Criar Escola"}
          </Title>

          <FormItem name="nome" label="Nome da Escola">
            <Input
              className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded"
              placeholder="Nome da escola"
            />
          </FormItem>

          <FormItem name="idMunicipio" label="ID do Município">
            <Input
              type="number"
              className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded"
              placeholder="Digite o código do município"
            />
          </FormItem>

          <FormItem name="nomeUsuario" label="Nome do Usuário">
            <Input
              className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded"
              placeholder="Digite o nome do usuário"
            />
          </FormItem>

          <FormItem name="senha" label="Senha">
            <Input.Password
              className="bg-[#A7C1A8] pl-2 w-80 h-10 rounded"
              placeholder={
                mode === "edit"
                  ? "Deixe em branco para não alterar"
                  : "Digite a senha do usuário"
              }
            />
          </FormItem>

         <FooterForm/>
        </Form>
      </div>
    </>
  );
}

export default Page;
