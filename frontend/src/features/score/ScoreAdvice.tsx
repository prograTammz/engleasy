import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Advices, CEFR } from "@/models/score";

type ScoreAdviceProps = {
  skill_level: CEFR;
};

export const ScoreAdvice: React.FC<ScoreAdviceProps> = ({ skill_level }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>How to improve?</CardTitle>
        <CardDescription>
          Follow these advices to pratice and improve your English level!
        </CardDescription>
      </CardHeader>
      <CardContent>{Advices[skill_level]}</CardContent>
    </Card>
  );
};
