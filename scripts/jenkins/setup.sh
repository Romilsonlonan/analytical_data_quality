#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
JENKINS_HOME="$PROJECT_ROOT/infra/jenkins/home"

echo "=== Jenkins Setup for Industrial Logistics Platform ==="

if [ ! -d "$JENKINS_HOME" ]; then
    echo "Creating Jenkins home directory: $JENKINS_HOME"
    mkdir -p "$JENKINS_HOME"
fi

if [ ! -f "$JENKINS_HOME/secrets/initialAdminPassword" ]; then
    echo "Jenkins home not initialized yet."
    echo "Run 'docker-compose up -d jenkins' first, then check:"
    echo "  docker exec ilp-jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
fi

echo ""
echo "Creating default job directories..."
mkdir -p "$JENKINS_HOME/jobs"
mkdir -p "$JENKINS_HOME/libs"
mkdir -p "$JENKINS_HOME/scripts"

echo ""
echo "Creating example pipeline..."
cat > "$JENKINS_HOME/jobs/example-pipeline/config.xml" << 'EOF'
<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description>Example pipeline for ILP</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>echo "Hello from Jenkins!"</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
EOF

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Access Jenkins at: http://localhost:8081"
echo "Default credentials: admin / admin123"
echo ""
echo "To get initial admin password:"
echo "  docker exec ilp-jenkins cat /var/jenkins_home/secrets/initialAdminPassword"