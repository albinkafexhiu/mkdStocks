import React from 'react';
import { AuthHero } from '../components/auth/AuthHero';
import { AuthForm } from '../components/auth/AuthForm';
import { useAuth } from '../hooks/useAuth';

const AuthPage: React.FC = () => {
  const {
    isLogin,
    formData,
    setIsLogin,
    handleSubmit,
    updateFormData
  } = useAuth();

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      <AuthHero />
      <AuthForm
        isLogin={isLogin}
        formData={formData}
        onSubmit={handleSubmit}
        onUpdate={updateFormData}
        onToggleMode={() => setIsLogin(!isLogin)}
      />
    </div>
  );
};

export default AuthPage;