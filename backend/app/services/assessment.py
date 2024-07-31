import json
import datetime

from app.services.openai import create_gpt_completion
from app.models.score import (EnglishScoreSheet, WritingScores, SpeakingScores, ReadingScores, ListeningScores)
from app.models.assessment import (Question, Questionnaire)

# ----------------------------
# Questionnaire Definitions
# ----------------------------

# Added question generation prompt that makes call to chatgpt
def generate_questionnaire():

    prompt = """
    Generate a unique English proficiency test questionnaire. Include four types of questions: reading, writing, listening, and speaking. Each type should have one question. The format should be a JSON array with the following fields:
    - type: one of 'reading', 'writing', 'listening', 'speaking'
    - question: the question text
    - content_type: one of 'text' or 'audio'
    - audio_content (optional): the transcript of the audio content (for listening type)
    - audio_url (optional): the URL of the audio content (for listening type)

    Example:
    [
        {
            "type": "reading",
            "question": "What is the main idea of the passage?",
            "content_type": "text"
        },
        {
            "type": "writing",
            "question": "Write an essay on climate change.",
            "content_type": "text"
        },
        {
            "type": "listening",
            "question": "What did the speaker say about renewable energy?",
            "content_type": "audio",
            "audio_content": "Renewable energy is crucial for sustainable development.",
            "audio_url": "http://example.com/audio/renewable_energy.mp3"
        },
        {
            "type": "speaking",
            "question": "Describe your favorite hobby.",
            "content_type": "text"
        }
    ]
    """

    questionnaire_data = json.loads(create_gpt_completion(prompt))
    return Questionnaire(tests=[Question(**test) for test in questionnaire_data])



# ----------------------------
# Score Sheet Definitions
# ----------------------------

# Prompt for generating criteria for scoring the questionnaire
def generate_score_sheet(questionnaire_json: str, user_id:str ) -> str:

    marking_criteria = """
    You are a scoring assistant for language proficiency tests. Score each answer based on the following criteria:

    - Writing:
      - Task Achievement: 0-20
      - Coherence and Cohesion: 0-20
      - Lexical Resource: 0-20
      - Grammatical Range and Accuracy: 0-20

    - Speaking:
      - Fluency and Coherence: 0-20
      - Pronunciation: 0-20
      - Lexical Resource: 0-20
      - Grammatical Range and Accuracy: 0-20

    - Reading:
      - Understanding Main Ideas: 0-20
      - Understanding Details: 0-20
      - Inference: 0-20
      - Lexical Resource: 0-20

    - Listening:
      - Understanding Main Ideas: 0-20
      - Understanding Details: 0-20
      - Inference: 0-20
      - Lexical Resource: 0-20

    Return the scores in the following JSON format:
    {
        "user_id": "user-id",
        "test_date": "ISO-8601-date",
        "writing": {
            "task_achievement": score,
            "coherence_and_cohesion": score,
            "lexical_resource": score,
            "grammatical_range_and_accuracy": score,
            "total": score
        },
        "speaking": {
            "fluency_and_coherence": score,
            "pronunciation": score,
            "lexical_resource": score,
            "grammatical_range_and_accuracy": score,
            "total": score
        },
        "reading": {
            "understanding_main_ideas": score,
            "understanding_details": score,
            "inference": score,
            "lexical_resource": score,
            "total": score
        },
        "listening": {
            "understanding_main_ideas": score,
            "understanding_details": score,
            "inference": score,
            "lexical_resource": score,
            "total": score
        },
        "overall_score": score,
        "cefr_level": "A1" | "A2" | "B1" | "B2" | "C1" | "C2"
    }
    """

    prompt = f"{marking_criteria}\n\n{questionnaire_json}"

    return get_score_sheet_object(create_gpt_completion(prompt), user_id)

# Takes the score sheet json after it gets generated and parsed from chatGPT with user_id
def get_score_sheet_object(score_sheet_json: str, user_id: str) -> str:
    return EnglishScoreSheet(
        user_id=user_id,  # Replace with actual user ID
        test_date=datetime.utcnow(),
        writing=WritingScores(
            task_achievement=score_sheet_json['writing']['task_achievement'],
            coherence_and_cohesion=score_sheet_json['writing']['coherence_and_cohesion'],
            lexical_resource=score_sheet_json['writing']['lexical_resource'],
            grammatical_range_and_accuracy=score_sheet_json['writing']['grammatical_range_and_accuracy'],
            total=score_sheet_json['writing']['total']
        ),
        speaking=SpeakingScores(
            fluency_and_coherence=score_sheet_json['speaking']['fluency_and_coherence'],
            pronunciation=score_sheet_json['speaking']['pronunciation'],
            lexical_resource=score_sheet_json['speaking']['lexical_resource'],
            grammatical_range_and_accuracy=score_sheet_json['speaking']['grammatical_range_and_accuracy'],
            total=score_sheet_json['speaking']['total']
        ),
        reading=ReadingScores(
            understanding_main_ideas=score_sheet_json['reading']['understanding_main_ideas'],
            understanding_details=score_sheet_json['reading']['understanding_details'],
            inference=score_sheet_json['reading']['inference'],
            lexical_resource=score_sheet_json['reading']['lexical_resource'],
            total=score_sheet_json['reading']['total']
        ),
        listening=ListeningScores(
            understanding_main_ideas=score_sheet_json['listening']['understanding_main_ideas'],
            understanding_details=score_sheet_json['listening']['understanding_details'],
            inference=score_sheet_json['listening']['inference'],
            lexical_resource=score_sheet_json['listening']['lexical_resource'],
            total=score_sheet_json['listening']['total']
        ),
        overall_score=score_sheet_json['overall_score'],
        cefr_level=score_sheet_json['cefr_level']
    )