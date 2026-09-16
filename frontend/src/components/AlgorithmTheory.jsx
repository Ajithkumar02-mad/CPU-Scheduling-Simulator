import algorithmTheory from "../data/algorithmTheory";
import "./AlgorithmTheory.css";

function AlgorithmTheory() {
    const algorithms = Object.values(algorithmTheory);

    const scrollToAlgorithm = (id) => {
        document.getElementById(id)?.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
    };

    return (
        <section className="theory-section" id="theory">

            {/* =====================================================
                THEORY HEADER
            ===================================================== */}

            <div className="theory-header">
                <p className="section-label">
                    CPU SCHEDULING THEORY
                </p>

                <h2>
                    Learn All 6 Scheduling Algorithms
                </h2>

                <p>
                    Beginner-friendly explanations, worked examples,
                    step-by-step solutions, formulas and exam tips.
                </p>
            </div>


            {/* =====================================================
                THEORY NAVIGATION
            ===================================================== */}

            <div className="theory-navigation">

                {algorithms.map((algorithm) => (
                    <button
                        key={algorithm.id}
                        className="theory-nav-button"
                        onClick={() =>
                            scrollToAlgorithm(algorithm.id)
                        }
                    >
                        {algorithm.shortName}
                    </button>
                ))}

            </div>


            {/* =====================================================
                ALGORITHM THEORY CARDS
            ===================================================== */}

            <div className="theory-content">

                {algorithms.map((algorithm, index) => (

                    <article
                        key={algorithm.id}
                        id={algorithm.id}
                        className="theory-card"
                    >

                        {/* -------------------------------------------------
                            TITLE
                        ------------------------------------------------- */}

                        <div className="theory-card-header">

                            <div className="theory-number">
                                {String(index + 1).padStart(2, "0")}
                            </div>

                            <div>
                                <p className="theory-label">
                                    ALGORITHM {index + 1}
                                </p>

                                <h3>
                                    {algorithm.name}
                                </h3>

                                <p className="theory-subtitle">
                                    {algorithm.subtitle}
                                </p>
                            </div>

                        </div>


                        {/* -------------------------------------------------
                            WHAT IS IT?
                        ------------------------------------------------- */}

                        <div className="theory-block">

                            <h4>
                                <span>01</span>
                                What is {algorithm.shortName}?
                            </h4>

                            <p className="theory-text">
                                {algorithm.whatIsIt}
                            </p>

                        </div>


                        {/* -------------------------------------------------
                            REAL WORLD ANALOGY
                        ------------------------------------------------- */}

                        <div className="theory-highlight">

                            <div className="highlight-icon">
                                💡
                            </div>

                            <div>

                                <h4>
                                    Think of it like this
                                </h4>

                                <p>
                                    {algorithm.analogy}
                                </p>

                            </div>

                        </div>


                        {/* -------------------------------------------------
                            HOW IT WORKS
                        ------------------------------------------------- */}

                        <div className="theory-block">

                            <h4>
                                <span>02</span>
                                How It Works
                            </h4>

                            <div className="step-list">

                                {algorithm.howItWorks.map(
                                    (step, stepIndex) => (

                                        <div
                                            className="theory-step"
                                            key={stepIndex}
                                        >

                                            <div className="step-number">
                                                {stepIndex + 1}
                                            </div>

                                            <p>
                                                {step}
                                            </p>

                                        </div>

                                    )
                                )}

                            </div>

                        </div>


                        {/* -------------------------------------------------
                            CHARACTERISTICS
                        ------------------------------------------------- */}

                        <div className="theory-grid">

                            <div className="info-panel">

                                <h4>
                                    📌 Characteristics
                                </h4>

                                <ul>

                                    {algorithm.characteristics.map(
                                        (item, itemIndex) => (

                                            <li key={itemIndex}>
                                                {item}
                                            </li>

                                        )
                                    )}

                                </ul>

                            </div>


                            {/* -------------------------------------------------
                                ADVANTAGES
                            ------------------------------------------------- */}

                            <div className="info-panel">

                                <h4>
                                    ✅ Advantages
                                </h4>

                                <ul>

                                    {algorithm.advantages.map(
                                        (item, itemIndex) => (

                                            <li key={itemIndex}>
                                                {item}
                                            </li>

                                        )
                                    )}

                                </ul>

                            </div>


                            {/* -------------------------------------------------
                                DISADVANTAGES
                            ------------------------------------------------- */}

                            <div className="info-panel">

                                <h4>
                                    ❌ Disadvantages
                                </h4>

                                <ul>

                                    {algorithm.disadvantages.map(
                                        (item, itemIndex) => (

                                            <li key={itemIndex}>
                                                {item}
                                            </li>

                                        )
                                    )}

                                </ul>

                            </div>

                        </div>


                        {/* -------------------------------------------------
                            FORMULAS
                        ------------------------------------------------- */}

                        <div className="theory-block">

                            <h4>
                                <span>03</span>
                                Important Formulas
                            </h4>

                            <div className="formula-list">

                                {algorithm.formulas.map(
                                    (formula, formulaIndex) => (

                                        <div
                                            className="formula-item"
                                            key={formulaIndex}
                                        >
                                            {formula}
                                        </div>

                                    )
                                )}

                            </div>

                        </div>


                        {/* =================================================
                            WORKED EXAMPLE
                        ================================================= */}

                        <div className="example-section">

                            <div className="example-header">

                                <div>

                                    <p className="theory-label">
                                        WORKED PROBLEM
                                    </p>

                                    <h4>
                                        {algorithm.example.title}
                                    </h4>

                                </div>

                                {algorithm.example.timeQuantum && (
                                    <div className="quantum-badge">
                                        Time Quantum:{" "}
                                        {algorithm.example.timeQuantum}
                                    </div>
                                )}

                            </div>


                            {/* ---------------------------------------------
                                NOTE
                            --------------------------------------------- */}

                            {algorithm.example.note && (

                                <div className="example-note">
                                    <strong>Note:</strong>{" "}
                                    {algorithm.example.note}
                                </div>

                            )}


                            {/* ---------------------------------------------
                                PROCESS TABLE
                            --------------------------------------------- */}

                            <div className="example-table-wrapper">

                                <table className="example-table">

                                    <thead>
                                        <tr>
                                            <th>Process</th>
                                            <th>Arrival Time</th>
                                            <th>Burst Time</th>

                                            {algorithm.example.processes.some(
                                                (process) =>
                                                    process.priority !==
                                                    undefined
                                            ) && (
                                                <th>Priority</th>
                                            )}
                                        </tr>
                                    </thead>

                                    <tbody>

                                        {algorithm.example.processes.map(
                                            (process) => (

                                                <tr key={process.id}>

                                                    <td>
                                                        <strong>
                                                            {process.id}
                                                        </strong>
                                                    </td>

                                                    <td>
                                                        {process.arrival}
                                                    </td>

                                                    <td>
                                                        {process.burst}
                                                    </td>

                                                    {algorithm.example.processes.some(
                                                        (item) =>
                                                            item.priority !==
                                                            undefined
                                                    ) && (
                                                        <td>
                                                            {process.priority}
                                                        </td>
                                                    )}

                                                </tr>

                                            )
                                        )}

                                    </tbody>

                                </table>

                            </div>


                            {/* ---------------------------------------------
                                STEP-BY-STEP SOLUTION
                            --------------------------------------------- */}

                            <div className="solution-area">

                                <h5>
                                    Step-by-Step Solution
                                </h5>

                                <div className="solution-steps">

                                    {algorithm.example.steps.map(
                                        (step, stepIndex) => (

                                            <div
                                                className="solution-step"
                                                key={stepIndex}
                                            >

                                                <div className="solution-step-number">
                                                    Step {stepIndex + 1}
                                                </div>

                                                <p>
                                                    {step}
                                                </p>

                                            </div>

                                        )
                                    )}

                                </div>

                            </div>


                            {/* ---------------------------------------------
                                GANTT CHART
                            --------------------------------------------- */}

                            <div className="example-gantt">

                                <h5>
                                    Gantt Chart
                                </h5>

                                <div className="gantt-example-box">
                                    {algorithm.example.gantt}
                                </div>

                            </div>


                            {/* ---------------------------------------------
                                CALCULATIONS
                            --------------------------------------------- */}

                            <div className="calculation-area">

                                <h5>
                                    Final Calculations
                                </h5>

                                <div className="calculation-list">

                                    {algorithm.example.calculations.map(
                                        (calculation, calculationIndex) => (

                                            <div
                                                className="calculation-item"
                                                key={calculationIndex}
                                            >

                                                <span>
                                                    {calculationIndex + 1}
                                                </span>

                                                <p>
                                                    {calculation}
                                                </p>

                                            </div>

                                        )
                                    )}

                                </div>

                            </div>

                        </div>


                        {/* -------------------------------------------------
                            EXAM TIPS
                        ------------------------------------------------- */}

                        <div className="exam-tips">

                            <div className="exam-tips-title">
                                🎯 Exam Tips
                            </div>

                            <ul>

                                {algorithm.examTips.map(
                                    (tip, tipIndex) => (

                                        <li key={tipIndex}>
                                            {tip}
                                        </li>

                                    )
                                )}

                            </ul>

                        </div>


                        {/* -------------------------------------------------
                            BACK TO TOP
                        ------------------------------------------------- */}

                        <button
                            className="back-to-theory"
                            onClick={() =>
                                scrollToAlgorithm("theory")
                            }
                        >
                            ↑ Back to Algorithm Menu
                        </button>

                    </article>

                ))}

            </div>

        </section>
    );
}

export default AlgorithmTheory;