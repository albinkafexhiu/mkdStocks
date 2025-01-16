import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import axios from 'axios';

const AuthPage = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: ''
  });

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    
    try {
      if (isLogin) {
        const response = await axios.post('http://localhost:8000/api/auth/login', {
          email: formData.email,
          password: formData.password
        });
        toast.success('Login successful!');
        navigate('/stocks');
      } else {
        // Check if passwords match for registration
        if (formData.password !== formData.confirmPassword) {
          toast.error('Passwords do not match!');
          return;
        }
        
        const response = await axios.post('http://localhost:8000/api/auth/register', {
          email: formData.email,
          password: formData.password,
          full_name: formData.fullName
        });
        toast.success('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Something went wrong');
    }
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      {/* Left side with glassmorphism effect */}
      <div className="relative w-full md:w-1/2 bg-gradient-to-br from-blue-600 to-indigo-800 p-8 md:p-12 flex flex-col justify-between overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/[0.2] -z-1" />
        
        {/* Decorative blurred circles */}
        <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-blue-400 opacity-20 blur-3xl" />
        <div className="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-indigo-400 opacity-20 blur-3xl" />
        
        <div className="relative z-10">
          <h1 className="text-3xl md:text-5xl font-bold text-white mb-4">
            Macedonian Stock Exchange
          </h1>
          <p className="text-blue-100 text-lg md:text-xl font-light">
            Empowering your investment decisions with real-time market insights
          </p>
        </div>

        <div className="relative z-10 backdrop-blur-lg bg-white/10 rounded-2xl p-6 mt-8 md:mt-0">
          <h3 className="text-white text-xl mb-4 font-medium">Market Pulse</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-100">MBI10 Index</span>
              <span className="text-emerald-400 font-medium">+1.2%</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-100">Daily Volume</span>
              <span className="text-white font-medium">€2.5M</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-blue-100">Market Status</span>
              <span className="text-emerald-400 font-medium">Open</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - Auth form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="mb-8 text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {isLogin ? 'Welcome back' : 'Create your account'}
            </h2>
            <p className="text-gray-600">
              {isLogin 
                ? 'Enter your credentials to access your portfolio' 
                : 'Start your investment journey today'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {!isLogin && (
              <Input
                label="Full Name"
                type="text"
                placeholder="John Doe"
                value={formData.fullName}
                onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                required
              />
            )}
            
            <Input
              label="Email"
              type="email"
              placeholder="name@company.com"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />

            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />

            {!isLogin && (
              <Input
                label="Confirm Password"
                type="password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                required
              />
            )}

            <Button 
              type="submit" 
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium"
            >
              {isLogin ? 'Sign in' : 'Create account'}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                {isLogin ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;