function GanttChart({ ganttChart }) {
    if (!ganttChart || ganttChart.length === 0) {
        return null;
    }

    const startTime = ganttChart[0].start;
    const endTime = ganttChart[ganttChart.length - 1].end;
    const totalDuration = endTime - startTime;

    return (
        <div className="gantt-container">

            {/* Timeline blocks */}
            <div className="gantt-timeline">

                {ganttChart.map((segment, index) => {
                    const duration =
                        segment.end - segment.start;

                    const width =
                        (duration / totalDuration) * 100;

                    const isIdle =
                        segment.process === "IDLE";

                    return (
                        <div
                            key={`${segment.process}-${index}`}
                            className={`gantt-segment ${
                                isIdle ? "gantt-idle" : ""
                            }`}
                            style={{
                                width: `${width}%`,
                            }}
                        >
                            <strong>
                                {segment.process}
                            </strong>

                            <span>
                                {segment.start} → {segment.end}
                            </span>

                            <small>
                                {duration} unit
                                {duration !== 1 ? "s" : ""}
                            </small>
                        </div>
                    );
                })}

            </div>


            {/* Time scale */}
            <div className="gantt-scale">

                {ganttChart.map((segment, index) => (
                    <span
                        key={`time-${index}`}
                        style={{
                            width: `${
                                (
                                    (segment.end - segment.start) /
                                    totalDuration
                                ) * 100
                            }%`,
                        }}
                    >
                        {segment.start}
                    </span>
                ))}

                {/* Final time */}
                <span className="gantt-end-time">
                    {endTime}
                </span>

            </div>

        </div>
    );
}

export default GanttChart;