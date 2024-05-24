import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from enchant.checker import SpellChecker
from nltk.stem import WordNetLemmatizer
from language_tool_python import LanguageTool
import nltk
nltk.download('stopwords')
class Spell_Checker():
# Download NLTK data (only required once)
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

    # Initialize spell checker
    spell_checker = SpellChecker("en_US")
    @staticmethod
    def suggest_corrections(text):
        # Tokenize the text
        tokens = word_tokenize(text)
        
        # Get part-of-speech tags
        tagged_tokens = pos_tag(tokens)
        
        # Filter out stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [token for token, tag in tagged_tokens if token.lower() not in stop_words]
        
        # Spell check and suggest corrections
        suggestions = []
        for token in filtered_tokens:
            if not wordnet.synsets(token):
                Spell_Checker.spell_checker.set_text(token)
                for error in Spell_Checker.spell_checker:
                    suggestions.extend(error.suggest())
        
        return suggestions
    @staticmethod
    def get_synonyms(word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        return list(set(synonyms))
    @staticmethod
    def check_grammar(text):
        tool = LanguageTool('en-US')
        matches = tool.check(text)
        return [match.msg for match in matches]
if __name__ == "__main__":

# Example usage
    text = "Thiss is a sentence with spelng errors."
    corrections = Spell_Checker.suggest_corrections(text)
    print("Spelling suggestions:", corrections)