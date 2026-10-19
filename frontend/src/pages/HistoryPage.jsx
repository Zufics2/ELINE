import { useEffect } from "react";
import { App, Button, Empty, Flex, Popconfirm, Table, Tag, Typography } from "antd";
import { Link } from "react-router-dom";
import { useHistoryStore } from "../store/useHistoryStore";

const TYPE_TAGS = {
  unique: ["success", "Unique"],
  infinite: ["warning", "Infinite"],
  none: ["error", "No solution"],
};

export default function HistoryPage() {
  const { items, loading, error, load, remove } = useHistoryStore();
  const { message } = App.useApp();
  useEffect(() => { load(); }, [load]);

  const columns = [
    { title: "#", dataIndex: "id", width: 70 },
    { title: "Method", dataIndex: "method" },
    {
      title: "Size",
      dataIndex: "input",
      render: (input) =>
        input?.matrix ? `${input.matrix.length} × ${input.matrix[0].length - 1}` : "–",
    },
    {
      title: "Outcome",
      render: (_, row) => {
        if (row.status !== "done") return <Tag>{row.status}</Tag>;
        const [color, label] = TYPE_TAGS[row.result_type] || ["default", "–"];
        return <Tag color={color}>{label}</Tag>;
      },
    },
    { title: "Created", dataIndex: "created_at", render: (v) => new Date(v).toLocaleString() },
    {
      title: "",
      align: "right",
      render: (_, row) => (
        <Flex gap={8} justify="flex-end">
          <Link to={`/solutions/${row.id}`}>Open</Link>
          <Popconfirm
            title="Delete this solution?"
            okText="Delete"
            onConfirm={() => remove(row.id).catch(() => message.error("Could not delete the solution."))}
          >
            <Button type="link" danger size="small">Delete</Button>
          </Popconfirm>
        </Flex>
      ),
    },
  ];

  return (
    <Flex vertical gap={16}>
      <Typography.Title style={{ marginTop: 0 }}>History</Typography.Title>
      {error && <Typography.Text type="danger">{error}</Typography.Text>}
      <Table
        rowKey="id"
        loading={loading}
        columns={columns}
        dataSource={items}
        pagination={{ pageSize: 10, hideOnSinglePage: true }}
        scroll={{ x: true }}
        locale={{ emptyText: <Empty description="No solutions yet. Solve a system to see it here." /> }}
      />
    </Flex>
  );
}
