import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/ui/Navbar';
import AuthPage from './pages/AuthPage';
import DashboardPage from './pages/DashboardPage';
import StockDataViewer from './components/StockDataViewer';

function App() {
  // Check if user is on auth page
  const isAuthPage = window.location.pathname === '/';

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
      {isAuthPage ? (
        <AuthPage />
      ) : (
        <Navbar>
          <Routes>
            <Route path="/stocks" element={<StockDataViewer />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </Navbar>
      )}
    </BrowserRouter>
  );
}

export default App;