import { Flex } from "antd";
import StepCard from "./StepCard";

export default function StepsViewer({ steps }) {
  return (
    <Flex vertical gap={12}>
      {steps.map((s) => (
        <StepCard key={s.index} step={s} />
      ))}
    </Flex>
  );
}
