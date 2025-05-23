# Configuración global 
environment = {
    "HUGGINGFACE_MODEL": "HiTZ/mdeberta-base-metaphor-detection-es",
    "AGGREGATION_STRATEGY": "simple",
    "METAFORAS_KNOWN_PATH": "resources/metaforas_conocidas.json",
    "CONCRETENESS_LEXICON_PATH": "resources/concreteness_lexicon.csv",
    "WEB_FREQ_THRESHOLD": 10000,
}

# Lista de modelos activos (personalizable por el usuario)
active_models = [
    "llama_3_70b_quant"
]

model_configs = {
    "hitz_deberta": {
        "type": "huggingface",
        "model_name": "HiTZ/mdeberta-base-metaphor-detection-es",
        "aggregation_strategy": "simple"
    },
    "lwachowiak_xlmr": {
        "type": "huggingface",
        "model_name": "lwachowiak/Metaphor-Detection-XLMR",
        "aggregation_strategy": "simple"
    },
    "openai_gpt": {
        "type": "openai",
        "model": "gpt-4",
        "api_key_env": "OPENAI_API_KEY"  
    },
    "gemini": {
        "type": "google",
        "model": "gemini-pro",
        "api_key_env": "GOOGLE_API_KEY"
    },
    "llama_api": {
        "type": "huggingface",
        "model_name": "meta-llama/Llama-3.1-70B-Instruct",
        "aggregation_strategy": "simple"
    },
    "mistral_api": {
        "type": "mistral",
        "model": "mistral-7b-instruct-v0.2",
        "api_url": "https://api.mistral.example/infer",
        "api_key_env": "MISTRAL_API_KEY"
    },
    "llama_3_70b_quant": {
        "type": "huggingface",
        "model_name": "RedHatAI/Meta-Llama-3.1-70B-Instruct-quantized.w8a16",
        "aggregation_strategy": "simple"
    }
}
