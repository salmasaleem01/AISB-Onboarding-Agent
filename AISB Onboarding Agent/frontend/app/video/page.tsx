"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function VideoPage() {
	const [applicantId, setApplicantId] = useState<number>(0);
	const [topic, setTopic] = useState<string>("Intro to AI");
	const [file, setFile] = useState<File | null>(null);
	const [result, setResult] = useState<any>(null);

	async function upload() {
		if (!file) return;
		const fd = new FormData();
		fd.append("applicant_id", String(applicantId));
		fd.append("topic", topic);
		fd.append("file", file);
		const res = await fetch(`${API_BASE}/video/upload`, { method: "POST", body: fd });
		const data = await res.json();
		setResult(data);
	}

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Video Upload</h2>
			<div className="grid gap-3">
				<input className="border p-2 rounded" placeholder="Applicant ID" type="number" value={applicantId} onChange={e=>setApplicantId(Number(e.target.value))}/>
				<input className="border p-2 rounded" placeholder="Topic" value={topic} onChange={e=>setTopic(e.target.value)}/>
				<input className="border p-2 rounded" type="file" accept="video/*" onChange={e=>setFile(e.target.files?.[0]||null)}/>
				<button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={upload}>Upload</button>
			</div>
			{result && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(result,null,2)}</pre>
			)}
		</div>
	);
}
