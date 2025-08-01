"use client";
import { Card, Table, Typography } from "antd";
import React, { useEffect, useState } from "react";
import { columns } from "./data";
import { getDSMunicipio } from "@/services/dashboard";

function BestStudentTable({
  hidePageButtons = false,
}: {
  hidePageButtons?: boolean;
}) {
  const [alunos, setAlunos] = useState([]);
  useEffect(() => {
    getDSMunicipio({ id: "1" }).then(({ data }) => {
      setAlunos(data.ranking.alunos.ranking);
    });
  }, []);
  const { Title } = Typography;

  return (
    <>
      <div>
        <Card className="flex flex-col max-w-3xl">
          <Title level={4}>Ranking Top 5 Média de Alunos</Title>
          <Table
            columns={columns}
            dataSource={hidePageButtons ? alunos.slice(0, 5) : alunos}
            pagination={{
              pageSize: 5,
              hideOnSinglePage: true,
            }}
          />
        </Card>
      </div>
    </>
  );
}

export default BestStudentTable;
