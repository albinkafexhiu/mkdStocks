import React, { useState } from 'react';
import { useNavigate, useLocation, Outlet } from 'react-router-dom';
import { 
  Home,
  Search,
  BarChart2,
  Menu,
  ChevronLeft,
  LogOut
} from 'lucide-react';

const Navbar = () => {
  const [isExpanded, setIsExpanded] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/home', icon: BarChart2, label: 'Home' },
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/stocks', icon: Search, label: 'Search Stocks' },
    { path: '/analysis', icon: BarChart2, label: 'Analysis' },
    { path: '/fundamental', icon: BarChart2, label: 'Fundamental Analysis' },

    
  ];

  const isActivePath = (path: string) => {
    return location.pathname === path;
  };

  const handleLogout = () => {
    navigate('/');
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <nav className={`
        fixed top-0 left-0 h-full bg-white border-r border-gray-200
        transition-all duration-300 ease-in-out z-50
        ${isExpanded ? 'w-64' : 'w-20'}
      `}>
        {/* Header */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
          {isExpanded && (
            <span className="text-lg font-semibold text-gray-900">MSE Analysis</span>
          )}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            {isExpanded ? <ChevronLeft size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Navigation Items */}
        <div className="flex-1 py-6 flex flex-col gap-2 px-3">
          {navItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`
                flex items-center gap-3 p-3 rounded-lg transition-colors
                ${isActivePath(item.path)
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-100'
                }
              `}
            >
              <item.icon size={20} />
              {isExpanded && <span>{item.label}</span>}
            </button>
          ))}
        </div>

        {/* Logout Button */}
        <div className="p-3 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 p-3 w-full rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
          >
            <LogOut size={20} />
            {isExpanded && <span>Logout</span>}
          </button>
        </div>
      </nav>

      {/* Main Content Container */}
      <main className={`
        flex-1 min-h-screen
        transition-all duration-300 ease-in-out
        ${isExpanded ? 'ml-64' : 'ml-20'}
      `}>
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Navbar;