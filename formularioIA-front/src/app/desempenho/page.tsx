"use client";
import React from "react";
import { useRouter } from "next/navigation";

const Desempenho: React.FC = () => {
	const router = useRouter();

	const navigate = (path: string) => {
		router.push(path);
	};

	const pages = [
		{ name: "Criar", href: "/desempenho/criar" },
		{ name: "Listar", href: "/desempenho/listar" },
	];

	return (
		<div className="flex justify-center items-center h-screen">
			<div className="space-y-6">
				{pages.map(({ name, href }) => (
					<button
						key={name}
						className="bg-blue-600 hover:bg-blue-700 text-white text-xl px-8 py-4 rounded-lg w-full max-w-xs"
						onClick={() => navigate(href)}
					>
						{name}
					</button>
				))}
			</div>
		</div>
	);
};

export default Desempenho;
