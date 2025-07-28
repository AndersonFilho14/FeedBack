"use client";
import { FormItem } from "@/components/FormItem";
import { createEscola, editEscola, getEscola } from "@/services/escola";
import { Escola } from "@/types/Escola";
import { Button, Form, Input, Typography } from "antd";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

function Page() {
  const [form] = Form.useForm();
  const searchParams = useSearchParams();
  const [mode, setMode] = useState<"edit" | "create">("create");
  const [escola, setEscola] = useState<Escola | null>();
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
    if (mode == "create") {
      createEscola(form.getFieldsValue())
        .then(() => {
          console.log("tudo certo");
        })
        .catch(() => {
          console.log("error");
        });
    } else {
      const currentEscola = form.getFieldsValue();
      if (escola && escola.senha == currentEscola.senha) {
        currentEscola.senha = undefined;
      }
      editEscola({ id, ...currentEscola });
    }
  };

  return (
    <>
      <Title level={3}>Formulário de Escola</Title>
      <Form form={form} onFinish={onSubmit}>
        <FormItem name="nome" label="Nome">
          <Input placeholder="Nome da escola" />
        </FormItem>
        <FormItem name="idMunicipio" label="Codigo do Municipio">
          <Input type="number" placeholder="Digite o código do usuário" />
        </FormItem>
        <FormItem name="nomeUsuario" label="Usuário">
          <Input placeholder="Digite o nome do usuário" />
        </FormItem>
        <FormItem name="senha" label="Senha">
          <Input type="password" placeholder="Digite a senha do usuário" />
        </FormItem>
        <div className="w-full flex  justify-between">
          <Button
            onClick={() => {
              route.back();
            }}
          >
            Voltar
          </Button>
          <Button type="primary" onClick={onSubmit}>
            Salvar
          </Button>
        </div>
      </Form>
    </>
  );
}

export default Page;
