import { motion } from 'motion/react';

export function Scene3D() {
  return (
    <div className="relative w-full h-full flex items-center justify-center">
      {/* Animated Gradient Orbs */}
      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          rotate: [0, 180, 360],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute w-96 h-96 rounded-full bg-gradient-to-r from-indigo-500/30 via-purple-500/30 to-blue-500/30 blur-3xl"
      />
      
      <motion.div
        animate={{
          scale: [1.2, 1, 1.2],
          rotate: [360, 180, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute w-80 h-80 rounded-full bg-gradient-to-l from-purple-500/20 via-pink-500/20 to-indigo-500/20 blur-2xl"
      />

      <motion.div
        animate={{
          y: [-50, 50, -50],
          x: [-30, 30, -30],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute w-64 h-64 rounded-full bg-gradient-to-br from-blue-500/25 via-cyan-500/25 to-indigo-500/25 blur-2xl"
      />

      {/* Geometric Shapes */}
      <motion.div
        animate={{
          rotateX: [0, 360],
          rotateY: [0, 360],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute w-48 h-48 border border-indigo-500/20 rounded-3xl backdrop-blur-sm"
        style={{ transform: 'perspective(1000px) rotateX(45deg) rotateY(45deg)' }}
      />

      <motion.div
        animate={{
          rotateX: [360, 0],
          rotateZ: [0, 360],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute w-64 h-64 border border-purple-500/15 rounded-full backdrop-blur-sm"
        style={{ transform: 'perspective(1000px) rotateX(60deg)' }}
      />
    </div>
  );
}
