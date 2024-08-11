import json
from datetime import datetime,timezone

from app.services.openai import create_gpt_completion
from app.models.score import EnglishScoreSheet
from app.models.assessment import Question, Questionnaire

# ----------------------------
# Questionnaire Definitions
# ----------------------------

# Added question generation prompt that makes call to chatgpt
async def generate_questionnaire() -> Questionnaire:

    prompt = """
    Generate a unique English proficiency test questionnaire. Include four types of questions: reading, writing, listening, and speaking. Each type should have one question. The format should be a JSON array with the following fields:
    - type: one of 'reading', 'writing', 'listening', 'speaking'
    - question: the question text
    - content_type: one of 'text' or 'audio'
    - text_content (for reading type): the passage content
    - audio_content (for listening type): the transcript of the audio content
    - audio_url (for listening type): the URL of the audio content

    Example:
    {
        questions:[
            {
                "type": "reading",
                "question": "What is the main idea of the passage?",
                "content_type": "text",
                "text_content": "The passage content goes here..."
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
    }
    """

    result = await create_gpt_completion(prompt)
    questionnaire_data = json.loads(result)

    return Questionnaire(questions=[Question(**question) for question in questionnaire_data['questions']])



# ----------------------------
# Score Sheet Definitions
# ----------------------------

# Prompt for generating criteria for scoring the questionnaire
async def generate_score_sheet(questionnaire: Questionnaire, user_id:str ) -> EnglishScoreSheet:

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
    and don't add the word "json" at the beginning and don't add comments the result need to be pure JSON
    """

    prompt = f"{marking_criteria}\n\n{questionnaire.model_dump_json()}"

    response = await create_gpt_completion(prompt)

    score_data = json.loads(response)

    score_data['user_id'] = user_id
    return EnglishScoreSheet.model_validate(score_data)
