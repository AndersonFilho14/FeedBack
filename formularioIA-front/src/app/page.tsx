"use client";

import React, { useEffect, useState } from "react";
import GraphPizza from "./components/GraphPizza";
import BarGraph from "./components/BarGraph";
import desempenho from "./api/desempenho";
import { treatDataForM } from "./service/treatDataForM";
import { treatDataMusic } from "./service/treatDataMusic";
import { treatDataAula } from "./service/treatDataAula";
import { treatDataEsport } from "./service/treatDataSport";
import { treatDataVolunt } from "./service/treatDataVolunt";
import { treatDataExtra } from "./service/treatDataExtra";
import { AlunoType } from "./types/AlunoType";

export default function Page() {
	const [alunos, setAlunos] = useState<AlunoType[]>([]);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const data = await desempenho.listar();
				setAlunos(data);
			} catch (error) {
				console.error("Erro ao buscar dados, usando mock:", error);
			}
		};

		fetchData();
	}, []);
	if (!alunos || alunos.length === 0) {
		return <p>Carregando dados...</p>;
	}
	return (
		<div className="flex-grow p-6 md:ml-0 overflow-y-auto">
			<div className="mb-6">
				<h1 className="text-2xl font-semibold text-gray-800">
					Painel de Desempenho dos Alunos
				</h1>
				<p className="text-gray-600">
					Visualize e analise os principais fatores que influenciam o rendimento
					escolar
				</p>
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
				<BarGraphCard
					title="Distribuição por Sexo"
					data={treatDataForM(alunos)}
					axis="sexo"
				/>
				<BarGraphCard
					title="Aula de Música"
					data={treatDataMusic(alunos)}
					axis="aulaMusica"
				/>
				<BarGraphCard
					title="Aulas Particulares"
					data={treatDataAula(alunos)}
					axis="aulasParticulares"
				/>
				<BarGraphCard
					title="Participação em Esportes"
					data={treatDataEsport(alunos)}
					axis="esportes"
				/>
				<BarGraphCard
					title="Voluntariado"
					data={treatDataVolunt(alunos)}
					axis="voluntariado"
				/>
				<BarGraphCard
					title="Atividades Extracurriculares"
					data={treatDataExtra(alunos)}
					axis="extraCurriculares"
				/>

				<div className="bg-white rounded-lg shadow p-4 col-span-1 md:col-span-2 lg:col-span-3">
					<h2 className="text-lg font-medium text-gray-700 mb-4">
						Distribuição Geral de Notas
					</h2>
					<div className="h-64">
						<GraphPizza dataGraph={alunos} />
					</div>
				</div>
			</div>
		</div>
	);
}

function BarGraphCard({
	title,
	data,
	axis,
}: {
	title: string;
	data: any;
	axis: string;
}) {
	return (
		<div className="bg-white rounded-lg shadow p-4">
			<h2 className="text-lg font-medium text-gray-700 mb-4">{title}</h2>
			<div className="h-64">
				<BarGraph dataGraph={data} dataxAxis={axis} />
			</div>
		</div>
	);
}
