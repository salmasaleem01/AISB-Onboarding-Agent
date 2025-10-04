"use client";
import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function QuizPage() {
	const [applicantId, setApplicantId] = useState<number>(0);
	const [questions, setQuestions] = useState<any[]>([]);
	const [answers, setAnswers] = useState<Record<number,string>>({});
	const [result, setResult] = useState<any>(null);

	async function generate() {
		const res = await fetch(`${API_BASE}/quiz/generate`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ applicant_id: applicantId, num_questions: 5 }),
		});
		const data = await res.json();
		setQuestions(data.questions || []);
	}

	async function submit() {
		const res = await fetch(`${API_BASE}/quiz/submit`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ applicant_id: applicantId, answers }),
		});
		const data = await res.json();
		setResult(data);
	}

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Quiz</h2>
			<div className="flex gap-2 items-center">
				<input className="border p-2 rounded" placeholder="Applicant ID" type="number" value={applicantId} onChange={e=>setApplicantId(Number(e.target.value))}/>
				<button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={generate}>Generate Quiz</button>
			</div>
			<div className="space-y-4">
				{questions.map((q, idx) => (
					<div key={q.id} className="bg-white border p-3 rounded">
						<div className="font-medium">Q{idx+1}. {q.question}</div>
						<div className="grid gap-2 mt-2">
							{q.options.map((opt: string, i: number) => {
								const key = ["A","B","C","D"][i] || String.fromCharCode(65+i);
								return (
									<label key={i} className="flex items-center gap-2">
										<input type="radio" name={`q${q.id}`} onChange={()=>setAnswers({...answers, [q.id]: key})} checked={answers[q.id]===key}/>
										<span>{key}. {opt}</span>
									</label>
								);
							})}
						</div>
					</div>
				))}
			</div>
			{questions.length>0 && (
				<button className="bg-green-600 text-white px-4 py-2 rounded" onClick={submit}>Submit Answers</button>
			)}
			{result && (
				<pre className="bg-gray-100 p-3 rounded overflow-auto text-sm">{JSON.stringify(result,null,2)}</pre>
			)}
		</div>
	);
}
