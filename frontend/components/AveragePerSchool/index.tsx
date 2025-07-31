/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { getDSMunicipio } from "@/services/dashboard";
import { Card, Typography } from "antd";
import React, { useEffect, useState } from "react";
import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const renderLabel = (entry: any) => {
  const { nome_escola, percent } = entry;
  if (percent === undefined) return nome_escola;
  return `${nome_escola}: ${(percent * 100).toFixed(1)}%`;
};

function AveragePerSchool() {
    const {Title} = Typography;
  const [escolas, setEscolas] = useState([]);
  useEffect(() => {
    getDSMunicipio({ id: "1" }).then(({ data }) => {
      setEscolas(data.ranking.escolas.ranking);
    });
  }, []);
  const cores = ["#1890ff", "#f5222d", "#52c41a", "#faad14", "#13c2c2"];

  return (
        <Card className="flex flex-col max-w-3xl">
      <Title level={3}>Média por Escola</Title>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={escolas}
              dataKey="media"
              nameKey="nome_escola"
              cx="50%"
              cy="50%"
              outerRadius={120}
              label={renderLabel}
            >
              {escolas.map((_, index) => (
                <Cell key={index} fill={cores[index % cores.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: any) => `${value.toFixed(2)}`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </Card>
  );
}

export default AveragePerSchool;
