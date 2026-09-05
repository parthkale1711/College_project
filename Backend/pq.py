import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

print("Loading dataset...")
df = pd.read_csv("datasets/IFND.csv")  # Adjust path if needed

# ── Clean up ───────────────────────────────────────────────────────────────
df = df.dropna(subset=['Statement', 'Label'])
df['Label'] = df['Label'].str.strip()

# ── Encode labels: TRUE = 0, Fake = 1 ─────────────────────────────────────
df['label_encoded'] = df['Label'].map({'TRUE': 0, 'Fake': 1})
df = df.dropna(subset=['label_encoded'])

print(f"Total usable records: {len(df)}")
print(f"TRUE: {(df['label_encoded']==0).sum()}, Fake: {(df['label_encoded']==1).sum()}")

# ── Features and labels ────────────────────────────────────────────────────
X_text = df['Statement'].astype(str)
y = df['label_encoded'].astype(int)

# ── Train test split ───────────────────────────────────────────────────────
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining set: {len(X_train_text)} articles")
print(f"Test set: {len(X_test_text)} articles")

# ── TF-IDF Vectorization ───────────────────────────────────────────────────
print("\nRunning TF-IDF vectorization...")
tfidf = TfidfVectorizer(max_features=12000, stop_words='english')
X_train_tfidf = tfidf.fit_transform(X_train_text)
X_test_tfidf = tfidf.transform(X_test_text)

# ── Apply SMOTE on training data ───────────────────────────────────────────
print("Applying SMOTE to balance training data...")
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_tfidf, y_train)
print(f"After SMOTE - TRUE: {(y_train_balanced==0).sum()}, Fake: {(y_train_balanced==1).sum()}")

# ── Train all three models ─────────────────────────────────────────────────
print("\nTraining LinearSVC...")
svc = LinearSVC(C=0.5, random_state=42, max_iter=2000)
svc.fit(X_train_balanced, y_train_balanced)

print("Training Logistic Regression...")
lr = LogisticRegression(solver='saga', max_iter=1000, random_state=42)
lr.fit(X_train_balanced, y_train_balanced)

print("Training Gradient Boosting...")
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb.fit(X_train_balanced, y_train_balanced)

# ── Get predictions from each model ───────────────────────────────────────
print("\nGenerating predictions...")
svc_preds = svc.predict(X_test_tfidf)
lr_preds = lr.predict(X_test_tfidf)
gb_preds = gb.predict(X_test_tfidf)

# ── Ensemble majority voting ───────────────────────────────────────────────
ensemble_preds = []
for i in range(len(y_test)):
    votes = [svc_preds[i], lr_preds[i], gb_preds[i]]
    ensemble_preds.append(1 if sum(votes) >= 2 else 0)
ensemble_preds = np.array(ensemble_preds)

# ── Evaluation function ────────────────────────────────────────────────────
def evaluate(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred) * 100
    prec = precision_score(y_true, y_pred, zero_division=0) * 100
    rec = recall_score(y_true, y_pred, zero_division=0) * 100
    f1 = f1_score(y_true, y_pred, zero_division=0) * 100
    return acc, prec, rec, f1

# ── Print results table ────────────────────────────────────────────────────
print("\n" + "="*65)
print(f"{'Model':<28} {'Accuracy':>8} {'Precision':>10} {'Recall':>8} {'F1':>8}")
print("="*65)

models = [
    ("LinearSVC", svc_preds),
    ("Logistic Regression", lr_preds),
    ("Gradient Boosting", gb_preds),
    ("Ensemble (Majority Vote)", ensemble_preds),
]

y_test_array = np.array(y_test)

for name, preds in models:
    acc, prec, rec, f1 = evaluate(name, y_test_array, preds)
    print(f"{name:<28} {acc:>7.2f}% {prec:>9.2f}% {rec:>7.2f}% {f1:>7.2f}%")

print("="*65)

# ── Confusion matrix for ensemble ─────────────────────────────────────────
print("\nConfusion Matrix (Ensemble):")
cm = confusion_matrix(y_test_array, ensemble_preds)
print(f"                  Predicted TRUE    Predicted FAKE")
print(f"Actual TRUE       {cm[0][0]:<18} {cm[0][1]}")
print(f"Actual FAKE       {cm[1][0]:<18} {cm[1][1]}")

print("\nDone! Copy these numbers into your paper.")
