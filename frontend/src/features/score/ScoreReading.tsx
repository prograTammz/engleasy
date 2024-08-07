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
import { ReadingScore } from "@/models/score";
import { Label, Pie, PieChart } from "recharts";

type ScoreReadingProps = {
  reading_score: ReadingScore;
};

const chartConfig = {
  score: {
    label: "Score",
  },
  understanding_main_ideas: {
    label: "Understanding main ideas",
    color: "hsl(var(--chart-1))",
  },
  understanding_details: {
    label: "Understanding details",
    color: "hsl(var(--chart-2))",
  },
  inference: {
    label: "Inference",
    color: "hsl(var(--chart-3))",
  },
  lexical_resource: {
    label: "Lexical Resource",
    color: "hsl(var(--chart-4))",
  },
} as ChartConfig;

export const ScoreReading: React.FC<ScoreReadingProps> = ({
  reading_score,
}) => {
  const chartData = [
    {
      skill: "understanding_main_ideas",
      score: reading_score.understanding_main_ideas,
      fill: "var(--color-understanding_main_ideas)",
    },
    {
      skill: "understanding_details",
      score: reading_score.understanding_details,
      fill: "var(--color-understanding_details)",
    },
    {
      skill: "inference",
      score: reading_score.inference,
      fill: "var(--color-inference)",
    },
    {
      skill: "lexical_resource",
      score: reading_score.lexical_resource,
      fill: "var(--color-lexical_resource)",
    },
  ];
  return (
    <div className="flex flex-wrap lg:flex-nowrap gap-4">
      {/* Score */}
      <Card className="flex flex-col shadow-md">
        <CardHeader className="items-center pb-0">
          <CardTitle>Reading Score</CardTitle>
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
                            {reading_score.total.toLocaleString()}
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
                Understanding Main Ideas (0-20 points):
              </strong>{" "}
              How well the main ideas are understood.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Understanding Details (0-20 points):
              </strong>{" "}
              How well specific details are understood.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Inference (0-20 points):
              </strong>{" "}
              The ability to make logical inferences from the text.
            </li>
            <li>
              <strong className="text-purple-500 dark:text-purple-300">
                Lexical Resource (0-20 points):
              </strong>{" "}
              Understanding of vocabulary used in the reading material.
            </li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};
