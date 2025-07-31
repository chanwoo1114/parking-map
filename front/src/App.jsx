import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import MapPage from './pages/MapPage.jsx';
import OAuthCallback from './pages/OAuthCallback.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
          <Route path="/map" element={<MapPage />} />

          <Route path="/oauth/callback/:provider" element={<OAuthCallback />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
