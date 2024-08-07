import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { ChatMessage } from "@/models/chat";

import { EnglishScoreSheet } from "@/models/score";

import React from "react";
import { Label, Pie, PieChart } from "recharts";
import { BaseBubble } from "./BaseBubble";

type SheetBubbleProps = {
  score_sheet: EnglishScoreSheet;
  chatMessage: ChatMessage;
};

const chartConfig = {
  score: {
    label: "Score",
  },
  writing: {
    label: "Writing",
    color: "hsl(var(--chart-1))",
  },
  speaking: {
    label: "Speaking",
    color: "hsl(var(--chart-2))",
  },
  reading: {
    label: "Reading",
    color: "hsl(var(--chart-3))",
  },
  listening: {
    label: "Listening",
    color: "hsl(var(--chart-4))",
  },
} as ChartConfig;

export const SheetBubble: React.FC<SheetBubbleProps> = ({
  score_sheet,
  chatMessage,
}) => {
  const chartData = [
    {
      skill: "writing",
      score: score_sheet.writing.total,
      fill: "var(--color-writing)",
    },
    {
      skill: "speaking",
      score: score_sheet.speaking.total,
      fill: "var(--color-speaking)",
    },
    {
      skill: "reading",
      score: score_sheet.reading.total,
      fill: "var(--color-reading)",
    },
    {
      skill: "listening",
      score: score_sheet.listening.total,
      fill: "var(--color-listening)",
    },
  ];

  return (
    <BaseBubble chatMessage={chatMessage}>
      <div className="mx-auto aspect-square w-[250px]">
        <span className="inline-block font-bold">Your score is: </span>
        <span className="inline-block text-muted-foreground">
          Go to score page to see details about your score!
        </span>
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
                          {score_sheet.overall_score.toLocaleString()}
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
      </div>
    </BaseBubble>
  );
};
