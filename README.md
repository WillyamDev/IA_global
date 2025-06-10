# 🌍 Previsão de Desastres Naturais com FastAPI + OpenWeather + Machine Learning

Este projeto usa **FastAPI**, **OpenWeather API** e **Machine Learning** para prever o tipo de desastre mais provável em uma determinada localização, além de gerar um gráfico dos principais desastres históricos registrados no banco de dados EM-DAT.

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório ou extraia o `.zip`

```bash
cd Global
2. Crie o ambiente virtual (opcional mas recomendado)
festança

Cópia

Editar
python3 -m venv venv
source venv/bin/activate  # no Linux/Mac
venv\Scripts\activate  # no Windows
3. Instalar as dependências
festança

Cópia

Editar
pip install -r requirements.txt
4. Configure como variáveis ​​de ambiente
Crie um arquivo .envcom o seguinte conteúdo:

este

Cópia

Editar
OPENWEATHER_API_KEY=SUACHAVEAQUI
EMDAT_CSV_PATH=./data/disasters_ml_ready.csv
Substitua SUACHAVEAQUIpela sua chave da API do OpenWeather.

🧠 Treinando o Modelo de ML
Antes de rodar a aplicação, execute:

festança

Cópia

Editar
python train_model.py
Isso treina e salva um modelo para prever o tipo de desastre com base em localização, país, nome do evento e outros atributos históricos.

🌐 Executando uma API
festança

Cópia

Editar
uvicorn app.main:app --reload
Abra no navegador: http://127.0.0.1:8000/docs para testar a API interativamente.

📥 Exemplo de Requisição
json

Cópia

Editar
POST /predict-disaster
{
  "location": "Japan"
}
Resposta atenciosa:

json

Cópia

Editar
{
  "message": "Previsão para Japan indica condições normais com temperatura de 22°C e clima clear sky.",
  "graph_urls": {
    "pizza_graph": "disasters_pie_Japan.png"
  },
  "predicted_disaster_type": "Flood"
}
📊 Sobre o Gráfico
O gráfico gerado ( .png) representa os 5 maiores desastres registrados no país informado, com base em número de afetados, extraído do conjunto de dados EM-DAT.

📁 Estrutura da Aplicação
festança

Cópia

Editar
IA_global/
├── app/
│   └── main.py
├── data/
│   └── disasters_ml_ready.csv
├── model/
│   └── disaster_model.pkl
├── train_model.py
├── requirements.txt
└── .env
🧪 Testado em
Python 3.10+

FastAPI 0.110+

scikit-learn, pandas, matplotlib, python-dotenv

👨‍🏫 Ideal para entrega acadêmica
Você pode enviar este projeto diretamente ao professor. Ele está estruturado como:

API funcional

ML integrado

Visualização histórica

Documentação clara e reproduzível

📺 Vídeo de Demonstração
Confira a demonstração completa do projeto no YouTube:

https://www.youtube.com/watch?v=QR8c_XG6krQ

🌍 Repositório no GitHub
O código completo do projeto está disponível no GitHub:

https://github.com/WillyamDev/IA_global
