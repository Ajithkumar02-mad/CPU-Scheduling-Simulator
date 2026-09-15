import { useEffect, useMemo, useState } from "react";

function SimulationAnimation({ result }) {
    const [currentTime, setCurrentTime] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [speed, setSpeed] = useState(700);

    const ganttChart = result?.gantt_chart || [];
    const processes = result?.processes || [];

    const startTime =
        ganttChart.length > 0
            ? ganttChart[0].start
            : 0;

    const endTime =
        ganttChart.length > 0
            ? ganttChart[ganttChart.length - 1].end
            : 0;


    // ========================================================
    // RESET WHEN RESULT CHANGES
    // ========================================================

    useEffect(() => {
        setCurrentTime(startTime);
        setIsPlaying(false);
    }, [result, startTime]);


    // ========================================================
    // CURRENT SEGMENT
    // ========================================================

    const currentSegment = useMemo(() => {
        if (
            currentTime === null ||
            ganttChart.length === 0
        ) {
            return null;
        }

        return ganttChart.find(
            (segment) =>
                currentTime >= segment.start &&
                currentTime < segment.end
        ) || null;

    }, [currentTime, ganttChart]);


    // ========================================================
    // PREVIOUS SEGMENT
    // ========================================================

    const previousSegment = useMemo(() => {
        if (!currentSegment) {
            return null;
        }

        const index =
            ganttChart.indexOf(currentSegment);

        return index > 0
            ? ganttChart[index - 1]
            : null;

    }, [currentSegment, ganttChart]);


    // ========================================================
    // CURRENT PROCESS
    // ========================================================

    const runningProcess =
        currentSegment?.process !== "IDLE"
            ? currentSegment?.process
            : null;


    // ========================================================
    // PROCESS INFORMATION
    // ========================================================

    const runningProcessData =
        processes.find(
            (process) =>
                process.id === runningProcess
        );


    // ========================================================
    // READY PROCESSES
    // ========================================================

    const readyProcesses = processes.filter(
        (process) => {

            if (currentTime === null) {
                return false;
            }

            const arrived =
                process.arrival_time <= currentTime;

            const completed =
                process.completion_time <= currentTime;

            return (
                arrived &&
                !completed &&
                process.id !== runningProcess
            );
        }
    );


    // ========================================================
    // EXPLANATION
    // ========================================================

    const explanation = useMemo(() => {

        if (!currentSegment) {
            return {
                title: "Simulation Ready",
                text: "Press Play to start the CPU simulation."
            };
        }


        if (currentSegment.process === "IDLE") {
            return {
                title: "CPU is Idle",
                text:
                    `No process is available at time ${currentTime}. ` +
                    `The CPU will remain idle until the next process arrives.`
            };
        }


        if (
            previousSegment &&
            previousSegment.process !==
                currentSegment.process
        ) {

            const previousProcess =
                processes.find(
                    (process) =>
                        process.id ===
                        previousSegment.process
                );


            if (
                previousProcess &&
                runningProcessData
            ) {

                if (
                    result.algorithm ===
                        "PRIORITY_PREEMPTIVE" &&
                    runningProcessData.priority <
                        previousProcess.priority
                ) {

                    return {
                        title:
                            `${runningProcessData.id} preempted ${previousProcess.id}`,
                        text:
                            `${runningProcessData.id} has higher priority ` +
                            `(${runningProcessData.priority}) than ` +
                            `${previousProcess.id} ` +
                            `(${previousProcess.priority}). ` +
                            `Smaller priority number means higher priority.`
                    };
                }


                if (
                    result.algorithm ===
                        "SRTF"
                ) {

                    return {
                        title:
                            `${runningProcessData.id} selected`,
                        text:
                            `${runningProcessData.id} has the shortest ` +
                            `remaining execution time among the available processes.`
                    };
                }


                if (
                    result.algorithm ===
                        "SJF"
                ) {

                    return {
                        title:
                            `${runningProcessData.id} selected`,
                        text:
                            `${runningProcessData.id} has the shortest ` +
                            `burst time among the available processes.`
                    };
                }


                if (
                    result.algorithm ===
                        "ROUND_ROBIN"
                ) {

                    return {
                        title:
                            `${runningProcessData.id} gets CPU`,
                        text:
                            `The previous process completed its time slice ` +
                            `or finished execution. The next ready process gets the CPU.`
                    };
                }


                if (
                    result.algorithm ===
                        "PRIORITY_NON_PREEMPTIVE"
                ) {

                    return {
                        title:
                            `${runningProcessData.id} selected`,
                        text:
                            `${runningProcessData.id} has the highest priority ` +
                            `among the processes available at this point.`
                    };
                }
            }
        }


        if (currentTime === startTime) {

            return {
                title:
                    `${runningProcessData?.id || "Process"} starts`,
                text:
                    `The first available process is selected by ` +
                    `${result.algorithm}.`
            };
        }


        return {
            title:
                `${runningProcessData?.id || "Process"} is running`,
            text:
                `${runningProcessData?.id || "The process"} ` +
                `is currently executing on the CPU.`
        };

    }, [
        currentSegment,
        previousSegment,
        currentTime,
        processes,
        runningProcessData,
        result.algorithm,
        startTime
    ]);


    // ========================================================
    // PLAYBACK
    // ========================================================

    useEffect(() => {

        if (
            !isPlaying ||
            currentTime === null
        ) {
            return;
        }

        if (currentTime >= endTime) {
            setIsPlaying(false);
            return;
        }

        const timer = setTimeout(() => {

            setCurrentTime(
                (time) => time + 1
            );

        }, speed);

        return () =>
            clearTimeout(timer);

    }, [
        isPlaying,
        currentTime,
        endTime,
        speed
    ]);


    // ========================================================
    // PLAY / PAUSE
    // ========================================================

    const togglePlayback = () => {

        if (currentTime >= endTime) {
            setCurrentTime(startTime);
            setIsPlaying(true);
            return;
        }

        setIsPlaying(
            (playing) => !playing
        );
    };


    // ========================================================
    // RESET
    // ========================================================

    const resetPlayback = () => {
        setCurrentTime(startTime);
        setIsPlaying(false);
    };


    if (
        !result ||
        ganttChart.length === 0
    ) {
        return null;
    }


    const progress =
        endTime > startTime
            ? (
                (currentTime - startTime) /
                (endTime - startTime)
            ) * 100
            : 0;


    return (
        <section className="animation-card">

            {/* ==================================================
                HEADER
                ================================================== */}

            <div className="section-header">

                <div>

                    <p className="section-label">
                        LIVE SIMULATION
                    </p>

                    <h2>
                        CPU Playback
                    </h2>

                </div>


                <div className="simulation-time">

                    Time:{" "}

                    <strong>
                        {currentTime}
                    </strong>

                    {" / "}

                    {endTime}

                </div>

            </div>


            {/* ==================================================
                CPU + READY QUEUE
                ================================================== */}

            <div className="simulation-monitor">

                {/* CPU */}

                <div className="cpu-monitor">

                    <p className="monitor-label">
                        CPU
                    </p>

                    <div
                        className={`cpu-box ${
                            runningProcess
                                ? "running"
                                : "idle"
                        }`}
                    >

                        <span className="cpu-icon">
                            CPU
                        </span>

                        <strong>
                            {runningProcess ||
                                "IDLE"}
                        </strong>

                        <small>
                            {runningProcess
                                ? "RUNNING"
                                : "CPU IDLE"}
                        </small>

                    </div>

                </div>


                {/* READY QUEUE */}

                <div className="ready-queue">

                    <p className="monitor-label">
                        READY PROCESSES
                    </p>

                    <div className="queue-list">

                        {readyProcesses.length === 0 ? (

                            <span className="queue-empty">
                                Queue Empty
                            </span>

                        ) : (

                            readyProcesses.map(
                                (process) => (
                                    <span
                                        className="queue-process"
                                        key={process.id}
                                    >
                                        {process.id}
                                    </span>
                                )
                            )

                        )}

                    </div>

                </div>

            </div>


            {/* ==================================================
                EXPLANATION
                ================================================== */}

            <div className="simulation-explanation">

                <div className="explanation-icon">
                    ?
                </div>

                <div>

                    <p className="explanation-label">
                        SCHEDULER DECISION
                    </p>

                    <h3>
                        {explanation.title}
                    </h3>

                    <p>
                        {explanation.text}
                    </p>

                </div>

            </div>


            {/* ==================================================
                PROGRESS
                ================================================== */}

            <div className="simulation-progress">

                <div className="progress-header">

                    <span>
                        Simulation Progress
                    </span>

                    <span>
                        {currentTime -
                            startTime}{" "}
                        /{" "}
                        {endTime -
                            startTime}
                    </span>

                </div>


                <div className="progress-track">

                    <div
                        className="progress-fill"
                        style={{
                            width:
                                `${Math.max(
                                    0,
                                    Math.min(
                                        100,
                                        progress
                                    )
                                )}%`,
                        }}
                    />

                </div>

            </div>


            {/* ==================================================
                CONTROLS
                ================================================== */}

            <div className="playback-controls">

                <button
                    className="play-button"
                    onClick={
                        togglePlayback
                    }
                >
                    {isPlaying
                        ? "❚❚ Pause"
                        : "▶ Play"}
                </button>


                <button
                    className="control-button"
                    onClick={
                        resetPlayback
                    }
                >
                    ↻ Reset
                </button>


                <label className="speed-control">

                    Speed

                    <select
                        value={speed}
                        onChange={(event) =>
                            setSpeed(
                                Number(
                                    event.target.value
                                )
                            )
                        }
                    >

                        <option value="1200">
                            Slow
                        </option>

                        <option value="700">
                            Normal
                        </option>

                        <option value="300">
                            Fast
                        </option>

                        <option value="100">
                            Very Fast
                        </option>

                    </select>

                </label>

            </div>

        </section>
    );
}

export default SimulationAnimation;