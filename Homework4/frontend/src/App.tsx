import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/ui/Navbar';
import AuthPage from './pages/AuthPage';
import DashboardPage from './pages/DashboardPage';
import HomePage from './pages/HomePage';
import StockDataViewer from './components/StockDataViewer';
import AnalysisPage from './pages/AnalysisPage';
import FundamentalAnalysisPage from './pages/FundamentalAnalysisPage';

function App() {
  return (
    <BrowserRouter>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            iconTheme: {
              primary: '#4ade80',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      <Routes>
        {/* Auth route */}
        <Route path="/" element={<AuthPage />} />
        
        {/* Protected routes wrapped in Navbar */}
        <Route element={<Navbar />}>
          <Route path="/home" element={<HomePage />} />
          <Route path="/stocks" element={<StockDataViewer />} />
          <Route path="/stocks/:symbol" element={<StockDataViewer />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/analysis" element={<AnalysisPage />} />
          <Route path="/fundamental" element={<FundamentalAnalysisPage />} />


        </Route>
        
        {/* Redirect unknown routes to auth page */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;