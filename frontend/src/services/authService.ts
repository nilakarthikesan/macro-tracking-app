import api from '../utils/api';
import {
  UserSignupRequest,
  UserLoginRequest,
  TokenResponse,
  UserResponse,
} from '../types/auth.types';

export class AuthService {
  // Test backend connection
  async testConnection(): Promise<any> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // User signup
  async signup(userData: UserSignupRequest): Promise<TokenResponse> {
    try {
      const response = await api.post('/auth/signup', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // User login
  async login(userData: UserLoginRequest): Promise<TokenResponse> {
    try {
      const response = await api.post('/auth/login', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Get current user
  async getCurrentUser(): Promise<UserResponse> {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Request password reset
  async requestPasswordReset(email: string): Promise<any> {
    try {
      const response = await api.post('/auth/password-reset', { email });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  // Test SendGrid email
  async testSendGrid(): Promise<any> {
    try {
      const response = await api.get('/emails/test-sendgrid');
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

const authService = new AuthService();
export default authService; 