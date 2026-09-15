import axios from "axios";


// ============================================================
// API CONFIGURATION
// ============================================================

const API = axios.create({
    baseURL: "http://127.0.0.1:5000",
    headers: {
        "Content-Type": "application/json",
    },
});


// ============================================================
// HEALTH CHECK
// ============================================================

export const checkHealth = async () => {
    const response = await API.get("/api/health");

    return response.data;
};


// ============================================================
// GET AVAILABLE ALGORITHMS
// ============================================================

export const getAlgorithms = async () => {
    const response = await API.get("/api/algorithms");

    return response.data;
};


// ============================================================
// RUN CPU SCHEDULING SIMULATION
// ============================================================

export const simulateScheduling = async (simulationData) => {
    const response = await API.post(
        "/api/simulate",
        simulationData
    );

    return response.data;
};


// ============================================================
// EXPORT API INSTANCE
// ============================================================

export default API;