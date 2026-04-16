import axios from "axios";
import config from "../config";

export const api = axios.create({
  baseURL: config.API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 30000,
  withCredentials: true, // Crucial for httpOnly cookies
});

// Since we use httpOnly cookies, we don't attach the Authorization header manually.
// We handle 401 Unauthorized errors to trigger logout/redirect.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && window.location.pathname !== "/login") {
      // Don't redirect if we are already on the login page and get a 401
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
