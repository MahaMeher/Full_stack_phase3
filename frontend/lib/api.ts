import { getSession } from '@/lib/auth';
import { Task, TaskFormData } from '@/types/task';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export { API_BASE_URL };

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  success: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL || 'http://localhost:8000';
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseUrl}${endpoint}`;

      // Prepare headers explicitly
      const sessionHeader = await this.getSessionHeader();
      const optionsHeaders = options.headers || {};

      // Merge headers safely
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...sessionHeader,
        ...optionsHeaders,
      };

      // Prepare fetch options without headers to avoid conflicts
      const fetchOptions: RequestInit = {
        method: options.method,
        body: options.body,
        cache: options.cache,
        credentials: options.credentials,
        headers,
        integrity: options.integrity,
        keepalive: options.keepalive,
        mode: options.mode,
        redirect: options.redirect,
        referrer: options.referrer,
        referrerPolicy: options.referrerPolicy,
        signal: options.signal,
        window: options.window,
      };

      const response = await fetch(url, fetchOptions);

      if (!response.ok) {
        // Try to get error message from response
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json();
            if (errorData.message) {
              errorMessage = errorData.message;
            }
          } else {
            const errorText = await response.text();
            if (errorText) {
              errorMessage = errorText;
            }
          }
        } catch (parseError) {
          // If we can't parse the error response, use the status code
          console.warn('Could not parse error response:', parseError);
        }

        return { error: errorMessage, success: false };
      }

      // Handle 204 No Content responses (and other 2xx responses with no content)
      if (response.status === 204) {
        return { data: null as any, success: true };
      }

      // Check if response has content before trying to parse JSON
      const contentLength = response.headers.get('content-length');
      const contentType = response.headers.get('content-type');

      if (contentLength === '0' || !contentType || !contentType.includes('application/json')) {
        // If there's no content or not JSON, return empty data
        return { data: null as any, success: true };
      }

      // For responses with JSON content, parse normally
      const data = await response.json();
      return { data, success: true };
    } catch (error: any) {
      // Log error for debugging
      console.error('API request error:', error);

      // Format error message for user
      let errorMessage = error.message || 'An error occurred';
      if (error.message.includes('fetch')) {
        errorMessage = 'Network error - please check your connection';
      }

      return { error: errorMessage, success: false };
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    });
  }

  async put<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    });
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  async patch<T>(endpoint: string, body: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(body),
    });
  }

  // Task-specific API methods
  async getTasks(): Promise<ApiResponse<Task[]>> {
    const response = await this.get<any>('/api/tasks');
    if (response.success && response.data && Array.isArray(response.data.tasks)) {
      // Handle the wrapped response format from backend and transform snake_case to camelCase
      const transformedTasks = response.data.tasks.map((task: any) => ({
        id: task.id,
        title: task.title,
        description: task.description,
        completed: task.completed,
        createdAt: task.created_at,
        updatedAt: task.updated_at,
        userId: task.user_id,
      }));
      return { data: transformedTasks, success: true };
    } else if (response.success && Array.isArray(response.data)) {
      // Fallback: handle direct array response and transform snake_case to camelCase
      const transformedTasks = response.data.map((task: any) => ({
        id: task.id,
        title: task.title,
        description: task.description,
        completed: task.completed,
        createdAt: task.created_at,
        updatedAt: task.updated_at,
        userId: task.user_id,
      }));
      return { data: transformedTasks, success: true };
    }
    return { error: response.error || 'Failed to fetch tasks', success: false };
  }

  async getTask(id: string): Promise<ApiResponse<Task>> {
    const response = await this.get<any>(`/api/tasks/${id}`);
    if (response.success && response.data) {
      // Transform snake_case to camelCase
      const transformedTask = {
        id: response.data.id,
        title: response.data.title,
        description: response.data.description,
        completed: response.data.completed,
        createdAt: response.data.created_at,
        updatedAt: response.data.updated_at,
        userId: response.data.user_id,
      };
      return { data: transformedTask, success: true };
    }
    return { error: response.error || 'Failed to fetch task', success: false };
  }

  async createTask(taskData: TaskFormData): Promise<ApiResponse<Task>> {
    const response = await this.post<any>('/api/tasks', taskData);
    if (response.success && response.data) {
      // Transform snake_case to camelCase
      const transformedTask = {
        id: response.data.id,
        title: response.data.title,
        description: response.data.description,
        completed: response.data.completed,
        createdAt: response.data.created_at,
        updatedAt: response.data.updated_at,
        userId: response.data.user_id,
      };
      return { data: transformedTask, success: true };
    }
    return { error: response.error || 'Failed to create task', success: false };
  }

  async updateTask(id: string, taskData: Partial<TaskFormData>): Promise<ApiResponse<Task>> {
    const response = await this.put<any>(`/api/tasks/${id}`, taskData);
    if (response.success && response.data) {
      // Transform snake_case to camelCase
      const transformedTask = {
        id: response.data.id,
        title: response.data.title,
        description: response.data.description,
        completed: response.data.completed,
        createdAt: response.data.created_at,
        updatedAt: response.data.updated_at,
        userId: response.data.user_id,
      };
      return { data: transformedTask, success: true };
    }
    return { error: response.error || 'Failed to update task', success: false };
  }

  async deleteTask(id: string): Promise<ApiResponse<boolean>> {
    const response = await this.request<any>(`/api/tasks/${id}`, { method: 'DELETE' });
    if (response.success) {
      // Return true to indicate successful deletion
      return { data: true, success: true };
    }
    return response;
  }

  private async getSessionHeader(): Promise<Record<string, string>> {
    try {
      const session = await getSession();
      return session?.jwtToken ? { 'Authorization': `Bearer ${session.jwtToken}` } : {};
    } catch {
      return {};
    }
  }

  async toggleTaskCompletion(id: string): Promise<ApiResponse<Task>> {
    const response = await this.patch<any>(`/api/tasks/${id}/complete`, {});
    if (response.success && response.data) {
      // Transform snake_case to camelCase
      const transformedTask = {
        id: response.data.id,
        title: response.data.title,
        description: response.data.description,
        completed: response.data.completed,
        createdAt: response.data.created_at,
        updatedAt: response.data.updated_at,
        userId: response.data.user_id,
      };
      return { data: transformedTask, success: true };
    }
    return { error: response.error || 'Failed to toggle task completion', success: false };
  }

  // Chat API methods
  async sendMessage(message: string, conversationId?: string): Promise<ApiResponse<any>> {
    const requestBody: any = { message };
    if (conversationId) {
      requestBody.conversation_id = conversationId;
    }

    const response = await this.post<any>('/api/chat', requestBody);
    return response;
  }

  async getConversationHistory(conversationId: string): Promise<ApiResponse<any>> {
    const response = await this.get<any>(`/api/conversations/${conversationId}`);
    return response;
  }

  async deleteConversation(conversationId: string): Promise<ApiResponse<any>> {
    const response = await this.delete<any>(`/api/conversations/${conversationId}`);
    return response;
  }
}

export const apiClient = new ApiClient();