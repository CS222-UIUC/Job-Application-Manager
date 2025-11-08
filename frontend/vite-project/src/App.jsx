import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage.jsx";
import Login from "./Login.jsx";
import TrackerMain from "./TrackerMain.jsx";
import Profile from "./Profile.jsx";
import ChatAI from "./ChatAI.jsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/tracker" element={<TrackerMain />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/chat-ai" element={<ChatAI />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
