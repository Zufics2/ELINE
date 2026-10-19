import { useEffect } from "react";
import { Button, Card, Flex, Result, Spin, Typography } from "antd";
import { Link, useParams } from "react-router-dom";
import SolutionView from "../components/SolutionView";
import { inputForms } from "../methods";
import { useSolverStore } from "../store/useSolverStore";

export default function SolverPage() {
  const { methodKey } = useParams();
  const { methods, methodsLoading, methodsError, loadMethods, solve, solving, solution, error, reset } =
    useSolverStore();

  useEffect(() => { loadMethods(); }, [loadMethods]);
  useEffect(() => { reset(); }, [methodKey, reset]);

  if (methodsLoading || (!methods.length && !methodsError)) return <Spin />;
  if (methodsError) return <Result status="error" title="Could not load methods" subTitle={methodsError} extra={<Button onClick={loadMethods}>Try again</Button>} />;

  const method = methods.find((m) => m.key === methodKey);
  if (!method)
    return <Result status="404" title="Unknown method" extra={<Link to="/">Back to methods</Link>} />;

  const Form = inputForms[method.input_schema.type];

  return (
    <Flex vertical gap={24}>
      <div>
        <Typography.Title style={{ marginTop: 0 }}>{method.name}</Typography.Title>
        <Typography.Paragraph type="secondary">{method.description}</Typography.Paragraph>
      </div>

      <Card>
        {Form ? (
          <Form
            key={method.key}
            schema={method.input_schema}
            loading={solving}
            onSubmit={(input) => solve(method.key, input)}
          />
        ) : (
          <Typography.Text type="danger">
            This method needs an input form of type “{method.input_schema.type}”, which the app does not have yet.
          </Typography.Text>
        )}
      </Card>

      {error && <Typography.Text type="danger">{error}</Typography.Text>}
      {solution && <SolutionView solution={solution} />}
    </Flex>
  );
}
