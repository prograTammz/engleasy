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
import { SpeakingScore } from "@/models/score";
import { Label, Pie, PieChart } from "recharts";

type ScoreSpeakingProps = {
  speaking_score: SpeakingScore;
};

const chartConfig = {
  score: {
    label: "Score",
  },
  fluency_and_coherence: {
    label: "Fluency & Coherence",
    color: "hsl(var(--chart-1))",
  },
  pronunciation: {
    label: "Pronunciation",
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

export const ScoreSpeaking: React.FC<ScoreSpeakingProps> = ({
  speaking_score,
}) => {
  const chartData = [
    {
      skill: "fluency_and_coherence",
      score: speaking_score.fluency_and_coherence,
      fill: "var(--color-fluency_and_coherence)",
    },
    {
      skill: "pronunciation",
      score: speaking_score.pronunciation,
      fill: "var(--color-pronunciation)",
    },
    {
      skill: "lexical_resource",
      score: speaking_score.lexical_resource,
      fill: "var(--color-lexical_resource)",
    },
    {
      skill: "grammatical_range_and_accuracy",
      score: speaking_score.grammatical_range_and_accuracy,
      fill: "var(--color-grammatical_range_and_accuracy)",
    },
  ];
  return (
    <div className="flex flex-wrap lg:flex-nowrap gap-4">
      {/* Score */}
      <Card className="flex flex-col shadow-md">
        <CardHeader className="items-center pb-0">
          <CardTitle>Speaking Score</CardTitle>
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
                            {speaking_score.total.toLocaleString()}
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
                Fluency and Coherence (0-20 points):
              </strong>{" "}
              The smoothness and logical flow of speech.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Pronunciation (0-20 points):
              </strong>{" "}
              The clarity and accuracy of pronunciation.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Lexical Resource (0-20 points):
              </strong>{" "}
              The range and appropriateness of vocabulary used.
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
