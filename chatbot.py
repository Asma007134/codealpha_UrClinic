import json
import re
from pathlib import Path
from difflib import get_close_matches

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp import preprocess


class UrClinicBot:

    def __init__(self):
        file_path = Path(__file__).parent / "faq_data.json"

        with open(file_path, "r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        # ---------------------------------------------------------
        # Build searchable knowledge base
        # ---------------------------------------------------------

        self.documents = []

        for faq in self.faqs:

            question = faq.get("question", "")
            examples = faq.get("examples", [])
            keywords = faq.get("keywords", [])
            category = faq.get("category", "")
            intent = faq.get("intent", "")

            # Repeat important fields to give them more TF-IDF weight
            document = " ".join([
                question,
                question,
                " ".join(examples),
                " ".join(keywords),
                category,
                intent
            ])

            self.documents.append(preprocess(document))

        # ---------------------------------------------------------
        # WORD TF-IDF
        # ---------------------------------------------------------

        self.word_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )

        self.word_vectors = self.word_vectorizer.fit_transform(
            self.documents
        )

        # ---------------------------------------------------------
        # CHARACTER TF-IDF
        # Helps with spelling mistakes like:
        # rshes -> rashes
        # medcine -> medicine
        # assisitant -> assistant
        # ---------------------------------------------------------

        self.char_vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
            min_df=1
        )

        self.char_vectors = self.char_vectorizer.fit_transform(
            self.documents
        )

        # ---------------------------------------------------------
        # Build vocabulary for lightweight spelling correction
        # ---------------------------------------------------------

        self.vocabulary = set()

        for faq in self.faqs:

            text_parts = [
                faq.get("question", ""),
                faq.get("category", ""),
                faq.get("intent", "")
            ]

            text_parts.extend(faq.get("examples", []))
            text_parts.extend(faq.get("keywords", []))

            for text in text_parts:
                tokens = re.findall(r"[a-zA-Z]+", text.lower())

                for token in tokens:
                    if len(token) >= 3:
                        self.vocabulary.add(token)

        # Common conversational words should not be corrected
        self.common_words = {
            "what",
            "where",
            "when",
            "why",
            "who",
            "which",
            "how",
            "can",
            "could",
            "should",
            "would",
            "please",
            "tell",
            "me",
            "my",
            "i",
            "have",
            "has",
            "is",
            "are",
            "am",
            "do",
            "does",
            "the",
            "for",
            "with",
            "and",
            "or",
            "to",
            "a",
            "an"
        }

    # =============================================================
    # SPELLING NORMALIZATION
    # =============================================================

    def normalize_spelling(self, text):

        tokens = re.findall(r"[a-zA-Z]+", text.lower())

        corrected = []

        for token in tokens:

            if (
                len(token) >= 4
                and token not in self.common_words
                and token not in self.vocabulary
            ):

                matches = get_close_matches(
                    token,
                    self.vocabulary,
                    n=1,
                    cutoff=0.78
                )

                if matches:
                    token = matches[0]

            corrected.append(token)

        return " ".join(corrected)

    # =============================================================
    # GREETING DETECTION
    # =============================================================

    def is_greeting(self, text):

        text = text.lower().strip()

        greetings = {
            "hi",
            "hello",
            "hey",
            "salam",
            "assalam o alaikum",
            "assalamu alaikum",
            "good morning",
            "good afternoon",
            "good evening"
        }

        if text in greetings:
            return True

        # Short greeting sentences
        if len(text.split()) <= 3:

            for greeting in greetings:
                if greeting in text:
                    return True

        return False

    # =============================================================
    # THANKS
    # =============================================================

    def is_thanks(self, text):

        text = text.lower()

        words = [
            "thanks",
            "thank you",
            "thx",
            "thankyou"
        ]

        return any(word in text for word in words)

    # =============================================================
    # EMERGENCY DETECTION
    # Emergency intent always gets priority.
    # =============================================================

    def detect_emergency(self, text):

        emergency_phrases = [

            "cannot breathe",
            "can't breathe",
            "difficulty breathing",
            "severe breathing",
            "shortness of breath",
            "severe chest pain",
            "chest pain",
            "unconscious",
            "passed out",
            "fainted",
            "stroke",
            "face drooping",
            "one sided weakness",
            "severe bleeding",
            "heavy bleeding",
            "seizure",
            "severe allergic reaction",
            "swelling of throat",
            "swelling of tongue",
            "rapidly worsening"
        ]

        return any(
            phrase in text.lower()
            for phrase in emergency_phrases
        )

    # =============================================================
    # HIGH-CONFIDENCE INTENT DETECTION
    # =============================================================

    def keyword_intent(self, text):

        text = text.lower()

        # ---------------------------------------------------------
        # Emergency
        # ---------------------------------------------------------

        if self.detect_emergency(text):

            emergency_terms = [
                "cannot breathe",
                "can't breathe",
                "difficulty breathing",
                "severe breathing",
                "shortness of breath",
                "severe chest pain",
                "chest pain",
                "unconscious",
                "stroke",
                "face drooping",
                "severe bleeding",
                "seizure",
                "severe allergic reaction"
            ]

            if any(term in text for term in emergency_terms):

                for index, faq in enumerate(self.faqs):

                    if faq.get("intent") in {
                        "emergency",
                        "breathing_problem",
                        "chest_pain",
                        "stroke",
                        "allergy"
                    }:

                        if faq.get("intent") == "breathing_problem" and (
                            "breath" in text or
                            "breathing" in text
                        ):
                            return index

                        if faq.get("intent") == "chest_pain" and "chest" in text:
                            return index

                        if faq.get("intent") == "stroke" and "stroke" in text:
                            return index

                        if faq.get("intent") == "allergy" and "allerg" in text:
                            return index

                return self.find_intent("emergency")

        # ---------------------------------------------------------
        # Medication
        # ---------------------------------------------------------

        medication_terms = [
            "medicine",
            "medication",
            "prescription",
            "drug",
            "tablet",
            "dose",
            "pharmacy",
            "medicne",
            "medicene",
            "assisitant",
            "assistant"
        ]

        if any(term in text for term in medication_terms):

            # If user is asking about medication
            index = self.find_intent("medicine_information")

            if index is not None:
                return index

        # ---------------------------------------------------------
        # Rash / skin
        # ---------------------------------------------------------

        skin_terms = [
            "rash",
            "rashes",
            "skin",
            "itch",
            "itching",
            "itchy",
            "acne",
            "dermatology",
            "dermatologist"
        ]

        if any(term in text for term in skin_terms):

            # If asking which doctor/department
            if any(
                word in text
                for word in [
                    "doctor",
                    "department",
                    "consult",
                    "whom",
                    "who",
                    "specialist"
                ]
            ):

                index = self.find_intent("rash")

                if index is not None:
                    return index

            index = self.find_intent("rash")

            if index is not None:
                return index

        # ---------------------------------------------------------
        # Cough
        # ---------------------------------------------------------

        cough_terms = [
            "cough",
            "coughing",
            "coughs",
            "phlegm",
            "respiratory"
        ]

        if any(term in text for term in cough_terms):

            index = self.find_intent("cough")

            if index is not None:
                return index

        # ---------------------------------------------------------
        # Fever
        # ---------------------------------------------------------

        fever_terms = [
            "fever",
            "temperature",
            "high temperature",
            "febrile"
        ]

        if any(term in text for term in fever_terms):

            index = self.find_intent("fever")

            if index is not None:
                return index

        # ---------------------------------------------------------
        # Headache
        # ---------------------------------------------------------

        if any(
            term in text
            for term in [
                "headache",
                "head pain",
                "migraine"
            ]
        ):

            return self.find_intent("headache")

        # ---------------------------------------------------------
        # Stomach
        # ---------------------------------------------------------

        if any(
            term in text
            for term in [
                "stomach",
                "abdomen",
                "abdominal",
                "belly"
            ]
        ):

            return self.find_intent("stomach_pain")

        # ---------------------------------------------------------
        # Back pain
        # ---------------------------------------------------------

        if any(
            term in text
            for term in [
                "back pain",
                "my back",
                "lower back"
            ]
        ):

            return self.find_intent("back_pain")

        # ---------------------------------------------------------
        # Joint / bone
        # ---------------------------------------------------------

        if any(
            term in text
            for term in [
                "joint",
                "knee",
                "bone",
                "arthritis",
                "fracture"
            ]
        ):

            return self.find_intent("joint_pain")

        return None

    # =============================================================
    # FIND INTENT
    # =============================================================

    def find_intent(self, intent_name):

        for index, faq in enumerate(self.faqs):

            if faq.get("intent") == intent_name:
                return index

        return None

    # =============================================================
    # MAIN RESPONSE ENGINE
    # =============================================================

    def get_response(self, user_question):

        if not user_question:
            return "Please type a question so I can help you. 😊"

        original_text = user_question.strip()

        # ---------------------------------------------------------
        # Greetings
        # ---------------------------------------------------------

        if self.is_greeting(original_text):

            return (
                "Hello! 👋 I'm UrClinic, your AI hospital "
                "information assistant.\n\n"
                "You can ask me about symptoms, departments, "
                "medical tests, medicines, appointments, "
                "emergency warning signs, and general health "
                "information."
            )

        # ---------------------------------------------------------
        # Thanks
        # ---------------------------------------------------------

        if self.is_thanks(original_text):

            return (
                "You're welcome! 😊 "
                "Feel free to ask another hospital or "
                "health-information question."
            )

        # ---------------------------------------------------------
        # Normalize spelling
        # ---------------------------------------------------------

        normalized = self.normalize_spelling(original_text)

        # ---------------------------------------------------------
        # NLP preprocessing
        # ---------------------------------------------------------

        cleaned_question = preprocess(normalized)

        if not cleaned_question:

            return (
                "I couldn't understand that message. "
                "Please try asking your question in another way."
            )

        # ---------------------------------------------------------
        # High-confidence keyword/intent matching
        # ---------------------------------------------------------

        keyword_match = self.keyword_intent(cleaned_question)

        if keyword_match is not None:

            return self.faqs[keyword_match]["answer"]

        # ---------------------------------------------------------
        # WORD TF-IDF SIMILARITY
        # ---------------------------------------------------------

        user_word_vector = self.word_vectorizer.transform(
            [cleaned_question]
        )

        word_scores = cosine_similarity(
            user_word_vector,
            self.word_vectors
        )[0]

        # ---------------------------------------------------------
        # CHARACTER TF-IDF SIMILARITY
        # ---------------------------------------------------------

        user_char_vector = self.char_vectorizer.transform(
            [cleaned_question]
        )

        char_scores = cosine_similarity(
            user_char_vector,
            self.char_vectors
        )[0]

        # ---------------------------------------------------------
        # Combined similarity
        #
        # Word similarity = semantic wording
        # Character similarity = spelling variation
        # ---------------------------------------------------------

        combined_scores = (
            0.70 * word_scores +
            0.30 * char_scores
        )

        best_match_index = combined_scores.argmax()
        best_score = combined_scores[best_match_index]

        # ---------------------------------------------------------
        # Confidence threshold
        # ---------------------------------------------------------

        if best_score < 0.16:

            return (
                "I'm sorry, I couldn't find a reliable answer "
                "to that question in my current hospital "
                "knowledge base. 😕\n\n"
                "Try asking about:\n"
                "• Symptoms\n"
                "• Hospital departments\n"
                "• Medical tests\n"
                "• Medicines\n"
                "• Appointments\n"
                "• Emergency warning signs\n"
                "• General health information"
            )

        return self.faqs[best_match_index]["answer"]