import { createBrowserRouter } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import HistoryPage from "../pages/HistoryPage";
import HomePage from "../pages/HomePage";
import NotFound from "../pages/NotFound";
import SolutionPage from "../pages/SolutionPage";
import SolverPage from "../pages/SolverPage";

export default createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: "/", element: <HomePage /> },
      { path: "/solve/:methodKey", element: <SolverPage /> },
      { path: "/history", element: <HistoryPage /> },
      { path: "/solutions/:id", element: <SolutionPage /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);
