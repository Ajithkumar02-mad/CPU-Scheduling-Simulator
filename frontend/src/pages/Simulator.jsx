import { useState } from "react";
import ProcessTable from "../components/ProcessTable";
import GanttChart from "../components/GanttChart";
import ResultsTable from "../components/ResultsTable";
import PerformanceCharts from "../components/PerformanceCharts";
import SimulationAnimation from "../components/SimulationAnimation";
import SolutionExplanation from "../components/SolutionExplanation";
import { simulateScheduling } from "../services/api";

function Simulator() {
    const [algorithm, setAlgorithm] = useState("FCFS");

    const [darkMode, setDarkMode] = useState(true);

    const [processes, setProcesses] = useState([]);

    const [timeQuantum, setTimeQuantum] = useState(2);

    const [error, setError] = useState("");

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);


    // ========================================================
    // ADD PROCESS
    // ========================================================

    const addProcess = () => {
        const nextNumber =
            processes.length > 0
                ? Math.max(
                    ...processes.map((process) =>
                        Number(
                            process.id.replace("P", "")
                        )
                    )
                ) + 1
                : 1;

        const newProcess = {
            id: `P${nextNumber}`,
            arrival_time: 0,
            burst_time: 1,
            priority: 1,
        };

        setProcesses((currentProcesses) => [
            ...currentProcesses,
            newProcess,
        ]);

        setError("");
    };


    // ========================================================
    // UPDATE PROCESS
    // ========================================================

    const updateProcess = (
        processId,
        field,
        value
    ) => {
        const numericValue =
            value === ""
                ? ""
                : Number(value);

        setProcesses((currentProcesses) =>
            currentProcesses.map((process) =>
                process.id === processId
                    ? {
                        ...process,
                        [field]: numericValue,
                    }
                    : process
            )
        );

        setError("");
    };


    // ========================================================
    // DELETE PROCESS
    // ========================================================

    const deleteProcess = (processId) => {
        setProcesses((currentProcesses) =>
            currentProcesses.filter(
                (process) =>
                    process.id !== processId
            )
        );

        setError("");
    };


    // ========================================================
    // RESET PROCESSES
    // ========================================================

    const resetProcesses = () => {
        setProcesses([]);
        setError("");
    };


    // ========================================================
    // ALGORITHM CHANGE
    // ========================================================

    const handleAlgorithmChange = (value) => {
        setAlgorithm(value);
        setError("");
    };


    // ========================================================
    // VALIDATE INPUT
    // ========================================================

    const validateInputs = () => {
        if (processes.length === 0) {
            return "Add at least one process.";
        }

        for (const process of processes) {
            if (
                process.arrival_time === "" ||
                !Number.isInteger(
                    process.arrival_time
                ) ||
                process.arrival_time < 0
            ) {
                return `${process.id}: Arrival time must be a non-negative integer.`;
            }

            if (
                process.burst_time === "" ||
                !Number.isInteger(
                    process.burst_time
                ) ||
                process.burst_time <= 0
            ) {
                return `${process.id}: Burst time must be greater than 0.`;
            }

            if (
                process.priority === "" ||
                !Number.isInteger(
                    process.priority
                )
            ) {
                return `${process.id}: Priority must be an integer.`;
            }
        }

        if (algorithm === "ROUND_ROBIN") {
            if (
                timeQuantum === "" ||
                !Number.isInteger(timeQuantum) ||
                timeQuantum <= 0
            ) {
                return "Time Quantum must be a positive integer.";
            }
        }

        return "";
    };


    // ========================================================
    // RUN SIMULATION - TEMPORARY
    // ========================================================

    const handleRunSimulation = async () => {
    const validationError = validateInputs();

    if (validationError) {
        setError(validationError);
        return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
        const simulationData = {
            algorithm,
            processes,
        };

        if (algorithm === "ROUND_ROBIN") {
            simulationData.time_quantum = timeQuantum;
        }

        const simulationResult =
            await simulateScheduling(simulationData);

        setResult(simulationResult);

    } catch (error) {
        console.error(
            "Simulation failed:",
            error
        );

        const message =
            error.response?.data?.error ||
            "Unable to connect to the backend.";

        setError(message);

    } finally {
        setLoading(false);
    }
};


    const validationError =
        validateInputs();


    return (
        <main
            className={`simulator-page ${
                darkMode
                    ? "dark"
                    : "light"
            }`}
        >

            {/* ==================================================
                TOP BAR
            ================================================== */}

            <div className="top-bar">

                <div className="app-brand">
                    CPU SCHEDULER
                </div>

                <button
                    className="theme-toggle"
                    onClick={() =>
                        setDarkMode(
                            !darkMode
                        )
                    }
                >
                    {darkMode
                        ? "☀ Light Mode"
                        : "☾ Dark Mode"}
                </button>

            </div>


            {/* ==================================================
                HERO
            ================================================== */}

            <section className="hero-section">

                <div>

                    <p className="eyebrow">
                        OPERATING SYSTEM SIMULATION
                    </p>

                    <h1>
                        CPU Scheduling
                        <span> Simulator</span>
                    </h1>

                    <p className="hero-description">
                        Visualize CPU scheduling
                        algorithms, process execution
                        and performance metrics.
                    </p>

                </div>

                <div className="status-badge">

                    <span className="status-dot"></span>

                    Backend Connected

                </div>

            </section>


            {/* ==================================================
                ALGORITHM CONFIGURATION
            ================================================== */}

            <section className="configuration-card">

                <div className="section-header">

                    <div>

                        <p className="section-label">
                            SIMULATION CONFIGURATION
                        </p>

                        <h2>
                            Configure Scheduler
                        </h2>

                    </div>

                </div>


                <div className="configuration-grid">

                    {/* Algorithm */}

                    <div className="algorithm-control">

                        <label htmlFor="algorithm">
                            Scheduling Algorithm
                        </label>

                        <select
                            id="algorithm"
                            value={algorithm}
                            onChange={(event) =>
                                handleAlgorithmChange(
                                    event.target.value
                                )
                            }
                        >

                            <option value="FCFS">
                                FCFS
                            </option>

                            <option value="SJF">
                                SJF
                            </option>

                            <option value="SRTF">
                                SRTF
                            </option>

                            <option value="ROUND_ROBIN">
                                Round Robin
                            </option>

                            <option value="PRIORITY_NON_PREEMPTIVE">
                                Priority — Non-Preemptive
                            </option>

                            <option value="PRIORITY_PREEMPTIVE">
                                Priority — Preemptive
                            </option>

                        </select>

                    </div>


                    {/* Time Quantum */}

                    {algorithm === "ROUND_ROBIN" && (

                        <div className="algorithm-control">

                            <label htmlFor="timeQuantum">
                                Time Quantum
                            </label>

                            <input
                                id="timeQuantum"
                                type="number"
                                min="1"
                                step="1"
                                value={timeQuantum}
                                onChange={(event) => {
                                    const value =
                                        event.target.value;

                                    setTimeQuantum(
                                        value === ""
                                            ? ""
                                            : Number(value)
                                    );

                                    setError("");
                                }}
                            />

                            <span className="input-hint">
                                CPU time allocated to each
                                process per turn.
                            </span>

                        </div>

                    )}

                </div>


                <div className="algorithm-info">

                    <strong>
                        {algorithm ===
                        "PRIORITY_NON_PREEMPTIVE"
                            ? "Priority — Non-Preemptive"
                            : algorithm ===
                              "PRIORITY_PREEMPTIVE"
                            ? "Priority — Preemptive"
                            : algorithm}
                    </strong>

                    <p>
                        {algorithm === "FCFS" &&
                            "Processes execute in the order they arrive."}

                        {algorithm === "SJF" &&
                            "The shortest available process executes first."}

                        {algorithm === "SRTF" &&
                            "The process with the shortest remaining time gets the CPU."}

                        {algorithm === "ROUND_ROBIN" &&
                            "Each process receives CPU time according to the selected time quantum."}

                        {algorithm ===
                            "PRIORITY_NON_PREEMPTIVE" &&
                            "The highest-priority available process executes until completion."}

                        {algorithm ===
                            "PRIORITY_PREEMPTIVE" &&
                            "A higher-priority arriving process can preempt the currently running process."}
                    </p>

                </div>

            </section>


            {/* ==================================================
                PROCESS CONFIGURATION
            ================================================== */}

            <section className="process-card">

                <div className="section-header">

                    <div>

                        <p className="section-label">
                            PROCESS CONFIGURATION
                        </p>

                        <h2>
                            Processes
                        </h2>

                    </div>


                    <div className="process-actions">

                        <button
                            className="secondary-button"
                            onClick={addProcess}
                        >
                            + Add Process
                        </button>

                        {processes.length > 0 && (
                            <button
                                className="secondary-button danger-outline"
                                onClick={
                                    resetProcesses
                                }
                            >
                                Reset
                            </button>
                        )}

                    </div>

                </div>


                {processes.length === 0 ? (

                    <div className="empty-process-state">

                        <div className="empty-icon">
                            CPU
                        </div>

                        <h3>
                            No processes configured
                        </h3>

                        <p>
                            Add processes to start your
                            scheduling simulation.
                        </p>

                        <button
                            className="primary-button"
                            onClick={addProcess}
                        >
                            + Add First Process
                        </button>

                    </div>

                ) : (

                    <ProcessTable
                        processes={processes}
                        onUpdate={updateProcess}
                        onDelete={deleteProcess}
                    />

                )}

            </section>


            {/* ==================================================
                ERROR
            ================================================== */}

            {error && (

                <div className="validation-error">
                    <span>!</span>
                    {error}
                </div>

            )}


            {/* ==================================================
                RUN SIMULATION
            ================================================== */}

           <section className="run-section">

    <button
        className="run-button"
        onClick={handleRunSimulation}
        disabled={
            processes.length === 0 ||
            Boolean(validationError) ||
            loading
        }
    >
        {loading
            ? "⟳ Running Simulation..."
            : "▶ Run Simulation"}
    </button>

</section>


{/* ==================================================
    SIMULATION RESULT
    ================================================== */}

{result && (

    <section className="result-card">

        <div className="section-header">

            <div>

                <p className="section-label">
                    SIMULATION RESULT
                </p>

                <h2>
                    {result.algorithm}
                </h2>

            </div>

            <div className="result-success">
                ✓ Simulation Complete
            </div>

        </div>


        {/* Gantt Chart Preview */}

        <div className="result-section">

            <p className="result-label">
                CPU TIMELINE
            </p>

         <GanttChart
                ganttChart={result.gantt_chart}
         />

        </div>

        {/* ==================================================
            LIVE SIMULATION
            ================================================== */}

        <SimulationAnimation
            result={result}
        />

        {/* ==================================================
            PROCESS RESULTS
            ================================================== */}

        <div className="result-section">

            <p className="result-label">
                PROCESS RESULTS
            </p>

            <ResultsTable
                processes={result.processes}
            />

        </div>

        {/* Metrics */}

        <div className="metrics-grid">

            <div className="metric-card">
                <span>
                    Avg Waiting Time
                </span>

                <strong>
                    {result.metrics.average_waiting_time.toFixed(2)}
                </strong>
            </div>


            <div className="metric-card">
                <span>
                    Avg Turnaround Time
                </span>

                <strong>
                    {result.metrics.average_turnaround_time.toFixed(2)}
                </strong>
            </div>


            <div className="metric-card">
                <span>
                    Avg Response Time
                </span>

                <strong>
                    {result.metrics.average_response_time.toFixed(2)}
                </strong>
            </div>


            <div className="metric-card">
                <span>
                    CPU Utilization
                </span>

                <strong>
                    {result.metrics.cpu_utilization.toFixed(2)}%
                </strong>
            </div>


            <div className="metric-card">
                <span>
                    Throughput
                </span>

                <strong>
                    {result.metrics.throughput.toFixed(3)}
                </strong>
            </div>


            <div className="metric-card">
                <span>
                    Context Switches
                </span>

                <strong>
                    {result.metrics.context_switches}
                </strong>
            </div>

        </div>

        {/* ==================================================
            PERFORMANCE CHARTS
            ================================================== */}

        <div className="result-section">

            <p className="result-label">
                PERFORMANCE ANALYSIS
            </p>

            <PerformanceCharts
                processes={result.processes}
            />
            
            <SolutionExplanation
                steps={result.solution_steps}
            />

        </div>

    </section>

)}

        </main>
    );
}

export default Simulator;