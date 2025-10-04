import Link from "next/link";

export default function HomePage() {
	return (
		<div className="space-y-4">
			<h1 className="text-2xl font-semibold">Bootcamp Onboarding</h1>
			<div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
				<Link className="px-4 py-3 bg-white border rounded" href="/apply">Apply</Link>
				<Link className="px-4 py-3 bg-white border rounded" href="/quiz">Quiz</Link>
				<Link className="px-4 py-3 bg-white border rounded" href="/video">Video Upload</Link>
				<Link className="px-4 py-3 bg-white border rounded" href="/admin">Admin Panel</Link>
				<Link className="px-4 py-3 bg-white border rounded" href="/dashboard">Student Dashboard</Link>
			</div>
		</div>
	);
}
