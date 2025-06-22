"use client";
import { useRouter } from "next/navigation";

interface TableListProps {
	columns: {
		title: string;
		dataIndex?: string;
		key: string;
		render?: (text: any, record: any) => React.ReactNode;
	}[];
	data: any[];
}

export default function TableList({ columns, data }: TableListProps) {
	const router = useRouter();

	return (
		<div className="overflow-x-auto">
			<table className="min-w-full divide-y divide-gray-200">
				<thead className="bg-gray-50">
					<tr>
						{columns.map((column) => (
							<th
								key={column.key}
								className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>
								{column.title}
							</th>
						))}
					</tr>
				</thead>
				<tbody className="bg-white divide-y divide-gray-200">
					{data.map((item) => (
						<tr key={item.id}>
							{columns.map((column) => (
								<td key={column.key} className="px-6 py-4 whitespace-nowrap">
									{column.render
										? column.render(null, item)
										: item[column.dataIndex as string]}
								</td>
							))}
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}
