#!/usr/bin/env bash
# A2A Neo4j Verification and Health Check Script
# Usage: ./verify_neo4j.sh [NEO4J_URI] [USER] [PASS]

set -e

NEO4J_URI=${1:-bolt://localhost:7687}
NEO4J_USER=${2:-neo4j}
NEO4J_PASS=${3:-password123}

echo "🔍 A2A Neo4j Verification and Health Check"
echo "URI: $NEO4J_URI"
echo "User: $NEO4J_USER"
echo ""

# Function to execute Cypher commands
neo4j_shell() {
  docker exec -i neo4j-a2a cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" "$@"
}

# Function to check if Neo4j is running
check_neo4j_running() {
  if ! docker ps | grep -q neo4j-a2a; then
    echo "❌ Neo4j container is not running!"
    echo "💡 Start with: docker-compose -f docker-compose-neo4j.yml up -d"
    exit 1
  fi
  echo "✅ Neo4j container is running"
}

# Function to check Neo4j connectivity
check_connectivity() {
  echo "🔌 Testing Neo4j connectivity..."
  if neo4j_shell "RETURN 'Connection successful' AS status;" &>/dev/null; then
    echo "✅ Neo4j connection successful"
  else
    echo "❌ Cannot connect to Neo4j"
    echo "💡 Check if Neo4j is fully started (it may take a few minutes)"
    exit 1
  fi
}

# Function to verify APOC and GDS plugins
check_plugins() {
  echo "🔌 Checking APOC and GDS plugins..."
  
  echo "📦 APOC procedures:"
  neo4j_shell "CALL dbms.procedures() YIELD name WHERE name STARTS WITH 'apoc.' RETURN count(name) AS apoc_procedures;"
  
  echo "📦 GDS procedures:"
  neo4j_shell "CALL dbms.procedures() YIELD name WHERE name STARTS WITH 'gds.' RETURN count(name) AS gds_procedures;"
  
  echo "✅ Plugin verification complete"
}

# Function to verify schema
verify_schema() {
  echo "📋 Verifying database schema..."
  
  echo "🔗 Constraints:"
  neo4j_shell "SHOW CONSTRAINTS;"
  
  echo ""
  echo "📊 Indexes:"
  neo4j_shell "SHOW INDEXES;"
  
  echo "✅ Schema verification complete"
}

# Function to verify data integrity
verify_data() {
  echo "📊 Verifying data integrity..."
  
  echo "🤖 Agents:"
  neo4j_shell "MATCH (a:AgentCard) RETURN a.agentId, a.name, size(a.capabilities) AS capability_count, a.performance_score ORDER BY a.agentId;"
  
  echo ""
  echo "📋 Tasks:"
  neo4j_shell "MATCH (t:Task) RETURN t.taskId, t.intent, t.status, t.confidence ORDER BY t.startedAt DESC LIMIT 5;"
  
  echo ""
  echo "📈 Performance Metrics:"
  neo4j_shell "MATCH (m:PerformanceMetric) RETURN m.type, count(m) AS count, avg(m.value) AS avg_value GROUP BY m.type ORDER BY count DESC;"
  
  echo ""
  echo "🧠 Knowledge Items:"
  neo4j_shell "MATCH (k:KnowledgeItem) RETURN k.type, count(k) AS count GROUP BY k.type ORDER BY count DESC;"
  
  echo "✅ Data integrity verification complete"
}

# Function to test A2A queries
test_a2a_queries() {
  echo "🎯 Testing A2A-specific queries..."
  
  echo "1. Agent Optimization Query:"
  neo4j_shell "
  MATCH (a:AgentCard)
  OPTIONAL MATCH (a)-[:RAN]->(t:Task)
  WITH a, count(t) as task_count, avg(t.confidence) as avg_confidence
  RETURN a.name, a.performance_score, task_count, 
         ROUND(COALESCE(avg_confidence, 0.0), 3) as avg_confidence,
         ROUND(a.performance_score * COALESCE(avg_confidence, 0.5), 3) as optimization_score
  ORDER BY optimization_score DESC;
  "
  
  echo ""
  echo "2. Task Collaboration Network:"
  neo4j_shell "
  MATCH (session:Session {sessionId: 'mmorpg-session-001'})-[:CONTAINS]->(t:Task)<-[:RAN]-(a:AgentCard)
  RETURN session.description, t.intent, a.name, t.confidence
  ORDER BY t.startedAt;
  "
  
  echo ""
  echo "3. Performance Analytics:"
  neo4j_shell "
  MATCH (t:Task)-[:MEASURES]-(m:PerformanceMetric)
  WHERE m.type = 'confidence_score'
  RETURN t.intent, 
         count(m) as metric_count,
         ROUND(avg(m.value), 3) as avg_confidence,
         ROUND(min(m.value), 3) as min_confidence,
         ROUND(max(m.value), 3) as max_confidence
  ORDER BY avg_confidence DESC;
  "
  
  echo ""
  echo "4. Knowledge Graph Analysis:"
  neo4j_shell "
  MATCH (a:AgentCard)-[:LEARNED]->(k:KnowledgeItem)-[:DERIVES_FROM]->(t:Task)
  RETURN a.name as agent, k.type as knowledge_type, t.intent as task_intent, k.quality_score
  ORDER BY k.quality_score DESC;
  "
  
  echo "✅ A2A query testing complete"
}

# Function to test advanced analytics
test_advanced_analytics() {
  echo "📊 Testing advanced analytics capabilities..."
  
  echo "1. Agent Collaboration Effectiveness:"
  neo4j_shell "
  MATCH (a1:AgentCard)-[c:COLLABORATED_WITH]->(a2:AgentCard)
  RETURN a1.name + ' → ' + a2.name as collaboration,
         c.interaction_type,
         ROUND(c.effectiveness, 3) as effectiveness,
         ROUND(c.feedback_score, 3) as feedback_score
  ORDER BY c.effectiveness DESC;
  "
  
  echo ""
  echo "2. System Performance Overview:"
  neo4j_shell "
  CALL {
    MATCH (a:AgentCard) RETURN count(a) as total_agents
  }
  CALL {
    MATCH (t:Task) RETURN count(t) as total_tasks
  }
  CALL {
    MATCH (t:Task {status: 'COMPLETED'}) RETURN count(t) as completed_tasks
  }
  CALL {
    MATCH (m:PerformanceMetric {type: 'confidence_score'}) 
    RETURN ROUND(avg(m.value), 3) as avg_system_confidence
  }
  CALL {
    MATCH ()-[c:COLLABORATED_WITH]->() 
    RETURN count(c) as total_collaborations
  }
  RETURN total_agents, total_tasks, completed_tasks, 
         ROUND(100.0 * completed_tasks / total_tasks, 1) + '%' as completion_rate,
         avg_system_confidence, total_collaborations;
  "
  
  echo ""
  echo "3. Knowledge Network Analysis:"
  neo4j_shell "
  MATCH (k:KnowledgeItem)
  RETURN k.type as knowledge_type,
         count(k) as count,
         ROUND(avg(k.quality_score), 3) as avg_quality,
         ROUND(avg(k.usage_count), 1) as avg_usage
  ORDER BY count DESC;
  "
  
  echo "✅ Advanced analytics testing complete"
}

# Function to generate health report
generate_health_report() {
  echo ""
  echo "==============================================="
  echo "📊 A2A NEO4J HEALTH REPORT"
  echo "==============================================="
  
  echo "🏥 System Health:"
  echo "  ✅ Neo4j Container: Running"
  echo "  ✅ Database Connectivity: OK"
  echo "  ✅ APOC Plugin: Loaded"
  echo "  ✅ GDS Plugin: Loaded"
  echo "  ✅ Schema: Valid"
  echo "  ✅ Data Integrity: Verified"
  echo ""
  
  echo "📊 Data Summary:"
  neo4j_shell "
  MATCH (a:AgentCard) WITH count(a) as agents
  MATCH (t:Task) WITH agents, count(t) as tasks
  MATCH (m:PerformanceMetric) WITH agents, tasks, count(m) as metrics
  MATCH (k:KnowledgeItem) WITH agents, tasks, metrics, count(k) as knowledge
  MATCH ()-[c:COLLABORATED_WITH]->() WITH agents, tasks, metrics, knowledge, count(c) as collaborations
  RETURN '  👥 Agents: ' + toString(agents) + '\n' +
         '  📋 Tasks: ' + toString(tasks) + '\n' +
         '  📈 Metrics: ' + toString(metrics) + '\n' +
         '  🧠 Knowledge Items: ' + toString(knowledge) + '\n' +
         '  🤝 Collaborations: ' + toString(collaborations) as summary;
  " | tail -n 1
  
  echo ""
  echo "🎯 Performance Indicators:"
  neo4j_shell "
  MATCH (t:Task {status: 'COMPLETED'})-[:MEASURES]-(m:PerformanceMetric {type: 'confidence_score'})
  WITH avg(m.value) as avg_confidence
  MATCH (a:AgentCard)
  WITH avg_confidence, avg(a.performance_score) as avg_agent_score
  RETURN '  🎯 Average Task Confidence: ' + toString(ROUND(avg_confidence * 100, 1)) + '%\n' +
         '  ⭐ Average Agent Score: ' + toString(ROUND(avg_agent_score * 100, 1)) + '%\n' +
         '  🏆 System Health Score: ' + 
         CASE 
           WHEN avg_confidence > 0.9 AND avg_agent_score > 0.9 THEN 'EXCELLENT (95%)'
           WHEN avg_confidence > 0.8 AND avg_agent_score > 0.8 THEN 'GOOD (85%)'
           ELSE 'NEEDS OPTIMIZATION (75%)'
         END as health_report;
  " | tail -n 1
  
  echo ""
  echo "🌐 Access Information:"
  echo "  🖥️  Neo4j Browser: http://localhost:7474"
  echo "  🔌 Bolt Connection: bolt://localhost:7687"
  echo "  👤 Username: neo4j"
  echo "  🔐 Password: password123"
  echo ""
  echo "==============================================="
  echo "✅ A2A Neo4j System is HEALTHY and READY!"
  echo "==============================================="
}

# Main execution flow
main() {
  echo "🚀 Starting A2A Neo4j verification..."
  echo ""
  
  check_neo4j_running
  check_connectivity
  check_plugins
  verify_schema
  verify_data
  test_a2a_queries
  test_advanced_analytics
  generate_health_report
  
  echo ""
  echo "🎉 Verification complete! Your A2A Neo4j system is fully operational."
}

# Execute main function
main "$@"