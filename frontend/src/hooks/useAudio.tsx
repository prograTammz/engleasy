import { useState, useEffect } from "react";

const useAudio = (url: string) => {
  const [audio, setAudio] = useState<HTMLAudioElement>();
  const [playing, setPlaying] = useState(false);
  const [blob, setBlob] = useState<Blob>();

  const toggle = () => setPlaying(!playing);

  useEffect(() => {
    const fetchAudio = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const audioBlob = await response.blob();
        setBlob(audioBlob);
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        setAudio(audio);
      } catch (error) {
        console.error("Error fetching audio:", error);
      }
    };

    fetchAudio();
  }, [url]);

  useEffect(() => {
    if (audio) {
      playing ? audio.play() : audio.pause();
    }
  }, [playing, audio]);

  useEffect(() => {
    if (audio) {
      const handleEnd = () => setPlaying(false);
      audio.addEventListener("ended", handleEnd);

      return () => {
        audio.removeEventListener("ended", handleEnd);
      };
    }
  }, [audio]);

  return { blob, audio, playing, toggle };
};

export default useAudio;
