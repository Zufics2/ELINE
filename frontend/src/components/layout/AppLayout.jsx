import { Layout, Menu, Typography } from "antd";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

const { Header, Content, Footer } = Layout;

const items = [
  { key: "/", label: "Methods" },
  { key: "/history", label: "History" },
];

export default function AppLayout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const selected = pathname.startsWith("/history") || pathname.startsWith("/solutions") ? "/history" : "/";

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center", gap: 32 }}>
        <Typography.Title
          level={3}
          style={{ color: "#fff", margin: 0, cursor: "pointer", letterSpacing: 1 }}
          onClick={() => navigate("/")}
        >
          ELINE
        </Typography.Title>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[selected]}
          items={items}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: "32px 24px" }}>
        <div style={{ maxWidth: 960, margin: "0 auto" }}>
          <Outlet />
        </div>
      </Content>
      <Footer style={{ textAlign: "center" }}>ELINE – linear algebra, step by step</Footer>
    </Layout>
  );
}
