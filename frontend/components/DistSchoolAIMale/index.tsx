/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { getDSEscola } from "@/services/dashboard";
import { Card, Typography } from "antd";
import { useEffect, useState } from "react";

import PizzaPerScore from "../PizzaPerScore";

export default function DistSchoolAIMale() {
  const [nota, setNotas] = useState<any>([]);
  useEffect(() => {
    getDSEscola({ id: "1" }).then(({ data }) => {
      setNotas(data.ia.por_sexo.distribuicao_por_sexo.Feminino);
    });
  }, []);

  const { Title } = Typography;
  return (
    <Card className="flex flex-col max-w-3xl">
      <Title level={4}>Média Score IA: Sexo Feminino</Title>
      <PizzaPerScore dataSource={nota} />
    </Card>
  );
}
