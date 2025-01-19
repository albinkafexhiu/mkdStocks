import React from 'react';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { AuthFormState } from '../../types/auth';

interface AuthFormProps {
  isLogin: boolean;
  formData: AuthFormState;
  onSubmit: (e: React.FormEvent) => Promise<void>;
  onUpdate: (field: keyof AuthFormState, value: string) => void;
  onToggleMode: () => void;
}

export const AuthForm: React.FC<AuthFormProps> = ({
  isLogin,
  formData,
  onSubmit,
  onUpdate,
  onToggleMode
}) => (
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

      <form onSubmit={onSubmit} className="space-y-6">
        {!isLogin && (
          <Input
            label="Full Name"
            type="text"
            placeholder="John Doe"
            value={formData.fullName}
            onChange={(e) => onUpdate('fullName', e.target.value)}
            required
          />
        )}
        
        <Input
          label="Email"
          type="email"
          placeholder="name@company.com"
          value={formData.email}
          onChange={(e) => onUpdate('email', e.target.value)}
          required
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          value={formData.password}
          onChange={(e) => onUpdate('password', e.target.value)}
          required
        />

        {!isLogin && (
          <Input
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            value={formData.confirmPassword}
            onChange={(e) => onUpdate('confirmPassword', e.target.value)}
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
            onClick={onToggleMode}
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            {isLogin ? 'Sign up' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  </div>
);