import "./globals.css";
import React from "react";

export const metadata = {
	title: "Bootcamp Onboarding",
	description: "AI Bootcamp Onboarding Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html lang="en">
			<body className="min-h-screen">
				<div className="max-w-5xl mx-auto p-6">{children}</div>
			</body>
		</html>
	);
}
