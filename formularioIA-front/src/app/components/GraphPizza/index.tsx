"use client";
import { PieChart, pieArcLabelClasses } from "@mui/x-charts/PieChart";
import { useEffect, useState } from "react";
import desempenho from "@/app/api/desempenho";
import convertsToPercentage from "@/app/service/convertsToPercentage";
import { AlunoType } from "../../types/AlunoType";

export const valueFormatter = (item: { value: number }) => `${item.value}%`;

export default function GraphPizza({ dataGraph }: { dataGraph: AlunoType[] }) {
	const size = {
		width: 256,
		height: 256,
	};

	return (
		<PieChart
			series={[
				{
					arcLabel: (item) => `${item.value}%`,
					arcLabelMinAngle: 35,
					arcLabelRadius: "60%",
					data: convertsToPercentage(dataGraph),
					valueFormatter,
				},
			]}
			sx={{
				[`& .${pieArcLabelClasses.root}`]: {
					fontWeight: "bold",
				},
			}}
			{...size}
		/>
	);
}
