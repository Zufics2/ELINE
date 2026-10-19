import axios from "axios";

const http = axios.create({ baseURL: import.meta.env.VITE_API_URL || "/api" });

export const fetchMethods = () => http.get("/methods/").then((r) => r.data);

// Resolves to { data, queued }: queued is true when the server answered 202.
export const createSolution = (payload) =>
  http.post("/solutions/", payload).then((r) => ({ data: r.data, queued: r.status === 202 }));

export const fetchSolutions = () => http.get("/solutions/").then((r) => r.data);
export const fetchSolution = (id) => http.get(`/solutions/${id}/`).then((r) => r.data);
export const deleteSolution = (id) => http.delete(`/solutions/${id}/`);
export const fetchTask = (taskId) => http.get(`/tasks/${taskId}/`).then((r) => r.data);

// Turns an axios error into one readable sentence.
export function errorMessage(err) {
  const data = err?.response?.data;
  if (data && typeof data === "object") {
    const first = Object.values(data)[0];
    return Array.isArray(first) ? first[0] : String(first);
  }
  if (err?.response) return `Request failed (${err.response.status}).`;
  return "Cannot reach the server. Check that the backend is running.";
}
