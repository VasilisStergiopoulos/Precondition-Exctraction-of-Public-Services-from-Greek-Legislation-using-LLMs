import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL


class LLMExtractor:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def extract_preconditions(self, process_id: str, text: str) -> dict:
        prompt = f"""
Εξήγαγε τις προϋποθέσεις παροχής δημόσιας υπηρεσίας από το παρακάτω κείμενο.

Ορισμός:
Ως "προϋπόθεση" θεωρείται οποιαδήποτε απαίτηση που πρέπει να πληροί ο αιτών
πριν από την παροχή της υπηρεσίας (π.χ. ηλικία, κατοικία, εισόδημα, έγγραφα, εργασιακή κατάσταση).

ΜΗΝ περιλαμβάνεις:
- περιγραφές διαδικασιών
- γενικές πληροφορίες
- επεξηγηματικά σχόλια
- μη δεσμευτικές διατυπώσεις

Μορφή εξόδου:
ΕΠΙΣΤΡΕΨΕ ΜΟΝΟ ΕΓΚΥΡΟ JSON (χωρίς markdown ή εξηγήσεις):

{{
  "process_id": "{process_id}",
  "preconditions": [
    {{
      "text": "ακριβές απόσπασμα προϋπόθεσης από το κείμενο",
      "category": "age|residency|income|document|family_status|employment|other",
      "applicant_type": "σε ποιον αφορά ή null",
      "legal_reference": "ακριβής αναφορά (π.χ. Άρθρο 5, παρ. 2) ή null",
      "confidence": 0.0
    }}
  ]
}}

Κανόνες εξαγωγής:
- Διατήρησε το κείμενο της προϋπόθεσης ΑΚΡΙΒΩΣ όπως εμφανίζεται (χωρίς παραφράσεις).
- ΜΗΝ εφευρίσκεις πληροφορίες που δεν υπάρχουν στο κείμενο.
- Αν μια πρόταση περιέχει πολλαπλές προϋποθέσεις, χώρισέ τις σε ξεχωριστές εγγραφές.
- Αφαίρεσε διπλότυπες προϋποθέσεις.
- Αν δεν υπάρχει σαφής προϋπόθεση, αγνόησέ την.
- Αν δεν εντοπιστούν προϋποθέσεις, επέστρεψε:
  {{"process_id": "{process_id}", "preconditions": []}}

Κατηγορίες (υποχρεωτικά μία από τις παρακάτω):
- age: ηλικιακά όρια
- residency: τόπος κατοικίας ή διαμονής
- income: εισοδηματικά ή οικονομικά κριτήρια
- document: απαιτούμενα έγγραφα ή πιστοποιητικά
- family_status: οικογενειακή κατάσταση
- employment: εργασιακή κατάσταση
- other: οτιδήποτε δεν ανήκει στα παραπάνω

Ειδικοί κανόνες:
- Το πεδίο "category" ΠΡΕΠΕΙ να είναι μία από τις προκαθορισμένες τιμές.
- Αν δεν υπάρχει πληροφορία για κάποιο πεδίο, βάλε null.
- Αν υπάρχει νομική αναφορά (άρθρο, παράγραφος), εξήγαγε την ακριβώς όπως εμφανίζεται.
- Εκτίμησε confidence (0–1) για κάθε προϋπόθεση (1 = πολύ σαφής, 0 = αβέβαιη).

Κείμενο προς ανάλυση:
{text[:12000]}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a precise information extraction system for Greek legal texts. Always return valid JSON and never include explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("JSON parsing failed. Raw output:")
            print(content)
            return {"process_id": process_id, "preconditions": []}