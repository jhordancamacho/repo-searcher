"use client";
import Header from "@/components/Header";
import { motion } from "framer-motion";

export default function Home() {
	return (
		<main className="relative min-h-screen w-full bg-black overflow-hidden flex flex-col items-center justify-center">
			{/* Background Blur Motion */}
			<div className="absolute inset-0 z-0 pointer-events-none">
				<motion.div
					animate={{
						x: ["0%", "20%", "-10%", "0%"],
						y: ["0%", "-20%", "10%", "0%"],
						scale: [1, 1.2, 0.9, 1],
					}}
					transition={{
						duration: 20,
						repeat: Infinity,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="absolute top-[10%] left-[20%] w-[50vw] h-[50vw] will-change-transform"
				>
					<div className="w-full h-full rounded-full bg-zinc-600/30 blur-[140px]" />
				</motion.div>

				<motion.div
					animate={{
						x: ["0%", "-30%", "20%", "0%"],
						y: ["0%", "30%", "-20%", "0%"],
						scale: [1, 0.8, 1.1, 1],
					}}
					transition={{
						duration: 25,
						repeat: Infinity,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="absolute top-[40%] right-[10%] w-[40vw] h-[30vw] will-change-transform"
				>
					<div className="w-full h-full rounded-full bg-white/20 blur-[130px]" />
				</motion.div>

				<motion.div
					animate={{
						x: ["0%", "10%", "-10%", "0%"],
						y: ["0%", "15%", "-15%", "0%"],
						scale: [1, 1.1, 1, 1],
					}}
					transition={{
						duration: 15,
						repeat: Infinity,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="absolute bottom-[-10%] left-[30%] w-[60vw] h-[40vw] will-change-transform"
				>
					<div className="w-full h-full rounded-full bg-gray-400/20 blur-[150px]" />
				</motion.div>
			</div>

			{/* Header with Login Button */}
			<Header />

			{/* Main Hero Content */}
			<div className="relative z-10 text-center flex flex-col items-center max-w-4xl px-6 mt-24">
				<motion.h1
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 1, delay: 0.2 }}
					className="text-5xl md:text-7xl font-extrabold text-white tracking-tighter mb-6 leading-tight drop-shadow-2xl"
				>
					Search any <br />
					<span className="text-transparent bg-clip-text bg-gradient-to-r from-zinc-300 via-white to-zinc-500 drop-shadow-none">
						GitHub repository
					</span>
				</motion.h1>

				<motion.p
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 1, delay: 0.4 }}
					className="text-lg md:text-xl text-zinc-400 mb-10 max-w-2xl"
				>
					Discover, authenticate, and explore codebases instantly. Start
					searching with our powerful API and integrated chat.
				</motion.p>

				<motion.div
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 1, delay: 0.6 }}
					className="flex items-center gap-4"
				>
					<button
						type="button"
						className="px-8 py-4 bg-white text-black font-semibold rounded-full text-lg hover:bg-zinc-200 transition-colors shadow-[0_0_30px_rgba(255,255,255,0.3)]"
					>
						Explore Repos
					</button>
					<button
						type="button"
						className="px-8 py-4 bg-transparent border border-white/20 text-white font-semibold rounded-full text-lg hover:bg-white/10 transition-colors"
					>
						View Docs
					</button>
				</motion.div>
			</div>
		</main>
	);
}
