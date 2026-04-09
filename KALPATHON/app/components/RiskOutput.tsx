import { motion } from 'motion/react';
import { Scale, Shield, AlertCircle } from 'lucide-react';

interface RiskBadgeProps {
  risk: 'Low' | 'Medium' | 'High';
}

export function RiskBadge({ risk }: RiskBadgeProps) {
  const config = {
    Low: {
      color: 'from-green-500 to-emerald-500',
      glow: 'shadow-[0_0_30px_rgba(34,197,94,0.5)]',
      border: 'border-green-500/50',
      icon: Shield,
    },
    Medium: {
      color: 'from-yellow-500 to-amber-500',
      glow: 'shadow-[0_0_30px_rgba(245,158,11,0.5)]',
      border: 'border-yellow-500/50',
      icon: AlertCircle,
    },
    High: {
      color: 'from-red-500 to-rose-500',
      glow: 'shadow-[0_0_30px_rgba(239,68,68,0.5)]',
      border: 'border-red-500/50',
      icon: AlertCircle,
    },
  };

  const { color, glow, border, icon: Icon } = config[risk];

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className={`inline-flex items-center gap-2 px-6 py-3 rounded-full bg-gradient-to-r ${color} ${glow} ${border} border backdrop-blur-xl`}
    >
      <Icon className="w-5 h-5 text-white" />
      <span className="text-white font-semibold tracking-wide">{risk} Risk</span>
    </motion.div>
  );
}

interface RiskOutputCardProps {
  risk: 'Low' | 'Medium' | 'High';
  explanation: string;
}

export function RiskOutputCard({ risk, explanation }: RiskOutputCardProps) {
  const glowColors = {
    Low: 'shadow-[0_0_60px_rgba(34,197,94,0.3),inset_0_0_60px_rgba(34,197,94,0.1)] border-green-500/30',
    Medium: 'shadow-[0_0_60px_rgba(245,158,11,0.3),inset_0_0_60px_rgba(245,158,11,0.1)] border-yellow-500/30',
    High: 'shadow-[0_0_60px_rgba(239,68,68,0.3),inset_0_0_60px_rgba(239,68,68,0.1)] border-red-500/30',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`glass-card p-8 ${glowColors[risk]} animate-pulse-glow`}
    >
      <div className="flex flex-col gap-6">
        <RiskBadge risk={risk} />
        
        <div className="space-y-3">
          <h3 className="text-xl font-semibold text-white/90">Plain English Explanation</h3>
          <p className="text-base leading-relaxed text-white/80 font-light">
            {explanation}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
