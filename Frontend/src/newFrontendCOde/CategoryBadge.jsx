const CategoryBadge = ({ category, selected, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-xs font-medium rounded-full transition-all duration-200 ${
        selected
          ? 'bg-gradient-primary text-primary-foreground shadow-sm'
          : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
      }`}
    >
      {category}
    </button>
  );
};

export default CategoryBadge;
