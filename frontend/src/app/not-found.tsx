import Link from "next/link";

export default function NotFound() {
	return (
		<main className="min-h-screen bg-black flex flex-col items-center justify-center px-6 text-center">
			<h1 className="text-8xl font-extrabold text-white tracking-tighter mb-4">
				404
			</h1>
			<p className="text-xl text-zinc-400 mb-8 max-w-md">
				The page you're looking for doesn't exist or has been moved.
			</p>
			<Link
				href="/"
				className="px-8 py-4 bg-white text-black font-semibold rounded-full text-lg hover:bg-zinc-200 transition-colors shadow-[0_0_30px_rgba(255,255,255,0.3)]"
			>
				Back to Home
			</Link>
		</main>
	);
}
