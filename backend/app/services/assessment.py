import json

from app.services.openai import create_gpt_completion

def generate_questionnaire():
    pass




def generate_score_sheet(questionnaire_json: str):

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

    return json.loads(create_gpt_completion(prompt))
