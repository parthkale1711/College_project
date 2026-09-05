import { motion } from "framer-motion";

const ConfidenceGauge = ({ confidence, isFake }) => {
  const value = Math.min(100, Math.max(0, confidence));
  const angle = (value / 100) * 270 - 135;

  const color = isFake
    ? "hsl(0, 72%, 55%)"
    : "hsl(142, 65%, 45%)";

  return (
    <div className="relative w-40 h-40 mx-auto">
      <svg viewBox="0 0 200 200" className="w-full h-full">
        {/* Progress arc ONLY (no background ring) */}
        <motion.path
          d={`M 30 130 A 70 70 0 ${value > 50 ? 1 : 0} 1 ${
            100 + Math.cos((angle * Math.PI) / 180) * 70
          } ${
            100 + Math.sin((angle * Math.PI) / 180) * 70
          }`}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeLinecap="round"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.9, ease: "easeOut" }}
        />
      </svg>

      {/* Center text — OPTICALLY centered */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none -translate-y-1">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.35 }}
          className="text-3xl font-bold text-slate-900 tabular-nums leading-none"
        >
          {value}%
        </motion.div>

        <span className="mt-1 text-[11px] font-semibold tracking-wide uppercase text-slate-500">
          Confidence
        </span>
      </div>
    </div>
  );
};

export default ConfidenceGauge;
