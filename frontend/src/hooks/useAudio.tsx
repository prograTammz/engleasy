import { useState, useEffect } from "react";

const useAudio = (url: string) => {
  const [audio, setAudio] = useState<HTMLAudioElement>();
  const [playing, setPlaying] = useState<boolean>(false);
  const [blob, setBlob] = useState<Blob>();
  const [currentTime, setCurrentTime] = useState<number>(0);
  const [duration, setDuration] = useState<number>(0);

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

        const initalizeAudio = () => {
          if (audio.duration === Infinity || isNaN(Number(audio.duration))) {
            audio.currentTime = 1e101;
            audio.addEventListener("timeupdate", updateDuration);
          }
        };
        audio.addEventListener("loadedmetadata", initalizeAudio);

        const updateDuration = (event: Event) => {
          const target = event.target as HTMLAudioElement;
          target.currentTime = 0;
          target.removeEventListener("timeupdate", updateDuration);
          setDuration(audio.duration);
        };

        const updateTime = () => setCurrentTime(audio.currentTime);
        const handleEnd = () => setPlaying(false);

        audio.addEventListener("timeupdate", updateTime);
        audio.addEventListener("ended", handleEnd);

        setAudio(audio);

        return () => {
          audio.removeEventListener("loadedmetadata", initalizeAudio);
          audio.removeEventListener("timeupdate", updateTime);
          audio.removeEventListener("ended", handleEnd);
        };
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

  return { blob, audio, playing, toggle, currentTime, duration };
};

export default useAudio;
