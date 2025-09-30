import keycloak from '../keycloak'

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
      const response = await fetch(url, config);

      if(response.status === 401){
        //token might be expired  try to refresh
        const refreshed = await keycloak.updateToken(30);
        if (refreshed && keycloak.token){
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

//   Example API methods
  async getProfile(): Promise<any> {
    return this.request('/auth/profile');
  }

  async getTodos(): Promise<any[]> {
        return this.request('/todos');
    }

    async createTodo(todo: any): Promise<any> {
        return this.request('/todos', {
            method: 'POST',
            body: todo,
        });
    }

    async updateTodo(id: string, todo: any): Promise<any> {
        return this.request(`/todos/${id}`, {
            method: 'PUT',
            body: todo,
        });
    }

    async deleteTodo(id: string): Promise<void> {
        return this.request(`/todos/${id}`, {
            method: 'DELETE',
        });
    }

}

export const apiService = new ApiService();
