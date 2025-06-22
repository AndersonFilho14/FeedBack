"use client";
import React from "react";
import { useRouter } from "next/navigation";

const levelFeedback = [
	{ value: 0, label: "Nenhum" },
	{ value: 1, label: "Baixo" },
	{ value: 2, label: "Moderado" },
	{ value: 3, label: "Alto" },
	{ value: 4, label: "Muito Alto" },
];

const radioTrueorFalseOption = [
	{ value: 1, label: "Sim" },
	{ value: 0, label: "Não" },
];

const askWithTrueOrFalse = [
	{ name: "aulasParticulares", label: "Aulas Particulares" },
	{ name: "extraCurriculares", label: "Extras Curriculares" },
	{ name: "esportes", label: "Esportes" },
	{ name: "aulaMusica", label: "Músicas" },
	{ name: "voluntariado", label: "Voluntariado" },
];

interface AlunoData {
	[key: string]: string | number;
	nome: string;
	idade: string;
	sexo: string;
	etnia: string;
	educacaoPais: string;
	tempoEstudoSemanal: string;
	faltas: string;
	apoioPais: string;
	aulasParticulares: number;
	extraCurriculares: number;
	esportes: number;
	aulaMusica: number;
	voluntariado: number;
	notaFinal: number;
}

interface AlunoFormProps {
	alunoData: AlunoData;
}

export default function AlunoFormRead({ alunoData }: AlunoFormProps) {
	const router = useRouter();

	// Mapeamento de valores para exibição
	const getSexoLabel = (value: string) => {
		switch (value) {
			case "0":
				return "Masculino";
			case "1":
				return "Feminino";
			case "2":
				return "Outro";
			default:
				return "Não informado";
		}
	};

	const getEtniaLabel = (value: string) => {
		switch (value) {
			case "0":
				return "Branca";
			case "1":
				return "Preta";
			case "2":
				return "Parda";
			case "3":
				return "Amarela";
			case "4":
				return "Indígena";
			case "5":
				return "Outra";
			default:
				return "Não informado";
		}
	};

	const getEducacaoPaisLabel = (value: string) => {
		switch (value) {
			case "0":
				return "Nenhuma";
			case "1":
				return "Fundamental";
			case "2":
				return "Médio";
			case "3":
				return "Superior";
			default:
				return "Não informado";
		}
	};

	const getApoioPaisLabel = (value: string) => {
		const level = levelFeedback.find((l) => l.value === Number(value));
		return level ? level.label : "Não informado";
	};

	return (
		<div className="max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg space-y-6">
			<div className="flex justify-between items-center">
				<h2 className="text-2xl font-bold">Dados do Aluno</h2>
			
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div>
					<label className="block text-sm font-medium text-gray-500">
						Nome
					</label>
					<div className="p-2 border-b border-gray-200">
						{alunoData.nome || "Não informado"}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Idade
					</label>
					<div className="p-2 border-b border-gray-200">
						{alunoData.idade || "Não informado"}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Sexo
					</label>
					<div className="p-2 border-b border-gray-200">
						{getSexoLabel(alunoData.sexo)}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Etnia
					</label>
					<div className="p-2 border-b border-gray-200">
						{getEtniaLabel(alunoData.etnia)}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Educação dos Pais
					</label>
					<div className="p-2 border-b border-gray-200">
						{getEducacaoPaisLabel(alunoData.educacaoPais)}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Tempo de Estudo Semanal (horas)
					</label>
					<div className="p-2 border-b border-gray-200">
						{alunoData.tempoEstudoSemanal || "Não informado"}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Número de Faltas
					</label>
					<div className="p-2 border-b border-gray-200">
						{alunoData.faltas || "Não informado"}
					</div>
				</div>

				<div>
					<label className="block text-sm font-medium text-gray-500">
						Apoio dos Pais
					</label>
					<div className="p-2 border-b border-gray-200">
						{getApoioPaisLabel(alunoData.apoioPais)}
					</div>
				</div>

		
			</div>

			<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
				{askWithTrueOrFalse.map((field) => (
					<div key={field.name}>
						<label className="block font-medium mb-1">{field.label}</label>
						<div className="p-2 border-b border-gray-200">
							{alunoData[field.name] === 1 ? "Sim" : "Não"}
						</div>
					</div>
				))}
			</div>
			<div className="w-full ">
					<label className="block text-sm font-bold text-gray-700">
						Nota final
					</label>
					<div className="p-2 border-b border-gray-200">
						{alunoData.notaFinal}
					</div>
				</div>
		</div>
	);
}
