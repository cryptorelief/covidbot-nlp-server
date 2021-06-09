import spacy
from pathlib import Path
import re

class Model:
    def __init__(self, version):
        modelpath = Path(f'./models/spacy_model_v{version}/')
        self.nlp = spacy.util.load_model_from_path(modelpath)

    def processMessage(self, text, metadata=[]):
        doc = self.nlp(text)
        messageType = self.getMessageType(doc)
        if messageType == 'irrelevant':
            return {'type': messageType}
        
        result = {}
        result['type'] = messageType
        result['resource'] = resource = []
        
        location = None
        for i in doc.ents:
            if i.label_ == 'RES':
                resource.append(i.ent_id_)
                # TODO - Create function for getting plasma
                # if i.ent_id_ in ['plasma', 'blood']:
                #     getBloodGroup(doc)
            if i.label_ == 'LOC':
                location = i.text
            if i.label == 'HOS':
                result['hospital'] = i.text
            if i.label == 'O2L':
                result['OxygenLevel'] = i.text
            if i.label == 'PER':
                result['Name'] = i.text
        
        result['phone'] = self.getPhoneNumbers(text)
        
        # print(metadata)
        if location is None:
            for i in metadata:
                metadoc = self.nlp(i)
                for j in metadoc.ents:
                    if j.label_ == 'LOC':
                        location = j.text
                        break
                if location != None:
                    break
        
        result['location'] = location,
        return result
        

    def getMessageType(self, doc):
        cats = doc.cats
        maxVal = 0
        maxType = None
        for i in cats:
            if cats[i]>maxVal:
                maxVal = cats[i]
                maxType = i
        return maxType
    
    def cleanPhone(self, ph):
        return re.sub(r"[- ]+", "", ph).strip()

    def getPhoneNumbers(self, text):
    #     ph = re.search(r"(?:\D|\A)([ 0-9]{10})(?:\D|\Z)", sample)
        count=0
        spaces=0
        numbers=[]
        for i, char in enumerate(text):
            if char.isnumeric():
                count += 1
            elif char in [' ','-']:
                if count > 0:
                    spaces += 1
            else:
                count = 0
                spaces = 0
            if count >= 10:
                start = i-(count+spaces)+1
                if text[start:start+2] == "91":
                    if count == 12:
                        numbers.append(self.cleanPhone(text[start+2:i+1]))
                        count = 0
                        spaces = 0
                    elif i+1==len(text) or not text[i+1].isnumeric():
                        numbers.append(self.cleanPhone(text[start:i+1]))
                        count = 0
                        spaces = 0
                else:
                    numbers.append(self.cleanPhone(text[start:i+1]))
                    count = 0
                    spaces = 0
                
        return numbers
