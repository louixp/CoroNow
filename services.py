
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import requests
import json
class NLAPI:
    
    def __init__(self, text):
        self.text = text
        self.client = language.LanguageServiceClient()

    def build(self, lang='en', text_type='PLAIN_TEXT'):
        self.document = types.Document(content=self.text, language=lang, type=text_type)
    
    def pretty_print(self, content):
        print(json.dumps(content, indent=4, sort_keys=True))

    def get_sentiment(self):
        sentiment = self.client.analyze_sentiment(document=self.document).document_sentiment
        result={
            "text": self.text,
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        }
        return result
    
    def get_entities(self, encoding='UTF32'):
        response = self.client.analyze_entities(document=self.document, encoding_type=encoding)
        result=[]
        for entity in response.entities:
            result.append({
                "name": entity.name,
                "type": entity.type,
                "metadata": str(entity.metadata),
                "salience": entity.salience
            })
        return result
    
    def get_entity_sentiments(self, encoding='UTF32'):
        response = self.client.analyze_entity_sentiment(document=self.document, encoding_type=encoding)
        result=[]
        for entity in response.entities:
            result.append({
                "name": entity.name,
                "type": entity.type,
                "metadata": str(entity.metadata),
                "salience": entity.salience,
                "score": entity.sentiment.score,
                "magnitude": entity.sentiment.magnitude
            })
        return result

    def get_syntax(self, encoding='UTF32'):
        response = self.client.analyze_syntax(document=self.document, encoding_type=encoding)
        result=[]
        for token in response.tokens:
            POS = token.part_of_speech
            EPOS = enums.PartOfSpeech 
            result.append({
                "name": token.text.content,
                "offset": token.text.begin_offset,
                "part_of_speech":{
                    "type": EPOS.Tag(POS.tag).name,
                    "aspect": EPOS.Aspect(POS.aspect).name,
                    "case": EPOS.Case(POS.case).name,
                    "form": EPOS.Form(POS.form).name,
                    "gender": EPOS.Gender(POS.gender).name,
                    "mood": EPOS.Mood(POS.mood).name,
                    "number": EPOS.Number(POS.number).name,
                    "proper": EPOS.Proper(POS.proper).name,
                    "tense": EPOS.Tense(POS.tense).name,
                    "reciprocity": EPOS.Reciprocity(POS.reciprocity).name,
                    "voice": EPOS.Voice(POS.voice).name
                },
                "head_token_index": token.dependency_edge.head_token_index,
                "label": token.dependency_edge.label,
                "lemma": token.lemma
            })
        return result


    def classify_text(self):
        



test1 = NLAPI("Google, headquartered in Mountain View, unveiled the new Android phone at the Consumer Electronic Show. Sundar Pichai said in his keynote that users love their new Android phones.")
test1.build()
test1.pretty_print(test1.get_entity_sentiments())
