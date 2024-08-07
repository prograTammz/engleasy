import { ChatMessage } from "@/models/chat";
import { BaseBubble } from "./BaseBubble";
import { AudioVisualizer } from "react-audio-visualize";
import { useEffect, useRef, useState } from "react";
import useAudio from "@/hooks/useAudio";
import { Button } from "@/components/ui/button";

type AudioBubbleProps = {
  chatMessage: ChatMessage;
};

export const AudioBubble: React.FC<AudioBubbleProps> = ({ chatMessage }) => {
  //   const [audioBlob, setAudioBlob] = useState<Blob>();
  const { blob, audio, playing, toggle } = useAudio(chatMessage.content);
  const visualizerRef = useRef<HTMLCanvasElement>(null);

  //   useEffect(() => {
  //     const urlToBlob = async () => {
  //       try {
  //         // Fetch the MP3 file
  //         const response = await fetch(chatMessage.content, { mode: "no-cors" });

  //         // Check if the response is okay
  //         if (!response.ok) {
  //           throw new Error(`HTTP error! Status: ${response.status}`);
  //         }
  //         console.log(audioBlob);
  //         setAudioBlob(await response.blob());
  //       } catch (error: unknown) {
  //         console.error("Error fetching MP3:", error);
  //       }
  //     };

  //     urlToBlob();
  //   }, [blob]);

  const handleAudio = () => {
    toggle();
  };

  return (
    <BaseBubble chatMessage={chatMessage}>
      <>
        {blob && (
          <AudioVisualizer
            ref={visualizerRef}
            blob={blob}
            width={300}
            height={50}
            barWidth={1}
            gap={0}
            barColor={"#f76565"}
          />
        )}
        <Button onClick={() => handleAudio()}>
          {playing ? "Stop" : "Start"}
        </Button>
      </>
    </BaseBubble>
  );
};
