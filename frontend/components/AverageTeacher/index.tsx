/* eslint-disable @typescript-eslint/no-explicit-any */
'use client'
import { getDSEscola } from "@/services/dashboard";
import { Card, Typography } from "antd";
import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from "recharts";

const cores = ["#52c41a", "#91d5ff", "#faad14", "#f5222d"];

export const AverageTeacher: React.FC = () => {
  const [professor, setProfessor] = useState([]);
  useEffect(() => {
    getDSEscola({ id: "1" }).then(({ data }) => {
      setProfessor(data.ranking.professores.ranking_professores);
    });
  },[]);
const { Title } = Typography;

  return (
    <Card style={{ width: "100%", height: 450 }}>
      <Title level={4}>Ranking de Professores por Média</Title>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={professor}
          margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
        >
          <XAxis
            dataKey="nome_professor"
            angle={-45}
            textAnchor="end"
            interval={0}
          />
          <YAxis domain={[0, 10]} />
          <Tooltip
            formatter={(value: number, name: string) =>
              name === "media"
                ? [`${value.toFixed(2)}`, "Média"]
                : [`${value}`, "Avaliações"]
            }
            labelFormatter={(label: string) => `Professor: ${label}`}
          />
          <Bar dataKey="media" name="media" >
              <LabelList dataKey="media" position="top" formatter={(v:any) => v!.toFixed(2)} />
            {professor.map((_, index) => (
              <Cell key={index} fill={cores[index % cores.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default AverageTeacher;
