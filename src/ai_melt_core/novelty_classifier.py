import json
import requests
from ai_melt_core.config import environment

class NoveltyClassifier:
    """
    Clasifica las expresiones como convencionales o novedosas.
    """
    def __init__(self):
        # with open(environment['METAFORAS_KNOWN_PATH'], 'r', encoding='utf-8') as f:
        #self.known = set(json.load(f))
        self.known = set([
            "perder la cabeza",
            "romper el hielo",
            "lluvia de ideas",
            "abrir puertas",
            "ganar terreno"        ])
        self.threshold = environment['WEB_FREQ_THRESHOLD']

    def is_conventional(self, expression: str) -> bool:
        # Verifica lista de metáforas conocidas
        if expression.lower() in self.known:
            return True
        # Verifica frecuencia en web (Bing Search API)
        # url = f"https://api.bing.microsoft.com/v7.0/search?q=\"{expression}\""
        # Aquí se asume que se configura la API key en encabezados
        # res = requests.get(url, headers={"Ocp-Apim-Subscription-Key": "<YOUR_KEY>"})
        # count = res.json().get('webPages', {}).get('totalEstimatedMatches', 0)
        count = 10
        return count >= self.threshold

    def label(self, expression: str) -> str:
        return "convencional" if self.is_conventional(expression) else "novedosa"