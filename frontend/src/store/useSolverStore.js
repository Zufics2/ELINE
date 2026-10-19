import { create } from "zustand";
import {
  createSolution,
  errorMessage,
  fetchMethods,
  fetchSolution,
  fetchTask,
} from "../api/client";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export const useSolverStore = create((set, get) => ({
  methods: [],
  methodsLoading: false,
  methodsError: null,
  solution: null,
  solving: false,
  error: null,

  loadMethods: async () => {
    if (get().methods.length || get().methodsLoading) return;
    set({ methodsLoading: true, methodsError: null });
    try {
      set({ methods: await fetchMethods() });
    } catch (err) {
      set({ methodsError: errorMessage(err) });
    } finally {
      set({ methodsLoading: false });
    }
  },

  reset: () => set({ solution: null, error: null, solving: false }),

  solve: async (method, input) => {
    set({ solving: true, error: null, solution: null });
    try {
      const { data, queued } = await createSolution({ method, input });
      let solution = data;
      if (queued) {
        // Big problems run in a Celery worker; poll until it finishes.
        for (let i = 0; i < 120; i++) {
          await sleep(1000);
          const task = await fetchTask(data.task_id);
          if (task.status !== "pending") break;
        }
        solution = await fetchSolution(data.id);
      }
      set({ solution });
    } catch (err) {
      set({ error: errorMessage(err) });
    } finally {
      set({ solving: false });
    }
  },
}));
