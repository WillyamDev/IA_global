from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import joblib
import os

# Caminhos
csv_path = "../data/public_emdat_custom_request_2025-06-02_4a01e99a-3a89-4154-b5a0-2cdadd208c80_prepared.csv"
model_path = "../data/public_emdat_custom_request_2025-06-02_4a01e99a-3a89-4154-b5a0-2cdadd208c80_prepared.pkl"

# Criar a pasta se não existir
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# Carregar os dados
df = pd.read_csv(csv_path)

# Separar X e y
X = df.drop(columns=["Disaster Type"])
y = df["Disaster Type"]

# Codificar países
country_encoder = LabelEncoder()
X["Country"] = country_encoder.fit_transform(X["Country"])

# Dividir os dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Salvar modelo + encoder
joblib.dump((model, country_encoder), model_path)
print(f"Modelo salvo em {model_path}")
