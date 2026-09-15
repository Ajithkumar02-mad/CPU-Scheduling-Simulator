import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";


function PerformanceCharts({ processes }) {

    if (!processes || processes.length === 0) {
        return null;
    }


    const waitingData = processes.map((process) => ({
        process: process.id,
        value: process.waiting_time,
    }));


    const turnaroundData = processes.map((process) => ({
        process: process.id,
        value: process.turnaround_time,
    }));


    return (
        <div className="charts-section">

            {/* ==================================================
                WAITING TIME
                ================================================== */}

            <div className="chart-card">

                <div className="chart-header">

                    <div>
                        <p className="result-label">
                            WAITING TIME
                        </p>

                        <h3>
                            Waiting Time by Process
                        </h3>
                    </div>

                </div>


                <div className="chart-container">

                    <ResponsiveContainer
                        width="100%"
                        height={300}
                    >

                        <BarChart
                            data={waitingData}
                            margin={{
                                top: 10,
                                right: 20,
                                left: 0,
                                bottom: 5,
                            }}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="var(--border)"
                            />

                            <XAxis
                                dataKey="process"
                                stroke="var(--text-muted)"
                            />

                            <YAxis
                                stroke="var(--text-muted)"
                            />

                            <Tooltip
                                contentStyle={{
                                    background:
                                        "var(--surface)",
                                    border:
                                        "1px solid var(--border)",
                                    borderRadius:
                                        "8px",
                                    color:
                                        "var(--text)",
                                }}
                            />

                            <Bar
                                dataKey="value"
                                name="Waiting Time"
                                fill="#5eead4"
                                radius={[5, 5, 0, 0]}
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </div>

            </div>


            {/* ==================================================
                TURNAROUND TIME
                ================================================== */}

            <div className="chart-card">

                <div className="chart-header">

                    <div>
                        <p className="result-label">
                            TURNAROUND TIME
                        </p>

                        <h3>
                            Turnaround Time by Process
                        </h3>
                    </div>

                </div>


                <div className="chart-container">

                    <ResponsiveContainer
                        width="100%"
                        height={300}
                    >

                        <BarChart
                            data={turnaroundData}
                            margin={{
                                top: 10,
                                right: 20,
                                left: 0,
                                bottom: 5,
                            }}
                        >

                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="var(--border)"
                            />

                            <XAxis
                                dataKey="process"
                                stroke="var(--text-muted)"
                            />

                            <YAxis
                                stroke="var(--text-muted)"
                            />

                            <Tooltip
                                contentStyle={{
                                    background:
                                        "var(--surface)",
                                    border:
                                        "1px solid var(--border)",
                                    borderRadius:
                                        "8px",
                                    color:
                                        "var(--text)",
                                }}
                            />

                            <Bar
                                dataKey="value"
                                name="Turnaround Time"
                                fill="#5eead4"
                                radius={[5, 5, 0, 0]}
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </div>

            </div>

        </div>
    );
}

export default PerformanceCharts;