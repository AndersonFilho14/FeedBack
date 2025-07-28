'use client'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LabelList,
} from "recharts";
import { Card, Typography } from "antd";
import { useEffect, useState } from "react";
import { getDSMunicipio } from "@/services/dashboard";

const { Title } = Typography;

export default function AvaragePerClass() {
  const [turma, setTurma] = useState([]);
  useEffect(() => {
    getDSMunicipio({ id: "1" }).then(({ data }) => {
      setTurma(data.ranking.turmas.ranking);
    });
  }, []);
  return (
    <Card className="flex flex-col max-w-3xl">
      <Title level={4}>Média por Turma</Title>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart
          layout="vertical"
          data={turma}
          margin={{ top: 20, right: 20, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 10]} />
          <YAxis type="category" dataKey="nome_turma" tick={{fontSize:12}} width={90} />
          <Tooltip />
          <Bar dataKey="media" fill="#1890ff">
            <LabelList dataKey="media" position="right" />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
