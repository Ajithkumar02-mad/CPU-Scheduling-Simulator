const algorithmTheory = {
    FCFS: {
        id: "fcfs-theory",
        shortName: "FCFS",
        name: "First Come, First Served",
        subtitle: "The process that arrives first gets the CPU first.",

        whatIsIt: `
            First Come, First Served (FCFS) is the simplest CPU scheduling
            algorithm. Processes are executed in the same order in which they
            arrive in the ready queue.

            FCFS is a non-preemptive scheduling algorithm. Once a process gets
            the CPU, it continues executing until its burst time is completed.
        `,

        analogy: `
            Think of people standing in a queue at a ticket counter.
            The person who comes first is served first, followed by the next
            person, and so on.

            CPU scheduling with FCFS works in a similar way.
        `,

        howItWorks: [
            "Check the arrival time of every process.",
            "Select the process that arrived first.",
            "Give the CPU to that process.",
            "Allow it to execute until completion.",
            "Select the next process according to arrival order.",
            "Continue until all processes are completed."
        ],

        characteristics: [
            "Non-preemptive",
            "Simple and easy to implement",
            "Processes are handled according to arrival order",
            "Uses a FIFO-style ready queue",
            "A long process can make shorter processes wait"
        ],

        advantages: [
            "Very simple scheduling logic",
            "Easy to understand and implement",
            "No starvation because every process eventually gets its turn",
            "Low scheduling overhead"
        ],

        disadvantages: [
            "Can produce a high average waiting time",
            "Suffers from the convoy effect",
            "Short processes may wait behind a long process",
            "Not ideal for interactive systems"
        ],

        formulas: [
            "Completion Time (CT) = Time at which process finishes",
            "Turnaround Time (TAT) = CT − Arrival Time",
            "Waiting Time (WT) = TAT − Burst Time",
            "Response Time (RT) = First Start Time − Arrival Time"
        ],

        example: {
            title: "FCFS Worked Example",
            processes: [
                { id: "P1", arrival: 0, burst: 5 },
                { id: "P2", arrival: 1, burst: 3 },
                { id: "P3", arrival: 2, burst: 2 }
            ],

            steps: [
                "At time 0, P1 has arrived, so P1 gets the CPU.",
                "P1 executes from time 0 to 5.",
                "During P1's execution, P2 and P3 arrive.",
                "At time 5, P1 is complete. P2 arrived before P3, so P2 executes next.",
                "P2 executes from time 5 to 8.",
                "Finally, P3 executes from time 8 to 10."
            ],

            gantt: "0 ───── P1 ───── 5 ─── P2 ─── 8 ── P3 ── 10",

            calculations: [
                "P1: CT = 5, TAT = 5 − 0 = 5, WT = 5 − 5 = 0",
                "P2: CT = 8, TAT = 8 − 1 = 7, WT = 7 − 3 = 4",
                "P3: CT = 10, TAT = 10 − 2 = 8, WT = 8 − 2 = 6",
                "Average Waiting Time = (0 + 4 + 6) / 3 = 3.33"
            ]
        },

        examTips: [
            "Always sort or reason about processes using arrival time.",
            "FCFS does not preempt the running process.",
            "If the CPU is idle, jump directly to the next arrival time.",
            "Remember: WT = TAT − BT."
        ]
    },

    SJF: {
        id: "sjf-theory",
        shortName: "SJF",
        name: "Shortest Job First",
        subtitle: "Among available processes, the one with the shortest burst time executes first.",

        whatIsIt: `
            Shortest Job First (SJF) selects the process with the smallest
            burst time from the processes that are currently available.

            The version covered here is non-preemptive. Once a process starts
            executing, it continues until it finishes.
        `,

        analogy: `
            Imagine a service desk where several customers are waiting.
            If the system wants to finish the maximum number of small tasks
            quickly, it may serve the customer with the smallest task first.
        `,

        howItWorks: [
            "Find the processes that have arrived.",
            "Look at the burst time of each available process.",
            "Select the process with the smallest burst time.",
            "Execute it completely.",
            "When it finishes, check the newly available processes.",
            "Again select the shortest available process.",
            "Continue until every process is completed."
        ],

        characteristics: [
            "Non-preemptive",
            "Uses burst time for scheduling decisions",
            "Only available processes can be selected",
            "Can reduce average waiting time",
            "Long processes may experience starvation"
        ],

        advantages: [
            "Often produces a low average waiting time",
            "Efficient for workloads where burst times are known",
            "Simple concept"
        ],

        disadvantages: [
            "Requires knowledge or estimation of burst time",
            "Long processes may wait for a long time",
            "Not suitable when burst time cannot be estimated accurately"
        ],

        formulas: [
            "TAT = CT − AT",
            "WT = TAT − BT",
            "RT = First Start Time − AT"
        ],

        example: {
            title: "SJF Worked Example",
            processes: [
                { id: "P1", arrival: 0, burst: 7 },
                { id: "P2", arrival: 2, burst: 4 },
                { id: "P3", arrival: 3, burst: 2 },
                { id: "P4", arrival: 4, burst: 1 }
            ],

            steps: [
                "At time 0, only P1 has arrived, so P1 must execute.",
                "P1 executes from 0 to 7.",
                "At time 7, P2, P3 and P4 are available.",
                "Their burst times are P2 = 4, P3 = 2 and P4 = 1.",
                "The shortest process is P4, so P4 executes from 7 to 8.",
                "Among the remaining processes, P3 has the shortest burst time, so it executes from 8 to 10.",
                "P2 is the only remaining process, so it executes from 10 to 14."
            ],

            gantt: "0 ─────── P1 ─────── 7 ─ P4 ─ 8 ── P3 ── 10 ─── P2 ─── 14",

            calculations: [
                "P1: CT = 7, TAT = 7 − 0 = 7, WT = 7 − 7 = 0",
                "P4: CT = 8, TAT = 8 − 4 = 4, WT = 4 − 1 = 3",
                "P3: CT = 10, TAT = 10 − 3 = 7, WT = 7 − 2 = 5",
                "P2: CT = 14, TAT = 14 − 2 = 12, WT = 12 − 4 = 8"
            ]
        },

        examTips: [
            "SJF considers only processes that have already arrived.",
            "It is non-preemptive, so a running process is not interrupted.",
            "Do not select a process that has not arrived yet.",
            "If multiple processes have the same burst time, use the defined tie-breaking rule."
        ]
    },

    SRTF: {
        id: "srtf-theory",
        shortName: "SRTF",
        name: "Shortest Remaining Time First",
        subtitle: "The process with the smallest remaining CPU time gets the CPU.",

        whatIsIt: `
            Shortest Remaining Time First (SRTF) is the preemptive version
            of Shortest Job First.

            The scheduler continuously checks the remaining burst time of
            available processes. If a newly arriving process has a smaller
            remaining time than the currently running process, the CPU can
            be given to the new process.
        `,

        analogy: `
            Imagine working on a task that needs 10 minutes. While working,
            someone gives you a new task that needs only 2 minutes.

            If the rule says "finish the shortest remaining task first",
            you may pause the 10-minute task and complete the 2-minute task.
        `,

        howItWorks: [
            "Start with the processes that have arrived.",
            "Select the process with the smallest remaining burst time.",
            "Run the selected process.",
            "Whenever another process arrives, compare remaining times.",
            "If the new process has a shorter remaining time, preempt the current process.",
            "Continue until all processes finish."
        ],

        characteristics: [
            "Preemptive scheduling",
            "Uses remaining burst time",
            "Processes can be interrupted",
            "Can reduce average waiting time",
            "More context switches can occur"
        ],

        advantages: [
            "Usually performs well for short jobs",
            "Can provide low average waiting time",
            "Responds to newly arriving short processes"
        ],

        disadvantages: [
            "More complex than SJF",
            "Can cause many context switches",
            "Long processes may experience starvation",
            "Requires remaining-time tracking"
        ],

        formulas: [
            "TAT = CT − AT",
            "WT = TAT − BT",
            "RT = First Start Time − AT"
        ],

        example: {
            title: "SRTF Worked Example",
            processes: [
                { id: "P1", arrival: 0, burst: 8 },
                { id: "P2", arrival: 2, burst: 3 },
                { id: "P3", arrival: 4, burst: 1 }
            ],

            steps: [
                "At time 0, only P1 is available, so P1 starts.",
                "P1 runs from 0 to 2. Its remaining time becomes 6.",
                "At time 2, P2 arrives with burst time 3.",
                "P2 has 3 units remaining while P1 has 6, so P1 is preempted.",
                "P2 runs from 2 to 4. Its remaining time becomes 1.",
                "At time 4, P3 arrives with burst time 1.",
                "P2 and P3 both have 1 unit remaining. Apply the tie-breaking rule.",
                "After the selected process finishes, continue with the shortest remaining process.",
                "Eventually P1 completes after the shorter processes finish."
            ],

            gantt: "0 ─ P1 ─ 2 ─ P2 ─ 4 ─ P3 ─ 5 ─ P2 ─ 6 ───── P1 ───── 12",

            calculations: [
                "Calculate completion time from the final execution point of each process.",
                "TAT = Completion Time − Arrival Time.",
                "WT = Turnaround Time − Burst Time.",
                "RT = First Start Time − Arrival Time."
            ]
        },

        examTips: [
            "Always compare REMAINING time, not original burst time.",
            "A newly arriving process can cause preemption.",
            "Check the ready processes whenever an arrival occurs.",
            "Keep track of every execution segment."
        ]
    },

    ROUND_ROBIN: {
        id: "round-robin-theory",
        shortName: "Round Robin",
        name: "Round Robin Scheduling",
        subtitle: "Each process receives a limited CPU time called a time quantum.",

        whatIsIt: `
            Round Robin is a preemptive scheduling algorithm designed mainly
            for time-sharing systems.

            Every ready process gets the CPU for a fixed amount of time called
            the time quantum. If the process does not finish during its
            quantum, it is moved back into the ready queue.
        `,

        analogy: `
            Imagine several students sharing one computer. Each student gets
            the computer for 2 minutes. After 2 minutes, the next student gets
            a turn. If a student finishes early, they leave the queue.
        `,

        howItWorks: [
            "Place arrived processes into the ready queue.",
            "Select the first process in the queue.",
            "Run it for at most one time quantum.",
            "If it finishes, remove it from the queue.",
            "If it does not finish, reduce its remaining time and place it at the end of the queue.",
            "Add newly arrived processes according to the scheduling rules.",
            "Repeat until all processes are completed."
        ],

        characteristics: [
            "Preemptive",
            "Uses a FIFO ready queue",
            "Uses a time quantum",
            "Provides fair CPU sharing",
            "Suitable for interactive and time-sharing systems"
        ],

        advantages: [
            "Fair CPU allocation",
            "Good response for interactive processes",
            "No process can normally monopolize the CPU",
            "Easy to understand"
        ],

        disadvantages: [
            "Very small quantum can cause many context switches",
            "Very large quantum makes it behave similarly to FCFS",
            "Performance depends heavily on time quantum"
        ],

        formulas: [
            "TAT = CT − AT",
            "WT = TAT − BT",
            "RT = First Start Time − AT"
        ],

        example: {
            title: "Round Robin Worked Example",
            timeQuantum: 2,

            processes: [
                { id: "P1", arrival: 0, burst: 5 },
                { id: "P2", arrival: 0, burst: 3 },
                { id: "P3", arrival: 0, burst: 4 }
            ],

            steps: [
                "All three processes are available at time 0.",
                "Queue: P1 → P2 → P3.",
                "P1 executes for 2 units: remaining time = 3.",
                "P1 goes to the end of the queue.",
                "P2 executes for 2 units: remaining time = 1.",
                "P2 goes to the end of the queue.",
                "P3 executes for 2 units: remaining time = 2.",
                "P3 goes to the end of the queue.",
                "P1 executes for 2 units: remaining time = 1.",
                "P2 executes for its remaining 1 unit and completes.",
                "P3 executes for its remaining 2 units and completes.",
                "P1 executes for its remaining 1 unit and completes."
            ],

            gantt: "0─P1─2─P2─4─P3─6─P1─8─P2─9─P3─11─P1─12",

            calculations: [
                "P1 completes at 12: TAT = 12 − 0 = 12, WT = 12 − 5 = 7.",
                "P2 completes at 9: TAT = 9 − 0 = 9, WT = 9 − 3 = 6.",
                "P3 completes at 11: TAT = 11 − 0 = 11, WT = 11 − 4 = 7.",
                "Average Waiting Time = (7 + 6 + 7) / 3 = 6.67"
            ]
        },

        examTips: [
            "Always maintain the ready queue carefully.",
            "Remember to reduce remaining burst time after every quantum.",
            "If remaining time is less than the quantum, execute only the remaining time.",
            "The time quantum greatly affects performance."
        ]
    },

    PRIORITY_NON_PREEMPTIVE: {
        id: "priority-np-theory",
        shortName: "Priority NP",
        name: "Priority Scheduling — Non-Preemptive",
        subtitle: "The highest-priority available process runs until completion.",

        whatIsIt: `
            In non-preemptive Priority Scheduling, every process is assigned
            a priority value.

            When the CPU becomes available, the scheduler selects the
            highest-priority process among the processes that have already
            arrived.

            Once execution starts, the process continues until completion.
        `,

        analogy: `
            Imagine an emergency department. Patients are assigned priorities.
            When a doctor becomes available, the highest-priority waiting
            patient is selected.
        `,

        howItWorks: [
            "Check which processes have arrived.",
            "Compare their priority values.",
            "Select the highest-priority process.",
            "Run it until completion.",
            "When it finishes, check the available processes again.",
            "Repeat until all processes finish."
        ],

        characteristics: [
            "Non-preemptive",
            "Uses priority for scheduling",
            "A running process is not interrupted",
            "Priority convention must be clearly defined",
            "Starvation can occur"
        ],

        advantages: [
            "Important processes can be executed earlier",
            "Simple to implement",
            "Useful when tasks have different importance levels"
        ],

        disadvantages: [
            "Low-priority processes may wait for a long time",
            "Starvation is possible",
            "Priority values must be assigned carefully"
        ],

        formulas: [
            "TAT = CT − AT",
            "WT = TAT − BT",
            "RT = First Start Time − AT"
        ],

        example: {
            title: "Priority Non-Preemptive Worked Example",
            note: "Assume a smaller priority number means higher priority.",

            processes: [
                { id: "P1", arrival: 0, burst: 5, priority: 3 },
                { id: "P2", arrival: 1, burst: 3, priority: 1 },
                { id: "P3", arrival: 2, burst: 2, priority: 2 }
            ],

            steps: [
                "At time 0, only P1 has arrived, so P1 starts.",
                "P1 continues until completion because the algorithm is non-preemptive.",
                "P1 completes at time 5.",
                "At time 5, P2 and P3 are available.",
                "P2 has priority 1 and P3 has priority 2.",
                "Priority 1 is higher, so P2 executes from 5 to 8.",
                "P3 then executes from 8 to 10."
            ],

            gantt: "0 ───── P1 ───── 5 ─── P2 ─── 8 ── P3 ── 10",

            calculations: [
                "P1: CT = 5, TAT = 5 − 0 = 5, WT = 5 − 5 = 0",
                "P2: CT = 8, TAT = 8 − 1 = 7, WT = 7 − 3 = 4",
                "P3: CT = 10, TAT = 10 − 2 = 8, WT = 8 − 2 = 6"
            ]
        },

        examTips: [
            "Know whether smaller or larger priority number means higher priority.",
            "Always consider only arrived processes.",
            "Non-preemptive means a running process cannot be interrupted.",
            "Remember that starvation is possible."
        ]
    },

    PRIORITY_PREEMPTIVE: {
        id: "priority-p-theory",
        shortName: "Priority P",
        name: "Priority Scheduling — Preemptive",
        subtitle: "A newly arriving higher-priority process can interrupt the current process.",

        whatIsIt: `
            Preemptive Priority Scheduling assigns a priority to every process.
            The CPU is given to the highest-priority available process.

            Unlike non-preemptive Priority Scheduling, the currently running
            process can be interrupted when a higher-priority process arrives.
        `,

        analogy: `
            Imagine an emergency control room. An operator may be working on
            a normal task, but if a critical emergency arrives, the emergency
            task immediately receives attention.
        `,

        howItWorks: [
            "Check the processes that have arrived.",
            "Select the highest-priority available process.",
            "Start executing it.",
            "When a new process arrives, compare its priority with the current process.",
            "If the new process has higher priority, preempt the current process.",
            "Run the higher-priority process.",
            "Resume the preempted process when appropriate.",
            "Continue until every process completes."
        ],

        characteristics: [
            "Preemptive",
            "Uses priority for CPU selection",
            "Higher-priority arrivals can cause preemption",
            "Requires tracking remaining execution time",
            "Starvation can occur"
        ],

        advantages: [
            "Urgent tasks can receive CPU immediately",
            "Useful for priority-based systems",
            "More responsive than non-preemptive priority scheduling"
        ],

        disadvantages: [
            "Can cause many context switches",
            "Low-priority processes may starve",
            "More complex than non-preemptive priority scheduling"
        ],

        formulas: [
            "TAT = CT − AT",
            "WT = TAT − BT",
            "RT = First Start Time − AT"
        ],

        example: {
            title: "Priority Preemptive Worked Example",
            note: "Assume a smaller priority number means higher priority.",

            processes: [
                { id: "P1", arrival: 0, burst: 8, priority: 3 },
                { id: "P2", arrival: 2, burst: 3, priority: 1 },
                { id: "P3", arrival: 4, burst: 2, priority: 2 }
            ],

            steps: [
                "At time 0, P1 is the only available process, so P1 starts.",
                "P1 executes from time 0 to 2. It has 6 units remaining.",
                "At time 2, P2 arrives with priority 1.",
                "P2 has higher priority than P1, so P1 is preempted.",
                "P2 executes from time 2 to 5 and completes.",
                "At time 4, P3 arrives, but P2 has higher priority, so P2 continues.",
                "At time 5, P2 is complete. P3 and P1 are available.",
                "P3 has priority 2 while P1 has priority 3, so P3 executes.",
                "P3 completes at time 7.",
                "P1 resumes and completes its remaining 6 units from 7 to 13."
            ],

            gantt: "0 ─ P1 ─ 2 ─── P2 ─── 5 ── P3 ── 7 ────── P1 ────── 13",

            calculations: [
                "P1: CT = 13, TAT = 13 − 0 = 13, WT = 13 − 8 = 5",
                "P2: CT = 5, TAT = 5 − 2 = 3, WT = 3 − 3 = 0",
                "P3: CT = 7, TAT = 7 − 4 = 3, WT = 3 − 2 = 1",
                "Response time is calculated using the first time each process receives the CPU."
            ]
        },

        examTips: [
            "Check for newly arriving higher-priority processes.",
            "Preemption means the current process can be interrupted.",
            "Track the remaining burst time of preempted processes.",
            "Clearly identify the priority convention before solving."
        ]
    }
};

export default algorithmTheory;