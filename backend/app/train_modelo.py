import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

# Caminho para os arquivos
csv_file_path = os.path.join("app", "data", "data.csv")  # Caminho do arquivo CSV
model_path = os.path.join("app", "data", "datacsvautalizado.pkl")  # Caminho do modelo

# Carregar o arquivo CSV
df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')

# Verificar a estrutura do dataframe
print(f"Primeiras linhas do CSV: {df.head()}")

# Preprocessamento dos dados
df["Country"] = df["Country"].astype(str)  # Garantir que a coluna "Country" é do tipo string

# Encode para a coluna "Country"
label_encoder = LabelEncoder()
df["Country"] = label_encoder.fit_transform(df["Country"])

# Definir as variáveis independentes (X) e dependente (y)
X = df[["Country", "Start Year", "Total Affected"]]  # Exemplo de características
y = df["Disaster Type"]  # Coluna alvo (tipo de desastre)

# Dividir o dataset em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Salvar o modelo treinado
joblib.dump(model, model_path)

# Salvar o encoder de país
joblib.dump(label_encoder, os.path.join("app", "data", "country_encoder.pkl"))

print(f"Modelo treinado e salvo em {model_path}")
