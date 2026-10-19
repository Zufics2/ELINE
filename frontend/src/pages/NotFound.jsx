import { Result } from "antd";
import { Link } from "react-router-dom";

export default function NotFound() {
  return <Result status="404" title="Page not found" extra={<Link to="/">Back to methods</Link>} />;
}
