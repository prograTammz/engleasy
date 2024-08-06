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
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
} from "recharts";

const chartData = [
  { skill: "Speaking", score: 35 },
  { skill: "Listening", score: 30 },
  { skill: "Writing", score: 45 },
  { skill: "Reading", score: 55 },
];

const chartConfig = {
  score: {
    label: "Score",
    color: "hsl(var(--chart-1))",
  },
} satisfies ChartConfig;

export const ScoreOverallChart: React.FC = () => {
  return (
    <Card className="w-full">
      <CardHeader className="items-center pb-4">
        <CardTitle>Your Skills</CardTitle>
        <CardDescription>
          Showing the progress if each Skill score
        </CardDescription>
      </CardHeader>
      <CardContent className="p2-">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px] w-[300px]"
        >
          <RadarChart data={chartData} width={250} height={250}>
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent indicator="line" labelKey="skill" />
              }
            />
            <PolarAngleAxis dataKey="skill" domain={[0, 80]} />
            <PolarRadiusAxis
              angle={60}
              domain={[0, 80]}
              stroke="hsla(var(--foreground))"
              orientation="middle"
              axisLine={false}
            />
            <PolarGrid gridType="circle" />
            <Radar
              dataKey="score"
              fill="var(--color-score)"
              fillOpacity={0.6}
              dot={{
                r: 4,
                fillOpacity: 1,
              }}
            />
          </RadarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
};
