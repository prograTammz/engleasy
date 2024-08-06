import { Progress } from "@/components/ui/progress";
import { CEFR } from "@/models/score";

type ScoreOverviewProps = {
  cefr_level: CEFR;
  overall_score: number;
};

type ScoreProgressProps = {
  cefr_level: CEFR;
  overall_score: number;
};

export const ScoreOverview: React.FC<ScoreOverviewProps> = ({
  cefr_level,
  overall_score,
}) => {
  return (
    <div className="bg-muted mx-8 my-4">
      <div>
        <span>Your English Score</span>
        <span>{overall_score}</span>
        <span>{cefr_level}</span>
        <ScoreProgress overall_score={overall_score} cefr_level={cefr_level} />
      </div>
    </div>
  );
};

const ScoreProgress: React.FC<ScoreProgressProps> = ({
  overall_score,
  cefr_level,
}) => {
  return (
    <div className="flex flex-col w-full">
      <div className="flex w-full justify-between">
        {Object.values(CEFR).map((level) => (
          <span
            className={`font-bold text-lg mb-2 ${
              cefr_level == level ? "text-purple-600 dark:text-purple-500" : ""
            }`}
          >
            {level}
          </span>
        ))}
      </div>
      <Progress value={(overall_score / 320) * 100} />
    </div>
  );
};
