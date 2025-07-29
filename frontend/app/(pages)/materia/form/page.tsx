"use client";
import FooterForm from "@/components/FooterForm";
import { FormItem } from "@/components/FormItem";
import { createMateria, editMateria, getMateria } from "@/services/materia";
import { Materia } from "@/types/Materia";
import { Form, Input } from "antd";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";

function Page() {
  const [form] = Form.useForm();
  const searchParams = useSearchParams();
  const [mode, setMode] = useState<"edit" | "create">("create");
  const [materia, setMateria] = useState<Materia | null>(null);
  const id = searchParams.get("id");
  const route = useRouter();

  useEffect(() => {
    if (id) {
      setMode("edit");
      getMateria({ id })
        .then((data) => {
          console.log(data, "aquiii");
          setMateria(data);
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
    const currentMateria = form.getFieldsValue() as Materia;

    if (mode === "create") {
      createMateria(currentMateria)
        .then(() => {
          console.log("tudo certo");
        })
        .catch(() => {
          console.log("error");
        });
    } else {
      editMateria({ id, ...currentMateria });
    }
  };

  return (
    <>
      <Form onFinish={onSubmit} form={form}>
        <FormItem name="nome" label="Nome">
          <Input placeholder="Nome da Materia" />
        </FormItem>
        <FooterForm/>
      </Form>
    </>
  );
}

export default Page;
