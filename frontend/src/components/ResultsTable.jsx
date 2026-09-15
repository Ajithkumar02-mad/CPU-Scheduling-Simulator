function ResultsTable({ processes }) {
    if (!processes || processes.length === 0) {
        return null;
    }

    return (
        <div className="results-table-wrapper">

            <table className="results-table">

                <thead>
                    <tr>
                        <th>Process</th>
                        <th>Arrival</th>
                        <th>Burst</th>
                        <th>Priority</th>
                        <th>Completion</th>
                        <th>Turnaround</th>
                        <th>Waiting</th>
                        <th>Response</th>
                        <th>State</th>
                    </tr>
                </thead>

                <tbody>

                    {processes.map((process) => (
                        <tr key={process.id}>

                            <td>
                                <span className="result-process-id">
                                    {process.id}
                                </span>
                            </td>

                            <td>
                                {process.arrival_time}
                            </td>

                            <td>
                                {process.burst_time}
                            </td>

                            <td>
                                {process.priority}
                            </td>

                            <td className="metric-value">
                                {process.completion_time}
                            </td>

                            <td className="metric-value">
                                {process.turnaround_time}
                            </td>

                            <td className="metric-value">
                                {process.waiting_time}
                            </td>

                            <td className="metric-value">
                                {process.response_time}
                            </td>

                            <td>
                                <span
                                    className={`state-badge ${
                                        process.state === "TERMINATED"
                                            ? "completed"
                                            : ""
                                    }`}
                                >
                                    {process.state}
                                </span>
                            </td>

                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
}

export default ResultsTable;