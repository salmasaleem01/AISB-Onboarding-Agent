"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function ApplyPage() {
	const [form, setForm] = useState({
		name: "",
		email: "",
		age: 18,
		degree: "",
		skills: "",
		track_preference: "Generative",
	});
	const [result, setResult] = useState<any>(null);

	async function submit() {
		const res = await fetch(`${API_BASE}/apply`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(form),
		});
		const data = await res.json();
		setResult(data);
	}

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Application Form</h2>
			<div className="grid gap-3">
				<input className="border p-2 rounded" placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
				<input className="border p-2 rounded" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
				<input className="border p-2 rounded" placeholder="Age" type="number" value={form.age} onChange={e=>setForm({...form,age:Number(e.target.value)})}/>
				<input className="border p-2 rounded" placeholder="Degree (e.g., BS CS)" value={form.degree} onChange={e=>setForm({...form,degree:e.target.value})}/>
				<textarea className="border p-2 rounded" placeholder="Skills (comma separated)" value={form.skills} onChange={e=>setForm({...form,skills:e.target.value})}/>
				<select className="border p-2 rounded" value={form.track_preference} onChange={e=>setForm({...form,track_preference:e.target.value})}>
					<option>Generative</option>
					<option>Agentic</option>
				</select>
				<button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={submit}>Submit</button>
			</div>
			{result && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(result,null,2)}</pre>
			)}
		</div>
	);
}
