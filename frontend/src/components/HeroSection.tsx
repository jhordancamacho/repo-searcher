"use client";

import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { useEffect } from "react";
import Header from "@/components/Header";

function BackgroundBlobs() {
	const mouseX = useMotionValue(0);
	const mouseY = useMotionValue(0);

	useEffect(() => {
		const handleMouseMove = (e: MouseEvent) => {
			const x = (e.clientX / window.innerWidth) * 2 - 1;
			const y = (e.clientY / window.innerHeight) * 2 - 1;
			mouseX.set(x);
			mouseY.set(y);
		};
		window.addEventListener("mousemove", handleMouseMove);
		return () => window.removeEventListener("mousemove", handleMouseMove);
	}, [mouseX, mouseY]);

	const smoothOptions = { stiffness: 40, damping: 20 };
	const smoothX = useSpring(mouseX, smoothOptions);
	const smoothY = useSpring(mouseY, smoothOptions);

	const x1 = useTransform(smoothX, [-1, 1], [-80, 80]);
	const y1 = useTransform(smoothY, [-1, 1], [-80, 80]);

	const x2 = useTransform(smoothX, [-1, 1], [100, -100]);
	const y2 = useTransform(smoothY, [-1, 1], [100, -100]);

	const x3 = useTransform(smoothX, [-1, 1], [-60, 60]);
	const y3 = useTransform(smoothY, [-1, 1], [60, -60]);

	return (
		<div className="absolute inset-0 z-0 pointer-events-none">
			<motion.div
				style={{ x: x1, y: y1 }}
				className="absolute top-[5%] left-[10%] w-[70vw] h-[70vw] will-change-transform"
			>
				<motion.div
					animate={{
						x: ["0%", "15%"],
						y: ["0%", "-15%"],
						scale: [1, 1.1],
					}}
					transition={{
						duration: 20,
						repeat: Number.POSITIVE_INFINITY,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="w-full h-full rounded-full bg-zinc-600/30 blur-[200px]"
				/>
			</motion.div>

			<motion.div
				style={{ x: x2, y: y2 }}
				className="absolute top-[30%] right-[5%] w-[60vw] h-[50vw] will-change-transform"
			>
				<motion.div
					animate={{
						x: ["0%", "-20%"],
						y: ["0%", "20%"],
						scale: [1, 1.2],
					}}
					transition={{
						duration: 25,
						repeat: Number.POSITIVE_INFINITY,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="w-full h-full rounded-full bg-white/10 blur-[250px]"
				/>
			</motion.div>

			<motion.div
				style={{ x: x3, y: y3 }}
				className="absolute bottom-[-20%] left-[20%] w-[80vw] h-[60vw] will-change-transform"
			>
				<motion.div
					animate={{
						x: ["0%", "10%"],
						y: ["0%", "10%"],
						scale: [1, 1.1],
					}}
					transition={{
						duration: 15,
						repeat: Number.POSITIVE_INFINITY,
						repeatType: "mirror",
						ease: "easeInOut",
					}}
					className="w-full h-full rounded-full bg-gray-400/20 blur-[220px]"
				/>
			</motion.div>
		</div>
	);
}

function HeroContent() {
	return (
		<div className="relative z-10 text-center flex flex-col items-center max-w-4xl px-6 mt-24">
			<motion.h1
				initial={{ opacity: 0, y: 30 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 1, delay: 0.2 }}
				className="text-5xl md:text-7xl font-extrabold text-white tracking-tighter mb-6 leading-tight drop-shadow-2xl"
			>
				Search any <br />
				<span className="text-transparent bg-clip-text bg-linear-to-r from-zinc-300 via-white to-zinc-500 drop-shadow-none">
					GitHub repository
				</span>
			</motion.h1>

			<motion.p
				initial={{ opacity: 0, y: 30 }}
				animate={{ opacity: 1, y: 0 }}
				transition={{ duration: 1, delay: 0.4 }}
				className="text-lg md:text-xl text-zinc-400 mb-10 max-w-2xl"
			>
				Discover, authenticate, and explore codebases instantly. Start searching
				with our powerful API and integrated chat.
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
	);
}

export default function HeroSection() {
	return (
		<>
			<BackgroundBlobs />
			<Header />
			<HeroContent />
		</>
	);
}
