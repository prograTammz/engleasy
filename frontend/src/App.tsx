import { ThemeProvider } from "@/contexts/theme";
import "./styles/global.css";
import { ChatWindow } from "@/features/chat-widget/ChatWindow";

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <ChatWindow />;
    </ThemeProvider>
  );
}

export default App;
