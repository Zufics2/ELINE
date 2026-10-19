import { Card, Col, Row, Typography } from "antd";
import { useNavigate } from "react-router-dom";

export default function MethodSelector({ methods }) {
  const navigate = useNavigate();
  return (
    <Row gutter={[16, 16]}>
      {methods.map((m) => (
        <Col key={m.key} xs={24} md={12}>
          <Card hoverable onClick={() => navigate(`/solve/${m.key}`)} style={{ height: "100%" }}>
            <Typography.Title level={4} style={{ marginTop: 0 }}>{m.name}</Typography.Title>
            <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
              {m.description}
            </Typography.Paragraph>
          </Card>
        </Col>
      ))}
    </Row>
  );
}
