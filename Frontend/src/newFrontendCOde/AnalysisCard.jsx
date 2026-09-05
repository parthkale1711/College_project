import { motion } from 'framer-motion';

// AnalysisCard component in plain JS
const AnalysisCard = ({ title, icon: Icon, children, variant = 'default', delay = 0 }) => {
  // Classes for different variants
  const variants = {
    default: 'bg-card border-border',
    info: 'bg-primary/5 border-primary/20',
    warning: 'bg-warning/5 border-warning/20',
  };

  const iconVariants = {
    default: 'text-muted-foreground',
    info: 'text-primary',
    warning: 'text-warning',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className={`p-5 rounded-xl border ${variants[variant]}`}
    >
      <h3 className={`text-sm font-semibold mb-3 flex items-center gap-2 ${iconVariants[variant]}`}>
        {Icon && <Icon className="w-4 h-4" />}
        {title}
      </h3>
      {children}
    </motion.div>
  );
};

export default AnalysisCard;
