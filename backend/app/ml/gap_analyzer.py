"""Intelligent Gap Analysis and Prioritized Actionable Roadmap Engine.

Identifies missing technical requirements for the predicted TRL, detects specific impediments
preventing progression to the next TRL, and generates prioritized de-risking roadmaps.
"""

import uuid
from typing import List, Dict, Any, Tuple

from ..models.schemas import GapRequirement, RoadmapPhase, EvidenceItem
from .trl_criteria import TRL_DEFINITIONS

class GapAnalyzer:
    """Performs rigorous gap analysis and constructs prioritized engineering roadmaps."""

    def __init__(self):
        # Standardized protocol references by TRL transition
        self.transition_protocols: Dict[int, Dict[str, Any]] = {
            2: {
                "action": "Formulate mathematical system specifications and complete detailed architectural design.",
                "tests": ["Analytical numerical simulation (COMSOL/ANSYS/MATLAB)", "First-order thermodynamics/mass balance verification", "Component trade-off study"],
                "deliverables": ["Preliminary Design Document (PDD)", "Interface Control Document (ICD) draft", "Simulation verification report"],
                "timeline": "1 - 3 Months"
            },
            3: {
                "action": "Synthesize or fabricate basic lab specimens and perform analytical proof-of-concept tests.",
                "tests": ["Benchtop functional characterization", "Spectroscopic / material property measurement", "Baseline performance calibration"],
                "deliverables": ["Laboratory Proof-of-Concept Report", "Empirical data logs", "Repeatability analysis dossier"],
                "timeline": "3 - 6 Months"
            },
            4: {
                "action": "Integrate discrete lab components into a functional benchtop breadboard assembly.",
                "tests": ["Component inter-communication test", "Signal/power interface verification", "Benchtop closed-loop control test"],
                "deliverables": ["Integrated Breadboard Test Report", "Breadboard schematic & firmware release", "Error margin quantification"],
                "timeline": "4 - 8 Months"
            },
            5: {
                "action": "Subject high-fidelity brassboard unit to relevant simulated environmental stresses.",
                "tests": ["Climatic chamber thermal cycling (-40°C to +85°C)", "Vibration & acoustic excitation sweep", "Simulated operational medium/gas exposure"],
                "deliverables": ["Environmental Test Report (ETR)", "Failure mode and effects analysis (FMEA)", "Degradation rate analysis"],
                "timeline": "6 - 12 Months"
            },
            6: {
                "action": "Construct a full-scale engineering development prototype and conduct field/pilot trials.",
                "tests": ["Pilot plant continuous endurance run (100+ hours)", "Subscale flight or mobile field rig demonstration", "Transient load rejection & fault injection testing"],
                "deliverables": ["Engineering Development Model (EDM) Dossier", "Field Demonstration Logbook", "System-level margin documentation"],
                "timeline": "9 - 18 Months"
            },
            7: {
                "action": "Integrate operational prototype into the target host platform for operational trials.",
                "tests": ["Live operational vehicle / grid / flight demonstration", "Real mission profile duty cycle execution", "Host platform electromagnetic & telemetry interoperability"],
                "deliverables": ["Operational Demonstration Flight/Field Report", "Safety hazard analysis", "Operational envelope sign-off"],
                "timeline": "12 - 24 Months"
            },
            8: {
                "action": "Finalize production design and execute formal regulatory qualification testing.",
                "tests": ["Mil-STD-810H / DO-160 / ISO formal qualification suite", "Full environmental & EMI/EMC compliance testing", "First article inspection (FAI) and burn-in"],
                "deliverables": ["Type Certification / Regulatory Clearance Dossier", "Frozen production drawing package", "Manufacturing Readiness Level (MRL 8) report"],
                "timeline": "12 - 20 Months"
            },
            9: {
                "action": "Deploy into continuous commercial service or operational mission flights.",
                "tests": ["Continuous mission telemetry monitoring", "Fleet-wide MTBF and reliability growth tracking", "Post-market surveillance and preventive maintenance audits"],
                "deliverables": ["Mission Completion Certificate", "Commercial Service Reliability Report", "Customer SLA & warranty audit"],
                "timeline": "Ongoing / 12+ Months"
            }
        }

    def analyze_gaps(
        self,
        predicted_trl: int,
        evidence_items: List[EvidenceItem],
        doc_text: str
    ) -> Tuple[List[GapRequirement], List[str], List[RoadmapPhase]]:
        """Perform comprehensive gap analysis and generate a 3-phase improvement roadmap."""
        doc_lower = doc_text.lower()
        next_trl = min(9, predicted_trl + 1)

        # Map existing evidence by TRL level and strength
        ev_by_trl: Dict[int, List[EvidenceItem]] = {}
        for ev in evidence_items:
            ev_by_trl.setdefault(ev.trl_level, []).append(ev)

        gap_requirements: List[GapRequirement] = []
        next_trl_barriers: List[str] = []

        # 1. Evaluate current TRL milestones
        current_meta = TRL_DEFINITIONS[predicted_trl]
        for idx, milestone in enumerate(current_meta["milestones"]):
            has_strong = any(e.strength == "Strong" for e in ev_by_trl.get(predicted_trl, []))
            has_mod = any(e.strength == "Moderate" for e in ev_by_trl.get(predicted_trl, []))

            if has_strong:
                status = "Met"
                severity = "Minor"
                impediment = "Requirement satisfied by verified empirical results in document."
                action = f"Maintain documentation of {milestone} for qualification dossier."
            elif has_mod:
                status = "Partially Met"
                severity = "Major"
                impediment = "Addressed with preliminary observations but lacks long-term quantitative repeatability."
                action = f"Conduct rigorous multi-batch verification experiments for {milestone}."
            else:
                status = "Missing"
                severity = "Critical"
                impediment = f"No direct empirical validation for {milestone} found in submitted documentation."
                action = f"Prioritize immediate execution of baseline tests to establish {milestone}."

            proto = self.transition_protocols.get(predicted_trl, self.transition_protocols[2])
            gap_requirements.append(
                GapRequirement(
                    requirement_id=f"GAP-{predicted_trl}-{idx+1}",
                    target_trl=predicted_trl,
                    category=f"TRL {predicted_trl} Baseline",
                    title=f"{current_meta['title']} - Milestone {idx+1}",
                    description=milestone,
                    status=status,
                    gap_severity=severity,
                    impediment_explanation=impediment,
                    recommended_action=action,
                    recommended_tests=proto["tests"][:2]
                )
            )

        # 2. Evaluate NEXT TRL milestones (The primary blockers)
        if next_trl > predicted_trl:
            next_meta = TRL_DEFINITIONS[next_trl]
            for idx, milestone in enumerate(next_meta["milestones"]):
                has_ev = bool(ev_by_trl.get(next_trl))
                status = "Partially Met" if has_ev else "Missing"
                severity = "Critical" if idx == 0 else "Major"

                impediment = (
                    f"The technology currently lacks validated demonstration of: '{milestone}'. "
                    f"This constitutes the primary technical bottleneck preventing advancement to TRL {next_trl}."
                )
                next_trl_barriers.append(
                    f"TRL {next_trl} Gate: Absence of demonstrated '{milestone}' in required environment."
                )

                proto = self.transition_protocols.get(next_trl, self.transition_protocols[min(9, next_trl)])
                gap_requirements.append(
                    GapRequirement(
                        requirement_id=f"GAP-{next_trl}-{idx+1}",
                        target_trl=next_trl,
                        category=f"TRL {next_trl} Progression Gate",
                        title=f"{next_meta['title']} - Advancement Criterion {idx+1}",
                        description=milestone,
                        status=status,
                        gap_severity=severity,
                        impediment_explanation=impediment,
                        recommended_action=proto["action"],
                        recommended_tests=proto["tests"]
                    )
                )

        # 3. Generate Prioritized 3-Phase Roadmap
        roadmap: List[RoadmapPhase] = []

        # Phase 1: Immediate De-Risking & Consolidation
        p1_target = predicted_trl
        p1_proto = self.transition_protocols.get(p1_target, self.transition_protocols[2])
        roadmap.append(
            RoadmapPhase(
                phase_id="PHASE-1",
                phase_name=f"Phase 1: Baseline Consolidation & Evidence De-Risking (TRL {p1_target})",
                target_trl=p1_target,
                timeline_estimate=p1_proto["timeline"],
                priority="High",
                milestones=[
                    f"Close all unverified claims identified in TRL {p1_target} assessment",
                    "Conduct repeatability tests with statistical variance bounds",
                    "Standardize interface and calibration documentation"
                ],
                validation_protocol=p1_proto["tests"][0] if p1_proto["tests"] else "Benchtop validation protocol",
                deliverables=p1_proto["deliverables"]
            )
        )

        # Phase 2: System Advancement & Environmental Integration
        p2_target = min(9, predicted_trl + 1)
        p2_proto = self.transition_protocols.get(p2_target, self.transition_protocols[min(9, p2_target)])
        roadmap.append(
            RoadmapPhase(
                phase_id="PHASE-2",
                phase_name=f"Phase 2: Advancement & Environmental Validation (TRL {p2_target})",
                target_trl=p2_target,
                timeline_estimate=p2_proto["timeline"],
                priority="High" if p2_target <= 6 else "Medium",
                milestones=[
                    f"Integrate subsystem components into {TRL_DEFINITIONS[p2_target]['category']} configuration",
                    f"Execute targeted testing: {p2_proto['tests'][0]}",
                    "Quantify operational margins and failure boundaries"
                ],
                validation_protocol=p2_proto["action"],
                deliverables=p2_proto["deliverables"]
            )
        )

        # Phase 3: Qualification & Operational Transition
        p3_target = min(9, predicted_trl + 2)
        p3_proto = self.transition_protocols.get(p3_target, self.transition_protocols[min(9, p3_target)])
        roadmap.append(
            RoadmapPhase(
                phase_id="PHASE-3",
                phase_name=f"Phase 3: Formal Qualification & Deployment Pathway (TRL {p3_target})",
                target_trl=p3_target,
                timeline_estimate=p3_proto["timeline"],
                priority="Medium" if p3_target <= 8 else "Low",
                milestones=[
                    f"Prepare complete compliance package for TRL {p3_target}",
                    f"Conduct {p3_proto['tests'][-1]} under authorized oversight",
                    "Transition manufacturing and operational handover protocols"
                ],
                validation_protocol=f"Standardized qualification per {p3_proto['deliverables'][0]}",
                deliverables=p3_proto["deliverables"]
            )
        )

        return gap_requirements, next_trl_barriers, roadmap
