from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Gerenciamento de Tráfego Aéreo Simulado",
    description="API inicial do projeto acadêmico de engenharia de software.",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "API do sistema de tráfego aéreo simulada online."}

@app.get("/health")
def health_check():
    return {"status": "ok"}