import { ThemeProvider } from "@/contexts/theme";
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@/styles/global.css";
// Lazy Load the pages
const Homepage = lazy(() => import("@/pages/Home"));
const LoginPage = lazy(() => import("@/pages/Login"));

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="dark-mode">
      {/* <ChatWindow />; */}
      <BrowserRouter>
        <Suspense>
          <Routes>
            <Route index element={<Homepage />} />
            <Route path="login" element={<LoginPage />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
