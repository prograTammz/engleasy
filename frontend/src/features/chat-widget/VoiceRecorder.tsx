import { Button } from "@/components/ui/button";
import React, { useState } from "react";

interface RecordButtonProps {
  isRecording: boolean;
  handleRecording: () => void;
}

export const VoiceRecorder: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  const handleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div>
      <RecordButton
        isRecording={isRecording}
        handleRecording={handleRecording}
      />
    </div>
  );
};

const RecordButton: React.FC<RecordButtonProps> = ({
  isRecording,
  handleRecording,
}) => {
  return (
    <Button
      onClick={() => handleRecording()}
      size="lg"
      className={`transition-all border-4 p-1 ${
        isRecording && "animate-pulse border-0 p-0"
      } rounded-full border-red-500  bg-transparent h-12 w-12`}
    >
      <div className="bg-red-500 w-full h-full rounded-full"></div>
    </Button>
  );
};
