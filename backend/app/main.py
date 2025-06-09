import pandas as pd
import requests
import matplotlib.pyplot as plt
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import joblib

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

# Caminho dos arquivos
csv_file_path = os.getenv("EMDAT_CSV_PATH")
model_path = os.path.join("data", "public_emdat_custom_request_2025-06-02_4a01e99a-3a89-4154-b5a0-2cdadd208c80_prepared.pkl")

# OpenWeather API
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# Classe para entrada
class LocationRequest(BaseModel):
    location: str

# Obter dados da OpenWeather
def get_weather_data(location: str):
    params = {
        'q': location,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(OPENWEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro ao obter dados da OpenWeather.")

# Prever tipo de desastre
def predict_disaster_type(location: str):
    try:
        model, country_encoder = joblib.load(model_path)

        # Padronizar o nome
        location = location.strip().title()

        # Verifica se o país existe no encoder
        if location not in country_encoder.classes_:
            return "Sem histórico suficiente para previsão."

        encoded_country = country_encoder.transform([location])[0]
        
        # Remover a coluna "Disaster Type" da previsão
        input_df = pd.DataFrame([{
            "Country": encoded_country,
            "Start Year": 2023,
            "Total Affected": 0  # Usando 0 como valor padrão para "Total Affected"
        }])

        # Prever o tipo de desastre
        prediction = model.predict(input_df)
        return prediction[0]

    except Exception as e:
        return f"Erro ao prever desastre: {str(e)}"



# Gerar gráfico de pizza
def generate_disaster_graph(location: str):
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
        df["Country"] = df["Country"].astype(str)  # Garantir tipo string

        disasters_in_location = df[df["Country"].str.contains(location, case=False, na=False)]
        disaster_types = ['Earthquake', 'Wildfire', 'Flood', 'Storm', 'Drought']
        disasters_filtered = disasters_in_location[disasters_in_location['Disaster Type'].isin(disaster_types)]

        if disasters_filtered.empty:
            return None

        # Corrigido: Usando .loc para evitar SettingWithCopyWarning
        disasters_filtered.loc[:, "Total Affected"] = pd.to_numeric(disasters_filtered["Total Affected"], errors="coerce")
        disasters_filtered = disasters_filtered.dropna(subset=["Total Affected"])

        # Verificando se há dados para plotar
        if disasters_filtered.empty:
            return None

        top_disasters = disasters_filtered.nlargest(5, 'Total Affected')

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            top_disasters['Total Affected'],
            labels=top_disasters['Disaster Type'].fillna('Desastre Desconhecido'),  # Usando 'Disaster Type' em vez de 'Event Name'
            autopct='%1.1f%%',
            startangle=90
        )
        ax.axis('equal')
        ax.set_title(f'Top 5 Desastres em {location}')
        pizza_graph_path = f"disasters_pie_{location}.png"
        plt.tight_layout()
        plt.savefig(pizza_graph_path)
        plt.close()
        return { "pizza_graph": pizza_graph_path }

    except Exception as e:
        raise Exception(f"Erro ao processar dados do EM-DAT: {e}")

# Endpoint principal
@app.post("/predict-disaster")
async def predict_disaster(request: LocationRequest):
    location = request.location
    try:
        weather_data = get_weather_data(location)
        temperature = weather_data["main"]["temp"]
        weather_description = weather_data["weather"][0]["description"]

        graph_paths = generate_disaster_graph(location)
        predicted_disaster = predict_disaster_type(location)

        return {
            "message": f"Previsão para {location}: {temperature}°C, {weather_description}.",
            "predicted_disaster_type": predicted_disaster,
            "graph_urls": graph_paths
        }
    except Exception as e:
        return { "message": "Erro ao processar dados.", "error": str(e) }
