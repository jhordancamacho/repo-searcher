import type { Metadata } from "next";
import HeroSection from "@/components/HeroSection";

export const metadata: Metadata = {
	title: "Repo Searcher — Search any GitHub repository",
	description:
		"Discover, authenticate, and explore codebases instantly with a powerful search API and integrated chat.",
};

export default function Home() {
	return (
		<main className="relative min-h-screen w-full bg-black overflow-hidden flex flex-col items-center justify-center">
			<HeroSection />
		</main>
	);
}
