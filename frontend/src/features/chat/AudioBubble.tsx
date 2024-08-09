import { ChatMessage } from "@/models/chat";
import { BaseBubble } from "./BaseBubble";
import { AudioVisualizer } from "react-audio-visualize";
import { useRef } from "react";
import useAudio from "@/hooks/useAudio";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Pause, Play } from "lucide-react";

type AudioBubbleProps = {
  chatMessage: ChatMessage;
};

export const AudioBubble: React.FC<AudioBubbleProps> = ({ chatMessage }) => {
  const { blob, playing, toggle, currentTime, duration } = useAudio(
    chatMessage.content
  );
  const visualizerRef = useRef<HTMLCanvasElement>(null);

  const handleAudio = () => {
    toggle();
  };

  return (
    <BaseBubble chatMessage={chatMessage}>
      <>
        <div className="flex gap-4 items-center">
          <div className="flex flex-col">
            {blob && (
              <AudioVisualizer
                ref={visualizerRef}
                blob={blob}
                width={200}
                height={50}
                barWidth={1}
                gap={0}
                barColor={"#f76565"}
              />
            )}
            <Progress value={(currentTime / duration) * 100} />
          </div>
          <Button
            onClick={() => handleAudio()}
            variant="outline"
            size="sm"
            className="h-12 w-12 rounded-full"
          >
            {playing ? <Pause /> : <Play />}
          </Button>
        </div>
      </>
    </BaseBubble>
  );
};
