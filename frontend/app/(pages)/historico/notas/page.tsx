"use client";
import { getHistoricoNotasList } from "@/services/historico";
import React, { useEffect, useState } from "react";
import { columns } from "./data";
import { Table } from "antd";

function Page() {
  const [notas, setNotas] = useState([]);
  useEffect(() => {
    getHistoricoNotasList({ id: 1 }).then((data) => {
      setNotas(data);
    });
  }, []);
  return (
    <>
      <Table dataSource={notas} columns={columns} />
    </>
  );
}

export default Page;
