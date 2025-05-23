import spacy

class Preprocessor:
    """
    Encargado de dividir el texto en oraciones y tokenizar, limpiando caracteres inválidos.
    """
    def __init__(self, model: str = "es_core_news_sm"):
        self.nlp = spacy.load(model)

    def clean_text(self, text: str) -> str:
        """Elimina caracteres no decodificables en UTF-8."""
        # Ignorar caracteres que no puedan codificarse en UTF-8
        return text.encode('utf-8', 'ignore').decode('utf-8')

    def split_sentences(self, text: str) -> list[str]:
        """Limpia el texto y lo divide en oraciones."""
        cleaned = self.clean_text(text)
        doc = self.nlp(cleaned)
        return [sent.text for sent in doc.sents]

    def lemmatize(self, text: str) -> str:
        """Devuelve el lematizado de una oración o expresión."""
        cleaned = self.clean_text(text)
        doc = self.nlp(cleaned)
        return " ".join([token.lemma_ for token in doc])