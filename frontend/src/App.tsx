import { ThemeProvider } from "@/contexts/theme";
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "@/styles/global.css";
import { AuthProvider } from "./contexts/auth";
import ProtectedRoute from "./pages/ProtectedRoute";
import { Toaster } from "./components/ui/toaster";
import { ChatProvider } from "./contexts/chat";
// Lazy Load the pages
const Homepage = lazy(() => import("@/pages/Home"));
const LoginPage = lazy(() => import("@/pages/Login"));
const RegisterPage = lazy(() => import("@/pages/Register"));
const AppLayout = lazy(() => import("@/pages/AppLayout"));
const ScoreSheet = lazy(() => import("@/pages/ScoreSheet"));
const ScoreSheetList = lazy(() => import("@/pages/ScoreSheetList"));
const PageNotFound = lazy(() => import("@/pages/PageNotFound"));
const BotPage = lazy(() => import("@/pages/Bot"));

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="dark-mode">
      <BrowserRouter>
        <AuthProvider>
          <Suspense>
            <Routes>
              <Route index path="/" element={<LoginPage />} />
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegisterPage />} />
              <Route
                path="app"
                element={
                  <ProtectedRoute>
                    <ChatProvider>
                      <AppLayout />
                    </ChatProvider>
                  </ProtectedRoute>
                }
              >
                <Route index element={<Homepage />} />
                <Route path="home" element={<Homepage />} />
                <Route path="bot" element={<BotPage />} />
                <Route path="scores" element={<ScoreSheetList />} />
                <Route path="scores/:id" element={<ScoreSheet />} />
              </Route>
              <Route path="*" element={<PageNotFound />} />
            </Routes>
          </Suspense>
        </AuthProvider>
      </BrowserRouter>
      <Toaster />
    </ThemeProvider>
  );
}

export default App;
