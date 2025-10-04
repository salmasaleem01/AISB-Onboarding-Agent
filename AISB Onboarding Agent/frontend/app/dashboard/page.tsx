"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function DashboardPage() {
	const [applicantId, setApplicantId] = useState<number>(0);
	const [date, setDate] = useState<string>("2025-10-01");
	const [present, setPresent] = useState<boolean>(false);
	const [assignmentFile, setAssignmentFile] = useState<File | null>(null);
	const [assignmentDesc, setAssignmentDesc] = useState<string>("");
	const [resp, setResp] = useState<any>(null);

	async function markAttendance() {
		const res = await fetch(`${API_BASE}/attendance`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ applicant_id: applicantId, date, present }),
		});
		setResp(await res.json());
	}

	async function uploadAssignment() {
		if (!assignmentFile) return;
		const fd = new FormData();
		fd.append("applicant_id", String(applicantId));
		fd.append("description", assignmentDesc);
		fd.append("file", assignmentFile);
		const res = await fetch(`${API_BASE}/assignments/upload`, { method: "POST", body: fd });
		setResp(await res.json());
	}

	return (
		<div className="space-y-6">
			<h2 className="text-xl font-semibold">Student Dashboard</h2>
			<div className="space-y-3 bg-white border p-4 rounded">
				<h3 className="font-medium">Attendance</h3>
				<div className="grid sm:grid-cols-2 gap-3">
					<input className="border p-2 rounded" placeholder="Applicant ID" type="number" value={applicantId} onChange={e=>setApplicantId(Number(e.target.value))}/>
					<input className="border p-2 rounded" placeholder="YYYY-MM-DD" value={date} onChange={e=>setDate(e.target.value)}/>
					<label className="flex items-center gap-2">
						<input type="checkbox" checked={present} onChange={e=>setPresent(e.target.checked)}/>
						<span>Present</span>
					</label>
					<button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={markAttendance}>Mark</button>
				</div>
			</div>

			<div className="space-y-3 bg-white border p-4 rounded">
				<h3 className="font-medium">Assignment Submission</h3>
				<div className="grid sm:grid-cols-2 gap-3">
					<input className="border p-2 rounded" placeholder="Applicant ID" type="number" value={applicantId} onChange={e=>setApplicantId(Number(e.target.value))}/>
					<input className="border p-2 rounded" placeholder="Description" value={assignmentDesc} onChange={e=>setAssignmentDesc(e.target.value)}/>
					<input className="border p-2 rounded" type="file" onChange={e=>setAssignmentFile(e.target.files?.[0]||null)}/>
					<button className="bg-green-600 text-white px-4 py-2 rounded" onClick={uploadAssignment}>Upload</button>
				</div>
			</div>

			{resp && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(resp,null,2)}</pre>
			)}
		</div>
	);
}
