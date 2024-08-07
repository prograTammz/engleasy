import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { WritingScore } from "@/models/score";
import { Label, Pie, PieChart } from "recharts";

type ScoreWritingProps = {
  writing_score: WritingScore;
};

const chartConfig = {
  score: {
    label: "Score",
  },
  task_achievement: {
    label: "Task Achievement",
    color: "hsl(var(--chart-1))",
  },
  coherence_and_cohesion: {
    label: "Coherence & Cohesion",
    color: "hsl(var(--chart-2))",
  },
  lexical_resource: {
    label: "Lexical Resource",
    color: "hsl(var(--chart-3))",
  },
  grammatical_range_and_accuracy: {
    label: "Grammatical range & Accuracy",
    color: "hsl(var(--chart-4))",
  },
} satisfies ChartConfig;

export const ScoreWriting: React.FC<ScoreWritingProps> = ({
  writing_score,
}) => {
  const chartData = [
    {
      skill: "task_achievement",
      score: writing_score.task_achievement,
      fill: "var(--color-task_achievement)",
    },
    {
      skill: "coherence_and_cohesion",
      score: writing_score.coherence_and_cohesion,
      fill: "var(--color-coherence_and_cohesion)",
    },
    {
      skill: "lexical_resource",
      score: writing_score.lexical_resource,
      fill: "var(--color-lexical_resource)",
    },
    {
      skill: "grammatical_range_and_accuracy",
      score: writing_score.grammatical_range_and_accuracy,
      fill: "var(--color-grammatical_range_and_accuracy)",
    },
  ];
  return (
    <div className="flex flex-wrap lg:flex-nowrap gap-4">
      {/* Score */}
      <Card className="flex flex-col shadow-md">
        <CardHeader className="items-center pb-0">
          <CardTitle>Writing Score</CardTitle>
          <CardDescription>
            Breaking down the score based on each skill
          </CardDescription>
        </CardHeader>
        <CardContent className="flex-1 pb-0">
          <ChartContainer
            config={chartConfig}
            className="mx-auto aspect-square max-h-[250px]"
          >
            <PieChart>
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent hideLabel />}
              />
              <Pie
                data={chartData}
                dataKey="score"
                nameKey="skill"
                innerRadius={60}
                strokeWidth={5}
              >
                <Label
                  content={({ viewBox }) => {
                    if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                      return (
                        <text
                          x={viewBox.cx}
                          y={viewBox.cy}
                          textAnchor="middle"
                          dominantBaseline="middle"
                        >
                          <tspan
                            x={viewBox.cx}
                            y={viewBox.cy}
                            className="fill-foreground text-3xl font-bold"
                          >
                            {writing_score.total.toLocaleString()}
                          </tspan>
                          <tspan
                            x={viewBox.cx}
                            y={(viewBox.cy || 0) + 24}
                            className="fill-muted-foreground"
                          >
                            Score
                          </tspan>
                        </text>
                      );
                    }
                  }}
                />
              </Pie>
            </PieChart>
          </ChartContainer>
        </CardContent>
      </Card>
      {/* Explanation */}
      <Card>
        <CardHeader className="items-center pb-0">
          <CardTitle>Score Explanation</CardTitle>
          <CardDescription>
            Each criterion is scored out of 20, with a total possible score of
            80 points for writing.!
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="flex flex-col gap-2 p-4">
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Task Achievement (0-20 points):
              </strong>{" "}
              How well the task requirements are met.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Coherence and Cohesion (0-20 points):
              </strong>{" "}
              The logical organization and flow of ideas.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Lexical Resource (0-20 points):
              </strong>{" "}
              The range and accuracy of vocabulary used.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Grammatical Range and Accuracy (0-20 points):
              </strong>{" "}
              The range and accuracy of grammatical structures used.
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};
