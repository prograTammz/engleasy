import { ThemeProvider } from "@/contexts/theme";
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Lazy Load the pages
const Homepage = lazy(() => import("@/pages/Home"));

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      {/* <ChatWindow />; */}
      <BrowserRouter>
        <Suspense>
          <Routes>
            <Route index element={<Homepage />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
