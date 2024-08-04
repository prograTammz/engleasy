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
  test_date: string;
  writing: WritingScore;
  speaking: SpeakingScore;
  reading: ReadingScore;
  listening: ListeningScore;
  overall_score: number;
}
