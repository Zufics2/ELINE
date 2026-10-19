import { useState } from "react";
import { Button, Flex, Segmented, Typography } from "antd";
import MatrixInput, { makeMatrix } from "../components/MatrixInput";

const EXAMPLE = [
  ["2", "1", "-1", "8"],
  ["-3", "-1", "2", "-11"],
  ["-2", "1", "2", "-3"],
];

/** Input form for solvers whose input_schema.type is "augmented_matrix". */
export default function AugmentedMatrixForm({ schema, onSubmit, loading }) {
  const [matrix, setMatrix] = useState(EXAMPLE);
  const [options, setOptions] = useState(
    Object.fromEntries((schema.options || []).map((o) => [o.key, o.default]))
  );

  const submit = () =>
    onSubmit({ matrix: matrix.map((r) => r.map((c) => (c.trim() === "" ? "0" : c))), ...options });

  return (
    <Flex vertical gap={20}>
      {(schema.options || []).map((opt) => (
        <Flex key={opt.key} vertical gap={4}>
          <Typography.Text type="secondary">{opt.label}</Typography.Text>
          <Segmented
            options={opt.choices}
            value={options[opt.key]}
            onChange={(v) => setOptions({ ...options, [opt.key]: v })}
          />
        </Flex>
      ))}

      <MatrixInput value={matrix} onChange={setMatrix} min={schema.min} max={Math.min(schema.max, 10)} />

      <Flex gap={12} wrap>
        <Button type="primary" size="large" loading={loading} onClick={submit}>
          Solve
        </Button>
        <Button size="large" disabled={loading} onClick={() => setMatrix(EXAMPLE)}>
          Load example
        </Button>
        <Button size="large" disabled={loading} onClick={() => setMatrix(makeMatrix(matrix.length, matrix[0].length))}>
          Clear
        </Button>
      </Flex>
    </Flex>
  );
}
