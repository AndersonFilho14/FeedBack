"use client";
import { BarChart } from "@mui/x-charts/BarChart";

export default function BarGraph({ dataGraph, dataxAxis }: any) {
	return (
		<BarChart
			dataset={dataGraph}
			series={[
				{ dataKey: "A", label: "A" },
				{ dataKey: "B", label: "B" },
				{ dataKey: "C", label: "C" },
				{ dataKey: "D", label: "D" },
				{ dataKey: "F", label: "F" },
			]}
			height={250}
			xAxis={[{ scaleType: "band", dataKey: dataxAxis }]}
		/>
	);
}
