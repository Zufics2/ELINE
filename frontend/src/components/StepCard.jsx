import { Card, Flex, Tag, Typography } from "antd";
import { BlockMath } from "react-katex";

export default function StepCard({ step }) {
  return (
    <Card
      size="small"
      title={
        <Flex gap={8} align="center">
          <Tag color="default" style={{ marginInlineEnd: 0 }}>{step.index}</Tag>
          <span>{step.title}</span>
        </Flex>
      }
    >
      <Typography.Paragraph style={{ marginBottom: step.operation || step.matrix ? 8 : 0 }}>
        {step.description}
      </Typography.Paragraph>
      {step.operation && <BlockMath math={step.operation} errorColor="#cf1322" />}
      {step.matrix && <BlockMath math={step.matrix} errorColor="#cf1322" />}
    </Card>
  );
}
