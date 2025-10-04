"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function AdminPage() {
	const [screenResults, setScreenResults] = useState<any>(null);
	const [finalSel, setFinalSel] = useState<any>(null);

	async function runScreening() {
		const res = await fetch(`${API_BASE}/screen-applications`);
		setScreenResults(await res.json());
	}
	async function runSelection() {
		const res = await fetch(`${API_BASE}/final-selection`);
		setFinalSel(await res.json());
	}

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Admin Panel</h2>
			<div className="flex gap-2">
				<button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={runScreening}>Run Screening</button>
				<button className="bg-green-600 text-white px-4 py-2 rounded" onClick={runSelection}>Run Final Selection</button>
			</div>
			{screenResults && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(screenResults,null,2)}</pre>
			)}
			{finalSel && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(finalSel,null,2)}</pre>
			)}
		</div>
	);
}
