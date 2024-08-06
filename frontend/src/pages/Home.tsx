import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/contexts/auth";
import { Score } from "@/features/score/Score";

export default function HomePage() {
  const { user } = useAuth();
  return (
    <>
      <h1>
        Welcome back,{" "}
        <span className="text-purple-800 dark:text-purple-400">
          {user?.name}
        </span>
      </h1>
      <Separator className="my-6" />
      <h2 className="mt-10 scroll-m-20 pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0">
        You latest English Score:
      </h2>
      <Score />
    </>
  );
}
