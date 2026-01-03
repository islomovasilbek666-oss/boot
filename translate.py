# services/translate.py
from googletrans import Translator

translator = Translator()

def en_to_uz(text: str) -> str:
    """Inglizcha matnni O‘zbekchaga tarjima qiladi"""
    result = translator.translate(text, src='en', dest='uz')
    return result.text

def uz_to_en(text: str) -> str:
    """O‘zbekcha matnni Inglizchaga tarjima qiladi"""
    result = translator.translate(text, src='uz', dest='en')
    return result.text