/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";
import { removerZeros } from "@/utils/removerZeros";
import { useEffect } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#B39DDB",
  "#F06292",
];

export default function PizzaPerScore({ dataSource }: { dataSource: any }) {
  const data = removerZeros(dataSource);
  useEffect(()=>{
    console.log(dataSource)
    console.log(data)
  },[])
  return (
    <ResponsiveContainer width="100%" height={400}>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label={({ name, percent }) =>
            percent !== undefined
              ? `${name}: ${(percent * 100).toFixed(1)}%`
              : name
          }
        >
          {data.map((_: any, index: number) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
          formatter={(value: number, name: string) => [
            `${value}`,
            `Nota ${name}`,
          ]}
        />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
