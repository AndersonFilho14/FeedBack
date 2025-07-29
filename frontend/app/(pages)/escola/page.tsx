"use client";
import { deleteEscola, getListEscolas } from "@/services/escola";
import { Escola } from "@/types/Escola";
import React, { useEffect, useState } from "react";
import { columns } from "./data";
import CustomTable from "@/components/CustomTable";

function Page() {
  const [escolas, setEscolas] = useState<Escola[]>();
  const [refresh, setRefresh] = useState(false);
  useEffect(() => {
    getListEscolas().then((data) => {
      setEscolas(data);
    });
  }, [refresh]);
  const handleDelete = (id: string) => {
    deleteEscola({ id }).finally(() => {
      setRefresh(!refresh);
    });
  };
  return (
    <>
      <CustomTable
        columns={columns}
        dataSource={escolas}
        handleDelete={handleDelete}
      />
    </>
  );
}

export default Page;
