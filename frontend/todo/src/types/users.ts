export interface User {
  id: number;
  username: string;
  email: string;
  name?: string;
  url?: string;
}

export interface RegisterUserRequest {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  name?: string;
}

export interface RegisterUserResponse {
  username: string;
  name: string;
  url: string;
}

export interface RegisterFormProps {
  onRegistrationSuccess?: () => void;
  onCancel?: () =>  void;
}

export interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  name: string;
}