import type {RegisterUserRequest, RegisterUserResponse, User} from "../types/users.ts";
import {apiService} from "./apiService.ts";

class UserService {
  async registerUser(userData: RegisterUserRequest) :Promise<RegisterUserResponse>{
    return apiService.registerUser(userData);
  }

  async getMe(): Promise<User>{
    return apiService.getCurrentUser();
  }

  async syncKeycloakUser(): Promise<User>{
    return apiService.syncKeycloakUser();
  }
}

export const userService = new UserService()