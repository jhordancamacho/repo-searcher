"use client";
import { motion } from "framer-motion";
import { User } from "lucide-react";

export default function Header() {
	return (
		<motion.header
			initial={{ opacity: 0, y: -20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ duration: 0.5 }}
			className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 border-b border-white/5 bg-black/20 backdrop-blur-xl"
		>
			<div className="flex items-center gap-3">
				<div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center border border-white/20 shadow-[0_0_15px_rgba(255,255,255,0.1)]">
					<span className="text-white font-bold text-lg">RS</span>
				</div>
				<span className="text-white font-semibold tracking-tight text-lg">
					Repo Searcher
				</span>
			</div>
			<button
				type="button"
				className="flex items-center gap-2 px-5 py-2.5 bg-white text-black hover:bg-zinc-200 hover:scale-105 active:scale-95 transition-all rounded-full font-medium text-sm shadow-[0_0_20px_rgba(255,255,255,0.2)]"
			>
				<User className="w-4 h-4" />
				Login
			</button>
		</motion.header>
	);
}
