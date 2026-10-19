import { useEffect } from "react";
import { Button, Flex, Result, Spin, Typography } from "antd";
import MethodSelector from "../components/MethodSelector";
import { useSolverStore } from "../store/useSolverStore";

export default function HomePage() {
  const { methods, methodsLoading, methodsError, loadMethods } = useSolverStore();
  useEffect(() => { loadMethods(); }, [loadMethods]);

  return (
    <Flex vertical gap={24}>
      <div>
        <Typography.Title style={{ marginTop: 0 }}>Solve linear algebra, one step at a time</Typography.Title>
        <Typography.Paragraph type="secondary" style={{ fontSize: 17 }}>
          Pick a method, enter your matrix and see every row operation explained.
        </Typography.Paragraph>
      </div>
      {methodsLoading && <Spin />}
      {methodsError && (
        <Result
          status="error"
          title="Could not load methods"
          subTitle={methodsError}
          extra={<Button onClick={loadMethods}>Try again</Button>}
        />
      )}
      {!methodsLoading && !methodsError && <MethodSelector methods={methods} />}
    </Flex>
  );
}
