export interface WritingScore {
  task_achievement: number;
  coherence_and_cohesion: number;
  lexical_resource: number;
  grammatical_range_and_accuracy: number;
  total: number;
}

export interface SpeakingScore {
  fluency_and_coherence: number;
  pronunciation: number;
  lexical_resource: number;
  grammatical_range_and_accuracy: number;
  total: number;
}

export interface ReadingScore {
  understanding_main_ideas: number;
  understanding_details: number;
  inference: number;
  lexical_resource: number;
  total: number;
}

export interface ListeningScore {
  understanding_main_ideas: number;
  understanding_details: number;
  inference: number;
  lexical_resource: number;
  total: number;
}

export interface EnglishScoreSheet {
  user_id: string;
  test_date: Date;
  writing: WritingScore;
  speaking: SpeakingScore;
  reading: ReadingScore;
  listening: ListeningScore;
  overall_score: number;
  cefr_level: CEFR;
}

export interface ScoresResponse {}

export enum CEFR {
  A1 = "A1",
  A2 = "A2",
  B1 = "B1",
  B2 = "B2",
  C1 = "C1",
  C2 = "C2",
}

export enum CEFRTitle {
  A1 = "Beginner",
  A2 = "Elementary",
  B1 = "Intermediate",
  B2 = "Upper-Intermediate",
  C1 = "Advanced",
  C2 = "Proficient",
}

export const Advices = {
  A1: "To improve your English at the A1 level, focus on building a strong foundation of basic vocabulary and simple sentence structures. Practice everyday conversations by greeting people, introducing yourself, and talking about common topics like weather and daily routines. Use flashcards and language apps to reinforce your vocabulary. Engage with simple English books and children's TV shows to improve your listening skills. Join language exchange groups where you can practice speaking with native speakers who are patient and supportive.",
  A2: "At the A2 level, start expanding your vocabulary related to more specific topics like hobbies, shopping, and travel. Practice forming longer sentences and questions. Listen to short, clear dialogues and try to understand the main points. Read simple texts, such as short stories and news articles aimed at English learners. Write short paragraphs about your day, your plans, or your opinions on familiar topics. Engage in conversations with others about your interests, and don't be afraid to make mistakes—it's part of the learning process.",
  B1: "To advance from B1, immerse yourself in English as much as possible. Listen to podcasts, watch movies, and read books on topics that interest you. Focus on understanding the main ideas and details. Practice writing essays and letters, paying attention to grammar and coherence. Engage in discussions and debates to improve your speaking fluency and confidence. Try to use new vocabulary and complex sentence structures. Join a study group or take an online course to receive structured guidance and feedback.",
  B2: "At the B2 level, aim to refine your language skills and expand your vocabulary further. Read a variety of texts, including newspapers, novels, and academic articles. Watch documentaries and TED talks to expose yourself to different accents and advanced topics. Practice writing detailed essays and reports, focusing on argumentation and clarity. Participate in discussions and presentations to enhance your speaking skills. Seek feedback from teachers or language partners to identify areas for improvement and work on them systematically.",
  C1: "For C1 learners, the goal is to achieve greater accuracy and subtlety in your language use. Read complex texts and analyze their structure and vocabulary. Watch and listen to advanced content, such as news broadcasts and university lectures, to improve your comprehension of nuanced information. Write in-depth essays and research papers, paying close attention to style and coherence. Engage in high-level discussions and debates, focusing on expressing your ideas clearly and persuasively. Consider taking specialized language courses or certifications to challenge yourself further.",
  C2: "At the C2 level, focus on mastering the nuances of the language. Read widely across different genres and fields to enrich your vocabulary and understanding of idiomatic expressions. Engage with sophisticated media, such as classic literature, scientific journals, and philosophical debates. Write extensively, aiming for precision and elegance in your language. Participate in professional or academic discussions and presentations, refining your ability to argue and persuade effectively. Continually seek feedback and strive for excellence in all aspects of your language use, maintaining a high level of practice and exposure to English.",
};

export const exampleSheet: EnglishScoreSheet = {
  user_id: "sfdnwednwnw",
  test_date: new Date(),
  writing: {
    task_achievement: 20,
    coherence_and_cohesion: 30,
    lexical_resource: 40,
    grammatical_range_and_accuracy: 50,
    total: 140,
  },
  speaking: {
    fluency_and_coherence: 20,
    pronunciation: 30,
    lexical_resource: 40,
    grammatical_range_and_accuracy: 50,
    total: 140,
  },
  reading: {
    understanding_main_ideas: 10,
    understanding_details: 15,
    inference: 16,
    lexical_resource: 9,
    total: 50,
  },
  listening: {
    understanding_main_ideas: 10,
    understanding_details: 15,
    inference: 16,
    lexical_resource: 9,
    total: 50,
  },
  overall_score: 250,
  cefr_level: CEFR.C1,
};
