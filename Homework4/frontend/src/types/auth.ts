export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface RegisterData extends LoginCredentials {
    confirmPassword: string;
    fullName: string;
  }
  
  export interface AuthFormState {
    email: string;
    password: string;
    confirmPassword: string;
    fullName: string;
  }