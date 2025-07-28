import { Table, Typography } from "antd";
import React, { useEffect, useState } from "react";
import { columns } from "./data";
import { Escola } from "@/types/Escola";
import { getListEscolas } from "@/services/escola";

function Page() {
  const [escolas, setEscolas] = useState<Escola[]>([]);
  useEffect(() => {
    getListEscolas().then((data) => {
      setEscolas(data);
    });
  }, []);
  const { Title } = Typography;
  return (
    <>
      <Title level={3}>Lista de Escolas</Title>
      <Table columns={columns} dataSource={escolas}></Table>
    </>
  );
}

export default Page;
