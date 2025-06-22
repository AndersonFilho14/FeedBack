"use client";
import desempenho from "@/app/api/desempenho";
import TableFormRead from "@/app/components/TableFormRead";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

function Page() {
	const { id } = useParams();
	const [alunoData, setAlunoData] = useState(null);

	useEffect(() => {
		if (id) {
			desempenho
				.encontrar(id)
				.then((data) => {
					setAlunoData(data);
				})
				.catch((error) => {
					console.error("Erro ao buscar aluno:", error);
				});
		}
	}, [id]);

	if (!alunoData) {
		return <div className="text-center mt-10">Carregando...</div>;
	}

	return 	<div className="flex justify-center items-center h-screen ">
				<div className="w-full">
				<TableFormRead alunoData={alunoData} />
				</div>
			</div>
}

export default Page;
