import { useAuth } from "@/contexts/auth";

export default function HomePage() {
  const { user } = useAuth();
  return (
    <main>
      <h1>
        Welcome back,{" "}
        <span className="text-purple-800 dark:text-purple-400">
          {user?.name}
        </span>
      </h1>
    </main>
  );
}
