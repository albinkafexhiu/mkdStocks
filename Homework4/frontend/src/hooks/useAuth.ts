import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../api/auth';
import { AuthFormState, LoginCredentials } from '../types/auth';
import toast from 'react-hot-toast';

export const useAuth = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState<AuthFormState>({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (isLogin) {
        const credentials: LoginCredentials = {
          email: formData.email,
          password: formData.password
        };
        
        await authApi.login(credentials);
        navigate('/home');
        toast.success('Login successful!');
      } else {
        if (formData.password !== formData.confirmPassword) {
          toast.error('Passwords do not match!');
          return;
        }
        
        await authApi.register({
          email: formData.email,
          password: formData.password,
          full_name: formData.fullName
        });
        
        toast.success('Registration successful! Please login.');
        setIsLogin(true);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Something went wrong';
      toast.error(errorMessage);
    }
  };

  const updateFormData = (field: keyof AuthFormState, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return {
    isLogin,
    formData,
    setIsLogin,
    handleSubmit,
    updateFormData
  };
};