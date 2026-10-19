import { Card, Flex, Result, Spin, Typography } from "antd";
import ResultCard from "./ResultCard";
import StepsViewer from "./StepsViewer";

/** Renders any stored solution using the shared step format. */
export default function SolutionView({ solution }) {
  if (solution.status === "pending") {
    return (
      <Card>
        <Flex gap={12} align="center">
          <Spin /> <span>The solution is still being computed…</span>
        </Flex>
      </Card>
    );
  }
  if (solution.status === "failed") {
    return <Result status="error" title="The solver failed" subTitle={solution.error} />;
  }
  return (
    <Flex vertical gap={16}>
      <ResultCard result={solution.result} latex={solution.result_latex} />
      <Typography.Title level={4} style={{ margin: "8px 0 0" }}>
        Steps
      </Typography.Title>
      <StepsViewer steps={solution.steps} />
    </Flex>
  );
}
