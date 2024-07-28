import { Separator } from "@/components/ui/separator";
import React from "react";

interface PhaseBubbleProps {
  phaseName: string;
  phaseNumber: number;
}

export const PhaseBubble: React.FC<PhaseBubbleProps> = ({
  phaseName,
  phaseNumber,
}) => {
  return (
    <div className="flex flex-col">
      <Separator />
      <div className="flex w-full justify-center gap-2 font-extrabold my-4">
        <span>
          Phase <span className="text-purple-700">{phaseNumber}</span>:
        </span>
        <span className="text-purple-700 uppercase">{phaseName}</span>
      </div>
      <Separator />
    </div>
  );
};
