function SolutionExplanation({ steps }) {
    if (!steps || steps.length === 0) {
        return null;
    }

    const getStepIcon = (type) => {
        switch (type) {
            case "PROCESS_SELECTION":
                return "▶";

            case "PREEMPTION":
                return "⚡";

            case "CONTEXT_SWITCH":
                return "↪";

            case "CPU_IDLE":
                return "⏸";

            case "PROCESS_COMPLETION":
                return "✓";

            case "INTRODUCTION":
                return "🧠";

            default:
                return "•";
        }
    };

    const getStepClass = (type) => {
        switch (type) {
            case "PREEMPTION":
                return "solution-step preemption";

            case "CPU_IDLE":
                return "solution-step idle";

            case "PROCESS_COMPLETION":
                return "solution-step completion";

            case "CONTEXT_SWITCH":
                return "solution-step switch";

            case "INTRODUCTION":
                return "solution-step introduction";

            default:
                return "solution-step";
        }
    };

    return (
        <section className="solution-card">

            {/* HEADER */}
            <div className="section-header">

                <div>
                    <p className="section-label">
                        STEP-BY-STEP SOLUTION
                    </p>

                    <h2>
                        🧠 How This Problem Was Solved
                    </h2>

                    <p className="solution-subtitle">
                        Understand why the scheduler makes
                        each decision.
                    </p>
                </div>

                <div className="solution-count">
                    {steps.length}{" "}
                    {steps.length === 1
                        ? "Step"
                        : "Steps"}
                </div>

            </div>

            {/* TIMELINE */}
            <div className="solution-timeline">

                {steps.map((step, index) => (

                    <div
                        className={getStepClass(step.type)}
                        key={`${step.time}-${index}`}
                    >

                        {/* TIMELINE MARKER */}
                        <div className="solution-marker">
                            <span>
                                {getStepIcon(step.type)}
                            </span>
                        </div>

                        {/* CONTENT */}
                        <div className="solution-content">

                            {/* STEP + TIME */}
                            <div className="solution-step-top">

                                <div className="solution-step-number">
                                    STEP {step.step}
                                </div>

                                <div className="solution-time">
                                    Time {step.time}
                                </div>

                            </div>

                            {/* TITLE */}
                            <h3>
                                {step.title}
                            </h3>

                            {/* EXPLANATION */}
                            <div className="solution-reason">

                                <p className="solution-reason-label">
                                    WHY?
                                </p>

                                <p className="solution-explanation">
                                    {step.explanation}
                                </p>

                            </div>

                        </div>

                    </div>

                ))}

            </div>

        </section>
    );
}

export default SolutionExplanation;