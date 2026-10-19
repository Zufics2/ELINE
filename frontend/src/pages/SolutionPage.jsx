import { useEffect, useState } from "react";
import { Result, Spin, Typography } from "antd";
import { Link, useParams } from "react-router-dom";
import { errorMessage, fetchSolution } from "../api/client";
import SolutionView from "../components/SolutionView";

export default function SolutionPage() {
  const { id } = useParams();
  const [solution, setSolution] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setSolution(null);
    setError(null);
    fetchSolution(id).then(setSolution).catch((e) => setError(errorMessage(e)));
  }, [id]);

  if (error) return <Result status="404" title="Solution not found" subTitle={error} extra={<Link to="/history">Back to history</Link>} />;
  if (!solution) return <Spin />;
  return (
    <>
      <Typography.Title style={{ marginTop: 0 }}>Solution #{solution.id}</Typography.Title>
      <SolutionView solution={solution} />
    </>
  );
}
