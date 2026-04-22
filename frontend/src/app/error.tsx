"use client";

export default function ErrorPage({
	reset,
}: {
	error: globalThis.Error & { digest?: string };
	reset: () => void;
}) {
	return (
		<main className="min-h-screen bg-black flex flex-col items-center justify-center px-6 text-center">
			<h1 className="text-6xl font-extrabold text-white tracking-tighter mb-4">
				Oops
			</h1>
			<p className="text-xl text-zinc-400 mb-8 max-w-md">
				Something went wrong. Please try again.
			</p>
			<button
				type="button"
				onClick={() => reset()}
				className="px-8 py-4 bg-white text-black font-semibold rounded-full text-lg hover:bg-zinc-200 transition-colors shadow-[0_0_30px_rgba(255,255,255,0.3)]"
			>
				Try again
			</button>
		</main>
	);
}
