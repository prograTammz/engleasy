import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
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
    <div className="flex flex-wrap bg-muted mx-8 my-4 justify-center">
      <div className="flex flex-col gap-2 items-center w-full lg:w-1/5 mb-4 lg:mb-0">
        <span className="uppercase font-bold">Your English Score</span>
        <span className="font-bold text-5xl inline-block bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-transparent bg-clip-text">
          {overall_score}
        </span>
        <p className="flex font-bold text-lg mb-2 gap-2">
          Your level is
          <span className="text-purple-600 dark:text-purple-500">
            {cefr_level}
          </span>
        </p>
      </div>
      <Separator orientation="vertical" />
      <div className="flex items-center w-full lg:w-3/5">
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
