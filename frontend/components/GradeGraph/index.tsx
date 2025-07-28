import { getDSMunicipio } from '@/services/dashboard';
import { Typography } from 'antd';
import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  Cell,
} from 'recharts';


const cores = ['#52c41a', '#faad14', '#f5222d'];

const GradeGraph: React.FC = () => {
    const [notas, setNotas]= useState([]);
    useEffect(()=>{
        getDSMunicipio({id: "1"})
        .then(({data})=>{
            setNotas(data.ia.distribuicao_notas.distribuicao_notas)
        })
    },[])
    const { Title } = Typography;

 return (
    <div style={{ width: '100%', height: 400 }}>
      <Title level={4}>Distribuição Geral das Notas</Title>
      <ResponsiveContainer>
        <BarChart
          data={notas}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <XAxis dataKey="categoria" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="valor" name="Quantidade de Alunos">
            {notas.map((_, index) => (
              <Cell key={index} fill={cores[index % cores.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default GradeGraph;
