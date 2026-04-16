/**
 * Centralized environment configuration.
 * Always check for required environment variables at runtime.
 */

const getEnvVar = (key: string, required = true): string => {
  const value = import.meta.env[key];
  if (!value && required) {
    if (import.meta.env.DEV) {
      console.warn(`Environment variable ${key} is missing. Falling back to defaults.`);
    }
  }
  return value || "";
};

export const config = {
  API_URL: getEnvVar("VITE_API_URL") || "/api/v1",
  WS_URL: getEnvVar("VITE_WS_URL") || "ws://localhost:8000",
  ENVIRONMENT: import.meta.env.MODE || "development",
  IS_DEV: import.meta.env.DEV,
  IS_PROD: import.meta.env.PROD,
  APP_NAME: "TensorAI",
  VERSION: "0.1.0",
};

export default config;
