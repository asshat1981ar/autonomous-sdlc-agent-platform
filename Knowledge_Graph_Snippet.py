
# Neo4j interaction example
from neo4j import GraphDatabase

def create_agent(tx, agent_id, capabilities):
    tx.run("MERGE (a:Agent {id: $agent_id}) "
           "SET a.capabilities = $capabilities",
           agent_id=agent_id, capabilities=capabilities)

def update_agent_capabilities(tx, agent_id, new_capabilities):
    tx.run("MATCH (a:Agent {id: $agent_id}) "
           "SET a.capabilities = $new_capabilities",
           agent_id=agent_id, new_capabilities=new_capabilities)

def record_task_assignment(tx, agent_id, task_id, status):
    tx.run(
        "MERGE (t:Task {id: $task_id}) "
        "MERGE (a:Agent {id: $agent_id}) "
        "MERGE (a)-[r:ASSIGNED_TO]->(t) "
        "SET r.status = $status, r.timestamp = datetime()",
        agent_id=agent_id, task_id=task_id, status=status
    )

def get_agent_performance(tx, agent_id):
    result = tx.run(
        "MATCH (a:Agent {id: $agent_id})-[r:ASSIGNED_TO]->(t:Task) "
        "RETURN r.status AS status, count(*) AS count "
        "GROUP BY r.status",
        agent_id=agent_id
    )
    return {record["status"]: record["count"] for record in result}

with GraphDatabase.driver("neo4j://localhost:7687", auth=("user", "password")) as driver:
    with driver.session() as session:
        try:
            session.execute_write(create_agent, "agent-123", ["coding", "testing"])
            session.execute_write(update_agent_capabilities, "agent-123", ["coding", "testing", "debugging"])
            session.execute_write(record_task_assignment, "agent-123", "task-456", "completed")
            performance = session.execute_read(get_agent_performance, "agent-123")
            print(f"Agent performance: {performance}")
        except Exception as e:
            print(f"Error interacting with Neo4j: {e}")
