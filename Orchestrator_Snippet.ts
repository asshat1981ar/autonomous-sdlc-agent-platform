
// TypeScript snippet for task orchestration
interface Task {
    id: string;
    type: string;
    payload: object;
}

async function routeTask(task: Task): Promise<void> {
    const suitableAgents = await getAgentsForTask(task.type);
    for (const agent of suitableAgents) {
        if (await sendTaskToAgent(agent, task)) {
            console.log(`Task ${task.id} routed successfully.`);
            return;
        }
    }
    console.error(`Failed to route task ${task.id}.`);
}
