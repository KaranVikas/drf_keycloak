import keycloak from '../keycloak'
import type { CreateTodoRequest, Todo, TodosResponse, UpdateTodoRequest}  from '../types/todo';
const API_BASE_URL = 'http://localhost:8000/api'

interface ApiRequestOptions {
  method?: string;
  headers?: Record<string,string>;
  body?: any;
}

class ApiService {
  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type':'application/json',
    };

    // Debug: Log the token
    console.log('Getting auth headers, token:', keycloak.token ? 'Present' : 'Missing');
    console.log('Keycloak authenticated:', keycloak.authenticated);

    if(keycloak.token){
      headers['Authorization'] = `Bearer ${keycloak.token}`;
    }

    return headers;
  }

  private async request<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`

    const config: RequestInit = {
      method: options.method || 'GET',
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers,
      },
    };

    if(options.body){
      config.body = JSON.stringify(options.body);
    }

    try{
      console.log()
      console.log("url",url)
      console.log("config", config)
      const response = await fetch(url, config);

      console.log(`🔍 Response status: ${response.status}`);


      if(response.status === 401){
        console.log('401 error - trying to refresh token...');

        //token might be expired  try to refresh
        const refreshed = await keycloak.updateToken(30);
        console.log('🔍 Token refresh result:', refreshed);

        if (refreshed && keycloak.token){
          console.log('Retrying with new token... ')
        //   Retry the request with new token
          config.headers = {
            ...this.getAuthHeaders(),
            ...options.headers,
          };
          const retryResponse = await fetch(url, config);
          if(!retryResponse.ok){
            throw new Error(`HTTP error! status: ${retryResponse.status}`)
          }
          return await retryResponse.json();
        }
        else {
          // Refresh failed, redirect to login
          keycloak.login();
          throw new Error('Authentication required');
        }
      }

      if(!response.ok){
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json();
    } catch(error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

//   USER ENDPOINTS
  async getProfile(): Promise<any> {
    return this.request('/auth/profile');
  }

  async getCurrentUser(): Promise<any>{
    return this.request('/users/me');
  }

  async getTodos(): Promise<TodosResponse> {
        return this.request<TodosResponse>('/todos/');
    }

  async createTodo(todoData: CreateTodoRequest): Promise<Todo> {
      return this.request<Todo>('/todos/', {
          method: 'POST',
          body: todoData,
      });
  }

  async updateTodo(id: number, todoData: UpdateTodoRequest): Promise<Todo> {
      return this.request<Todo>(`/todos/${id}/`, {
          method: 'PUT',
          body: todoData,
      });
  }

  async deleteTodo(id: number): Promise<Todo> {
      return this.request<Todo>(`/todos/${id}/`, {
          method: 'DELETE',
      });
  }

}

export const apiService = new ApiService();
