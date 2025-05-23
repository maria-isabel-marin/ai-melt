import spacy

class Postprocessor:
    """
    Agrupa tokens en expresiones completas y expande contexto.
    """
    def __init__(self, model: str = "es_core_news_sm"):
        self.nlp = spacy.load(model)

    def expand_expression(self, sentence: str, entity: dict) -> str:
        """Dado el offset de una entidad, expande a frase completa o sintagma relevante."""
        doc = self.nlp(sentence)
        span = doc.char_span(entity['start'], entity['end'])
        if not span:
            return entity['word']
        # ejemplo: añadir complementos directos
        tokens = [tok.text for tok in span]
        for child in span.root.children:
            if child.dep_ in ("dobj", "obj"):
                tokens.append(child.text)
        return " ".join(tokens)