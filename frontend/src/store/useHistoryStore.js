import { create } from "zustand";
import { deleteSolution, errorMessage, fetchSolutions } from "../api/client";

export const useHistoryStore = create((set, get) => ({
  items: [],
  loading: false,
  error: null,

  load: async () => {
    set({ loading: true, error: null });
    try {
      set({ items: await fetchSolutions() });
    } catch (err) {
      set({ error: errorMessage(err) });
    } finally {
      set({ loading: false });
    }
  },

  remove: async (id) => {
    await deleteSolution(id);
    set({ items: get().items.filter((x) => x.id !== id) });
  },
}));
