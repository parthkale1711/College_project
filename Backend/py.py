import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset (adjust path if needed)
df = pd.read_csv("datasets/IFND.csv", header=None)  # no header in your example

# Assign column names based on your example
df.columns = ["ID", "Statement", "Web", "Category", "Date", "Label"]

# Strip extra spaces (if any)
df['Label'] = df['Label'].str.strip()

# Count Fake vs Real
counts = df['Label'].value_counts()
print("Article Counts:\n", counts)

# Percentage distribution
percentages = df['Label'].value_counts(normalize=True) * 100
print("\nPercentage Distribution:\n", percentages.round(2))

# Total number of articles
total_articles = len(df)
print("\nTotal Articles:", total_articles)

# Optional: Bar chart for visualization
counts.plot(kind='bar', color=['green', 'red'])
plt.title("Distribution of Real vs Fake News")
plt.xlabel("Label")
plt.ylabel("Number of Articles")
plt.show()