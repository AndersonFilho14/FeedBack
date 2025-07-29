import { Button, Table, TableProps } from "antd";
import { Edit2Icon, Eye, RecycleIcon, TrashIcon } from "lucide-react";
import { usePathname, useRouter } from "next/navigation";
import React from "react";

function CustomTable({
  columns,
  dataSource,
  handleDelete,
}: {
  columns: TableProps["columns"];
  dataSource: TableProps["dataSource"];
  handleDelete: (id: string) => void;
}) {
  const route = useRouter();
  const href = usePathname();
  const dataCol: TableProps["columns"] = [
    {
      key: "Ações",
      title: "Ações",
      render: (_, rol) => (
        <>
          <div>
            <Button
              onClick={() => {
                route.push(`${href}/form?id=${rol.id}`);
              }}
            >
              <Edit2Icon />
            </Button>
            <Button onClick={() => handleDelete(rol.id)}>
              <TrashIcon />
            </Button>
          </div>
        </>
      ),
    },
  ];

  return (
    <>
      <Table columns={[...columns!, ...dataCol]} dataSource={dataSource} />
    </>
  );
}

export default CustomTable;
