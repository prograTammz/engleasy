import React from "react";

interface PhaseBubbleProps {
  phaseName: string;
}

export const PhaseBubble: React.FC<PhaseBubbleProps> = ({ phaseName }) => {
  return <div>{phaseName}</div>;
};
