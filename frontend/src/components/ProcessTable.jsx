function ProcessTable({
    processes,
    onUpdate,
    onDelete,
}) {
    return (
        <div className="process-table-wrapper">

            <table className="process-table">

                <thead>
                    <tr>
                        <th>Process</th>
                        <th>Arrival Time</th>
                        <th>Burst Time</th>
                        <th>Priority</th>
                        <th>Action</th>
                    </tr>
                </thead>

                <tbody>

                    {processes.map((process) => (
                        <tr key={process.id}>

                            <td>
                                <span className="process-id">
                                    {process.id}
                                </span>
                            </td>

                            <td>
                                <input
                                    type="number"
                                    min="0"
                                    value={process.arrival_time}
                                    onChange={(event) =>
                                        onUpdate(
                                            process.id,
                                            "arrival_time",
                                            event.target.value
                                        )
                                    }
                                />
                            </td>

                            <td>
                                <input
                                    type="number"
                                    min="1"
                                    value={process.burst_time}
                                    onChange={(event) =>
                                        onUpdate(
                                            process.id,
                                            "burst_time",
                                            event.target.value
                                        )
                                    }
                                />
                            </td>

                            <td>
                                <input
                                    type="number"
                                    value={process.priority}
                                    onChange={(event) =>
                                        onUpdate(
                                            process.id,
                                            "priority",
                                            event.target.value
                                        )
                                    }
                                />
                            </td>

                            <td>
                                <button
                                    className="delete-button"
                                    onClick={() =>
                                        onDelete(process.id)
                                    }
                                >
                                    Delete
                                </button>
                            </td>

                        </tr>
                    ))}

                </tbody>

            </table>

        </div>
    );
}

export default ProcessTable;