"use client";
import React, { useEffect, useState } from "react";
import desempenho from "@/app/api/desempenho";
import { useRouter } from "next/navigation";  // Use useRouter from next/navigation
import TableList from "@/app/components/TableList";

export default function DesempenhoPage() {
	const [alunos, setAlunos] = useState<any[]>([]);
	const router = useRouter();  // Use the router hook here

	useEffect(() => {
		const loadData = async () => {
			try {
				const data = await desempenho.listar();
				setAlunos(data);
				console.log(data);
			} catch (error) {
				console.error("Erro ao carregar dados:", error);
				setAlunos([]);
			}
		};

		loadData();
	}, []);

	const columns = [
		{
			title: "Nome",
			dataIndex: "nome",
			key: "nome",
		},
		{
			title: "Idade",
			dataIndex: "idade",
			key: "idade",
		},
		{
			title: "Etnia",
			dataIndex: "etnia",
			key: "etnia",
		},
		{
			title: "Ação",
			key: "acao",
			render: (_: any, record: any) => (
				<button
					onClick={() => router.push(`/desempenho/visualizar/${record.id}`)}  // Use router.push correctly
					className="text-black hover:text-blue-600"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						className="h-5 w-5"
						viewBox="0 0 20 20"
						fill="currentColor"
					>
						<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
						<path
							fillRule="evenodd"
							d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
							clipRule="evenodd"
						/>
					</svg>
				</button>
			),
		},
	];

	return <TableList columns={columns} data={alunos ?? []} />;
}
