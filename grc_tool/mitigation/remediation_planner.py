"""
Remediation Planning Module
Creates comprehensive remediation plans with resource allocation.
"""

import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RemediationPlanner:
    """
    Automated remediation planning and scheduling.
    Provides project management capabilities beyond Nessus.
    """
    
    def __init__(self):
        """Initialize Remediation Planner."""
        logger.info("RemediationPlanner initialized")
    
    def create_remediation_plan(self, mitigation_plans: Dict) -> Dict:
        """
        Create comprehensive remediation plan.
        
        Args:
            mitigation_plans: Organized mitigation plans
            
        Returns:
            Complete remediation plan with timeline
        """
        logger.info("Creating comprehensive remediation plan")
        
        # Create timeline
        timeline = self._create_timeline(mitigation_plans)
        
        # Allocate resources
        resource_allocation = self._allocate_resources(mitigation_plans)
        
        # Create milestones
        milestones = self._define_milestones(timeline)
        
        # Calculate metrics
        metrics = self._calculate_plan_metrics(mitigation_plans)
        
        plan = {
            "plan_created": datetime.now().isoformat(),
            "timeline": timeline,
            "resource_allocation": resource_allocation,
            "milestones": milestones,
            "metrics": metrics,
            "risks": self._identify_plan_risks(mitigation_plans),
            "dependencies": self._identify_dependencies(mitigation_plans)
        }
        
        logger.info("Remediation plan created successfully")
        return plan
    
    def _create_timeline(self, mitigation_plans: Dict) -> Dict:
        """
        Create implementation timeline.
        
        Args:
            mitigation_plans: Mitigation plans
            
        Returns:
            Timeline with phases
        """
        start_date = datetime.now()
        
        phases = []
        current_date = start_date
        
        # Phase 1: Immediate actions
        immediate = mitigation_plans.get("immediate_actions", [])
        if immediate:
            phase1_end = current_date + timedelta(days=1)
            phases.append({
                "phase": 1,
                "name": "Critical Remediation",
                "start_date": current_date.isoformat(),
                "end_date": phase1_end.isoformat(),
                "actions": len(immediate),
                "priority": "CRITICAL"
            })
            current_date = phase1_end
        
        # Phase 2: Urgent actions
        urgent = mitigation_plans.get("urgent_actions", [])
        if urgent:
            phase2_end = current_date + timedelta(days=3)
            phases.append({
                "phase": 2,
                "name": "High Priority Remediation",
                "start_date": current_date.isoformat(),
                "end_date": phase2_end.isoformat(),
                "actions": len(urgent),
                "priority": "HIGH"
            })
            current_date = phase2_end
        
        # Phase 3: Scheduled actions
        scheduled = mitigation_plans.get("scheduled_actions", [])
        if scheduled:
            phase3_end = current_date + timedelta(days=14)
            phases.append({
                "phase": 3,
                "name": "Scheduled Remediation",
                "start_date": current_date.isoformat(),
                "end_date": phase3_end.isoformat(),
                "actions": len(scheduled),
                "priority": "MEDIUM"
            })
            current_date = phase3_end
        
        # Phase 4: Routine actions
        routine = mitigation_plans.get("routine_actions", [])
        if routine:
            phase4_end = current_date + timedelta(days=30)
            phases.append({
                "phase": 4,
                "name": "Routine Remediation",
                "start_date": current_date.isoformat(),
                "end_date": phase4_end.isoformat(),
                "actions": len(routine),
                "priority": "LOW"
            })
        
        return {
            "start_date": start_date.isoformat(),
            "estimated_completion": current_date.isoformat(),
            "total_phases": len(phases),
            "phases": phases
        }
    
    def _allocate_resources(self, mitigation_plans: Dict) -> Dict:
        """
        Allocate resources for remediation.
        
        Args:
            mitigation_plans: Mitigation plans
            
        Returns:
            Resource allocation plan
        """
        all_plans = (
            mitigation_plans.get("immediate_actions", []) +
            mitigation_plans.get("urgent_actions", []) +
            mitigation_plans.get("scheduled_actions", []) +
            mitigation_plans.get("routine_actions", [])
        )
        
        # Collect all required resources
        resource_needs = {}
        for plan in all_plans:
            for resource in plan.get("required_resources", []):
                if resource not in resource_needs:
                    resource_needs[resource] = {
                        "count": 0,
                        "total_hours": 0,
                        "phases": []
                    }
                resource_needs[resource]["count"] += 1
                
                # Estimate hours from effort
                effort = plan.get("estimated_effort", "Low (< 4 hours)")
                hours = self._parse_effort_hours(effort)
                resource_needs[resource]["total_hours"] += hours
        
        return {
            "resource_requirements": resource_needs,
            "total_resource_types": len(resource_needs),
            "estimated_team_size": self._estimate_team_size(resource_needs)
        }
    
    def _define_milestones(self, timeline: Dict) -> List[Dict]:
        """
        Define project milestones.
        
        Args:
            timeline: Project timeline
            
        Returns:
            List of milestones
        """
        milestones = []
        
        for phase in timeline.get("phases", []):
            milestones.append({
                "milestone": f"Complete Phase {phase['phase']}",
                "target_date": phase["end_date"],
                "criteria": f"All {phase['actions']} actions in {phase['name']} completed",
                "status": "PENDING"
            })
        
        # Add final milestone
        milestones.append({
            "milestone": "Complete Remediation",
            "target_date": timeline.get("estimated_completion"),
            "criteria": "All identified risks mitigated and validated",
            "status": "PENDING"
        })
        
        return milestones
    
    def _calculate_plan_metrics(self, mitigation_plans: Dict) -> Dict:
        """
        Calculate plan metrics.
        
        Args:
            mitigation_plans: Mitigation plans
            
        Returns:
            Plan metrics
        """
        all_plans = (
            mitigation_plans.get("immediate_actions", []) +
            mitigation_plans.get("urgent_actions", []) +
            mitigation_plans.get("scheduled_actions", []) +
            mitigation_plans.get("routine_actions", [])
        )
        
        total_cost = sum(
            plan.get("cost_estimate", {}).get("total_cost_usd", 0)
            for plan in all_plans
        )
        
        total_effort = sum(
            self._parse_effort_hours(plan.get("estimated_effort", "Low (< 4 hours)"))
            for plan in all_plans
        )
        
        return {
            "total_actions": len(all_plans),
            "total_estimated_cost_usd": total_cost,
            "total_estimated_hours": total_effort,
            "average_cost_per_action": total_cost / max(len(all_plans), 1),
            "average_hours_per_action": total_effort / max(len(all_plans), 1)
        }
    
    def _identify_plan_risks(self, mitigation_plans: Dict) -> List[Dict]:
        """
        Identify risks to the remediation plan.
        
        Args:
            mitigation_plans: Mitigation plans
            
        Returns:
            List of plan risks
        """
        risks = []
        
        summary = mitigation_plans.get("summary", {})
        
        if summary.get("immediate_count", 0) > 5:
            risks.append({
                "risk": "Resource Overload",
                "description": "High number of immediate actions may overwhelm team",
                "mitigation": "Consider additional resources or prioritize further"
            })
        
        if summary.get("total_count", 0) > 20:
            risks.append({
                "risk": "Project Complexity",
                "description": "Large number of actions increases project complexity",
                "mitigation": "Break into smaller sub-projects with dedicated leads"
            })
        
        risks.append({
            "risk": "System Downtime",
            "description": "Remediation may require system downtime",
            "mitigation": "Schedule maintenance windows, plan for redundancy"
        })
        
        return risks
    
    def _identify_dependencies(self, mitigation_plans: Dict) -> List[Dict]:
        """
        Identify dependencies between actions.
        
        Args:
            mitigation_plans: Mitigation plans
            
        Returns:
            List of dependencies
        """
        # Simplified dependency identification
        dependencies = []
        
        all_plans = (
            mitigation_plans.get("immediate_actions", []) +
            mitigation_plans.get("urgent_actions", [])
        )
        
        # Look for common dependencies
        patching_plans = [p for p in all_plans if "patch" in p.get("risk_type", "").lower()]
        config_plans = [p for p in all_plans if "config" in p.get("risk_type", "").lower()]
        
        if patching_plans and config_plans:
            dependencies.append({
                "dependency": "Patching before Configuration",
                "description": "Apply patches before reconfiguring services",
                "affected_actions": len(patching_plans) + len(config_plans)
            })
        
        return dependencies
    
    def _parse_effort_hours(self, effort_string: str) -> float:
        """
        Parse effort hours from string.
        
        Args:
            effort_string: Effort description
            
        Returns:
            Hours as float
        """
        if "Low" in effort_string:
            return 2.0
        elif "Medium" in effort_string:
            return 10.0
        elif "High" in effort_string:
            return 20.0
        return 5.0
    
    def _estimate_team_size(self, resource_needs: Dict) -> int:
        """
        Estimate required team size.
        
        Args:
            resource_needs: Resource requirements
            
        Returns:
            Estimated team size
        """
        # Simplified team size estimation
        total_hours = sum(r["total_hours"] for r in resource_needs.values())
        
        # Assume 8-hour workdays and 2-week sprint
        available_hours_per_person = 8 * 10  # 80 hours
        
        team_size = max(1, int(total_hours / available_hours_per_person) + 1)
        
        return min(team_size, 10)  # Cap at 10 for practicality
