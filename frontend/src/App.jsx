import { App as AntApp, ConfigProvider } from "antd";
import { RouterProvider } from "react-router-dom";
import router from "./routes";

const theme = {
  token: { colorPrimary: "#1d5c63", borderRadius: 6, fontSize: 15 },
};

export default function App() {
  return (
    <ConfigProvider theme={theme}>
      <AntApp>
        <RouterProvider router={router} />
      </AntApp>
    </ConfigProvider>
  );
}
