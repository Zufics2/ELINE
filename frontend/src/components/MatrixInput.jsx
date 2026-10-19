import { Fragment } from "react";
import { Flex, Input, InputNumber, Typography } from "antd";

const { Text } = Typography;

export function makeMatrix(rows, cols, old = []) {
  return Array.from({ length: rows }, (_, i) =>
    Array.from({ length: cols }, (_, j) => old[i]?.[j] ?? "0")
  );
}

/** Editable augmented matrix [A | b]. `value` is an array of rows of strings. */
export default function MatrixInput({ value, onChange, min = 1, max = 10 }) {
  const rows = value.length;
  const vars = value[0].length - 1;

  const setCell = (i, j, v) =>
    onChange(value.map((row, r) => (r === i ? row.map((c, k) => (k === j ? v : c)) : row)));

  const resize = (r, v) => onChange(makeMatrix(r, v + 1, value));

  return (
    <Flex vertical gap={16}>
      <Flex gap={24} wrap>
        <Flex vertical gap={4}>
          <Text type="secondary">Equations</Text>
          <InputNumber min={min} max={max} value={rows} onChange={(n) => n && resize(n, vars)} />
        </Flex>
        <Flex vertical gap={4}>
          <Text type="secondary">Variables</Text>
          <InputNumber min={min} max={max} value={vars} onChange={(n) => n && resize(rows, n)} />
        </Flex>
      </Flex>

      <div style={{ overflowX: "auto", paddingBottom: 4 }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: `repeat(${vars}, 76px) 20px 76px`,
            gap: 8,
            alignItems: "center",
            width: "max-content",
          }}
        >
          {Array.from({ length: vars }, (_, j) => (
            <Text key={`h${j}`} type="secondary" style={{ textAlign: "center" }}>
              x<sub>{j + 1}</sub>
            </Text>
          ))}
          <span />
          <Text type="secondary" style={{ textAlign: "center" }}>constant</Text>

          {value.map((row, i) =>
            row.map((cell, j) => (
              <Fragment key={`${i}-${j}`}>
                {j === vars && (
                  <span style={{ borderLeft: "2px solid #8c8c8c", height: 28, justifySelf: "center" }} />
                )}
                <Input
                  aria-label={`Row ${i + 1}, ${j === vars ? "constant" : `x${j + 1}`}`}
                  value={cell}
                  style={{ textAlign: "center" }}
                  onChange={(e) => setCell(i, j, e.target.value)}
                  onFocus={(e) => e.target.select()}
                />
              </Fragment>
            ))
          )}
        </div>
      </div>
      <Text type="secondary">Integers, decimals and fractions such as 1/3 are accepted.</Text>
    </Flex>
  );
}
