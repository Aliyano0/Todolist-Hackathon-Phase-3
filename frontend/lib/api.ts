// API client for the Todo application with Better Auth integration
// Better Auth manages JWT tokens in httpOnly cookies

export type PriorityLevel = 'high' | 'medium' | 'low';

export interface TodoItem {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: PriorityLevel;
  category: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    // Get JWT token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options?.headers as Record<string, string>),
    };

    // Add Authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      credentials: 'include', // Send cookies with request
      headers,
    });

    if (response.status === 401) {
      // Redirect to login on unauthorized
      if (typeof window !== 'undefined') {
        window.location.href = '/login?expired=true';
      }
      throw new Error('Unauthorized');
    }

    if (response.status === 403) {
      throw new Error('Access denied');
    }

    if (!response.ok) {
      let errorMessage = 'Request failed';
      try {
        const error = await response.json();
        errorMessage = error.detail || error.message || JSON.stringify(error);
      } catch (e) {
        errorMessage = `Request failed with status ${response.status}`;
      }
      console.error('API Error:', errorMessage);
      throw new Error(errorMessage);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  /**
   * GET /api/{user_id}/tasks - Retrieve all todos for the current user
   */
  async getTodos(userId: string): Promise<TodoItem[]> {
    const data = await this.request<{ data: TodoItem[] }>(`/api/${userId}/tasks`);
    return data.data || [];
  }

  /**
   * POST /api/{user_id}/tasks - Create a new todo
   */
  async createTodo(
    userId: string,
    todoData: Omit<TodoItem, 'id' | 'createdAt' | 'updatedAt' | 'userId'>
  ): Promise<TodoItem> {
    const data = await this.request<{ data: TodoItem }>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(todoData),
    });

    return data.data;
  }

  /**
   * PUT /api/{user_id}/tasks/{id} - Update an existing todo
   */
  async updateTodo(
    userId: string,
    id: string,
    todoData: Partial<TodoItem>
  ): Promise<TodoItem> {
    const updatePayload: Partial<TodoItem> = {};
    if (todoData.title !== undefined) updatePayload.title = todoData.title;
    if (todoData.description !== undefined) updatePayload.description = todoData.description;
    if (todoData.completed !== undefined) updatePayload.completed = todoData.completed;
    if (todoData.priority !== undefined) updatePayload.priority = todoData.priority;
    if (todoData.category !== undefined) updatePayload.category = todoData.category;

    const data = await this.request<{ data: TodoItem }>(`/api/${userId}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updatePayload),
    });

    return data.data;
  }

  /**
   * DELETE /api/{user_id}/tasks/{id} - Delete a todo
   */
  async deleteTodo(userId: string, id: string): Promise<void> {
    await this.request<void>(`/api/${userId}/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  /**
   * PATCH /api/{user_id}/tasks/{id}/toggle - Toggle the completion status of a todo
   */
  async toggleTodoComplete(userId: string, id: string): Promise<TodoItem> {
    const data = await this.request<{ data: TodoItem }>(`/api/${userId}/tasks/${id}/toggle`, {
      method: 'PATCH',
    });

    return data.data;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();