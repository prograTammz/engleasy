import { Button } from "@/components/ui/button";
import { AudioVisualizer, LiveAudioVisualizer } from "react-audio-visualize";
import React, { useRef, useState } from "react";

interface RecordButtonProps {
  isRecording: boolean;
  handleRecording: () => void;
}

export const VoiceRecorder: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  //These values SHOULD NOT cause a re-render, useref is a must
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);

  const startRecording = async () => {
    //Asks for permission to get the user data
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);
    //Push new audio chunks when it's recorded
    mediaRecorder.current.ondataavailable = (event) => {
      audioChunks.current.push(event.data);
    };
    //Create a blob after recording is finished from the audio chunks
    mediaRecorder.current.onstop = () => {
      setAudioBlob(new Blob(audioChunks.current));
    };
    //Starts recording
    mediaRecorder.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    //Stops the recording
    mediaRecorder.current?.stop();
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
    <div className="bg-muted rounded-lg p-4 flex flex-col justify-center items-center">
      <div className="h-16">
        {isRecording && mediaRecorder.current && (
          <LiveAudioVisualizer
            mediaRecorder={mediaRecorder.current}
            width={320}
            height={64}
            barWidth={2}
            gap={2}
            barColor={"rgb(239, 68, 68)"}
          />
        )}
        {!isRecording && audioBlob && (
          <AudioVisualizer
            blob={audioBlob}
            width={320}
            height={64}
            barWidth={2}
            gap={2}
            barColor={"rgb(239, 68, 68)"}
          />
        )}
      </div>
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
