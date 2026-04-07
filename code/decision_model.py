"""decision_model.py

Starter skeleton for bounded decision-making in embedded AI systems.

Core pipeline:
1) Read current system state.
2) Generate candidate actions (policy output placeholder).
3) Filter by hard constraints (safety + hardware limits).
4) Select best feasible action.
5) Fall back to conservative safe behavior when needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass(frozen=True)
class SystemState:
    """Represents a minimal embedded system state."""

    battery_level: float         # 0.0 to 1.0
    temperature_c: float         # device temperature
    obstacle_distance_m: float   # nearest obstacle distance
    mission_priority: float      # 0.0 (low) to 1.0 (high)


@dataclass(frozen=True)
class Action:
    """Candidate action proposed by a policy."""

    name: str
    power_cost: float            # abstract normalized power draw
    thermal_impact: float        # expected temperature increase
    risk_score: float            # lower is safer
    reward_score: float          # higher is better for objective


Constraint = Callable[[SystemState, Action], bool]


class AmygdalicDecisionModel:
    """Bounded action selector with safety interlock semantics."""

    def __init__(self, constraints: List[Constraint]) -> None:
        self.constraints = constraints

    def propose_actions(self, state: SystemState) -> List[Action]:
        """Placeholder policy output.

        In a real system, replace with model inference or planner output.
        """
        return [
            Action("accelerate", power_cost=0.45, thermal_impact=3.0, risk_score=0.50, reward_score=0.90),
            Action("maintain", power_cost=0.20, thermal_impact=1.0, risk_score=0.20, reward_score=0.65),
            Action("decelerate", power_cost=0.15, thermal_impact=0.3, risk_score=0.10, reward_score=0.55),
            Action("stop", power_cost=0.05, thermal_impact=0.1, risk_score=0.02, reward_score=0.40),
        ]

    def filter_feasible_actions(self, state: SystemState, actions: List[Action]) -> List[Action]:
        """Apply hard constraints: only actions passing all constraints survive."""
        feasible: List[Action] = []
        for action in actions:
            if all(rule(state, action) for rule in self.constraints):
                feasible.append(action)
        return feasible

    def select_action(self, state: SystemState, feasible_actions: List[Action]) -> Action:
        """Choose action from safe set using a simple bounded utility function."""
        if not feasible_actions:
            return self.safe_fallback_action(state)

        def utility(a: Action) -> float:
            return (0.7 * a.reward_score) - (0.3 * a.risk_score)

        return max(feasible_actions, key=utility)

    def safe_fallback_action(self, state: SystemState) -> Action:
        """Conservative fallback when no feasible action exists."""
        return Action("safe_hold", power_cost=0.04, thermal_impact=0.0, risk_score=0.0, reward_score=0.1)

    def decide(self, state: SystemState) -> Dict[str, object]:
        """Full decision pipeline for one control step."""
        proposals = self.propose_actions(state)
        feasible = self.filter_feasible_actions(state, proposals)
        selected = self.select_action(state, feasible)

        return {
            "state": state,
            "proposed_actions": proposals,
            "feasible_actions": feasible,
            "selected_action": selected,
        }


# ---- Example constraint rules (safety interlock) --------------------------------

def battery_constraint(state: SystemState, action: Action) -> bool:
    """Disallow high-power actions when battery is critically low."""
    if state.battery_level < 0.15 and action.power_cost > 0.2:
        return False
    return True


def thermal_constraint(state: SystemState, action: Action) -> bool:
    """Disallow actions that may exceed thermal budget."""
    max_temp_c = 80.0
    projected_temp = state.temperature_c + action.thermal_impact
    return projected_temp <= max_temp_c


def obstacle_safety_constraint(state: SystemState, action: Action) -> bool:
    """Disallow aggressive motion near obstacles."""
    if state.obstacle_distance_m < 0.5 and action.name == "accelerate":
        return False
    return True


if __name__ == "__main__":
    model = AmygdalicDecisionModel(
        constraints=[
            battery_constraint,
            thermal_constraint,
            obstacle_safety_constraint,
        ]
    )

    sample_state = SystemState(
        battery_level=0.12,
        temperature_c=77.5,
        obstacle_distance_m=0.4,
        mission_priority=0.8,
    )

    decision = model.decide(sample_state)
    print("Selected action:", decision["selected_action"])
    print("Feasible actions:", [a.name for a in decision["feasible_actions"]])
