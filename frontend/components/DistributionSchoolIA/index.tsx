/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { getDSEscola } from "@/services/dashboard";
import { Card, Typography } from "antd";
import { useEffect, useState } from "react";

import PizzaPerScore from "../PizzaPerScore";

export default function DistributionSchoolIA() {
  const [nota, setNotas] = useState<any>([]);
  useEffect(() => {
    getDSEscola({ id: "1" }).then(({ data }) => {
      setNotas(data.ia.distribuicao_notas.distribuicao_por_escola);
    });
  }, []);

  const { Title } = Typography;
  return (
    <Card className="flex flex-col max-w-3xl">
      <Title level={4}>Média de Score IA</Title>
      <PizzaPerScore dataSource={nota} />
    </Card>
  );
}
