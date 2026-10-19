import { Card, Flex, Tag, Typography } from "antd";
import { BlockMath } from "react-katex";

const KINDS = {
  unique: { color: "success", label: "Unique solution" },
  infinite: { color: "warning", label: "Infinitely many solutions" },
  none: { color: "error", label: "No solution" },
};

export default function ResultCard({ result, latex }) {
  const kind = KINDS[result?.type] || { color: "default", label: "Result" };
  return (
    <Card title="Result">
      <Flex gap={8} wrap style={{ marginBottom: 8 }}>
        <Tag color={kind.color}>{kind.label}</Tag>
        {result?.rank !== undefined && <Tag>rank {result.rank}</Tag>}
        {result?.free_variables?.length > 0 && (
          <Tag>free: {result.free_variables.join(", ")}</Tag>
        )}
      </Flex>
      {result?.type === "infinite" && (
        <Typography.Paragraph type="secondary">
          Each free variable can take any value; the symbols t₁, t₂, … stand for those values.
        </Typography.Paragraph>
      )}
      <BlockMath math={latex} errorColor="#cf1322" />
    </Card>
  );
}
