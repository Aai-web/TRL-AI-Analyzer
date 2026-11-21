"""Authoritative TRL (Technology Readiness Level 1-9) Criteria and Taxonomy.

Based on NASA SP-20205003605, DoD Technology Readiness Assessment (TRA) Guidance,
and ISO 16290:2013 Space systems — Definition of Technology Readiness Levels (TRLs).
"""

from typing import Dict, List, Any

TRL_DEFINITIONS: Dict[int, Dict[str, Any]] = {
    1: {
        "title": "Basic Principles Observed and Reported",
        "category": "Basic Research",
        "definition": "Lowest level of technology readiness. Scientific research begins to be translated into applied R&D. Examples include paper studies of a technology's basic properties, fundamental physical laws, and mathematical formulations.",
        "milestones": [
            "Basic physical principles observed and mathematically formulated",
            "Initial scientific literature review and theoretical conjectures documented",
            "No experimental proof of concept yet; purely theoretical or observational",
        ],
        "keywords": [
            "theoretical principle", "basic principle", "fundamental physics", "first principles",
            "first-principles", "mathematical model", "theoretical formulation", "observed phenomenon",
            "literature review", "preliminary conjecture", "scientific hypothesis", "analytical equation",
            "paper study", "quantum mechanical", "thermodynamic calculation", "governing equation",
            "ab initio", "theoretical", "hypothesis", "conjecture", "observed", "formulation"
        ],
        "speculative_discount_weight": 0.1,
    },
    2: {
        "title": "Technology Concept and/or Application Formulated",
        "category": "Applied Research",
        "definition": "Invention begins. Once basic principles are observed, practical applications can be invented. Applications are speculative, and there may be no proof or detailed analysis to support the assumptions.",
        "milestones": [
            "Practical application identified and conceptual design outlined",
            "System architecture sketched with functional block diagrams",
            "Analytical protocols proposed; preliminary simulations or qualitative evaluations",
        ],
        "keywords": [
            "concept formulation", "practical application", "conceptual design", "patent application",
            "system concept", "functional block diagram", "proposed architecture", "feasibility assessment",
            "preliminary simulation", "potential use case", "conceptual study", "speculative design",
            "schematic outline", "design rationale", "preliminary engineering"
        ],
        "speculative_discount_weight": 0.2,
    },
    3: {
        "title": "Analytical and Experimental Proof-of-Concept",
        "category": "Feasibility & Proof of Concept",
        "definition": "Active R&D is initiated. This includes analytical studies and laboratory studies to physically validate that the analytical predictions are correct. Validation of separate critical components or functions.",
        "milestones": [
            "Laboratory benchtop experiments demonstrating critical function",
            "Analytical models corroborated by experimental measurements",
            "Proof-of-concept synthesis or small-scale laboratory measurements completed",
        ],
        "keywords": [
            "proof of concept", "proof-of-concept", "laboratory experiment", "benchtop experiment",
            "in vitro", "synthetic demonstration", "experimental validation", "critical function",
            "analytical prediction", "measured response", "measured yield", "lab-scale",
            "test tube", "spectroscopic characterization", "x-ray diffraction", "reproducible measurement"
        ],
        "speculative_discount_weight": 0.35,
    },
    4: {
        "title": "Component Validation in Laboratory Environment",
        "category": "Laboratory Validation",
        "definition": "Basic technological components are integrated to establish that pieces will work together. This is relatively 'low fidelity' compared to the eventual system. Examples include integration of 'ad hoc' hardware in the laboratory.",
        "milestones": [
            "Ad-hoc breadboard system constructed and integrated in lab",
            "Multiple discrete components interoperating together",
            "Functional interfaces tested against baseline lab requirements",
        ],
        "keywords": [
            "breadboard", "laboratory environment", "component validation", "integrated breadboard",
            "benchtop prototype", "functional integration", "subsystem test bench", "lab test rig",
            "interface verification", "component assembly", "low fidelity", "stand-alone test",
            "oscilloscope measurement", "data acquisition rig", "preliminary test coupon"
        ],
        "speculative_discount_weight": 0.45,
    },
    5: {
        "title": "Component Validation in Relevant Environment",
        "category": "Relevant Environment Validation",
        "definition": "Fidelity of breadboard technology increases significantly. The basic technological components are integrated with reasonably realistic supporting elements so they can be tested in a simulated environment.",
        "milestones": [
            "High-fidelity breadboard or brassboard tested in simulated operational conditions",
            "Thermal, vibration, acoustic, or chemical stress testing in relevant environment",
            "Subsystem interfaces tested under realistic boundary conditions",
        ],
        "keywords": [
            "relevant environment", "simulated environment", "brassboard", "environmental chamber",
            "thermal vacuum", "thermal cycling", "stress testing", "simulated flight conditions",
            "accelerated aging", "climatic chamber", "vibration table", "flow loop",
            "pilot scale", "temperature extremes", "simulated solar flux", "realistic loading"
        ],
        "speculative_discount_weight": 0.6,
    },
    6: {
        "title": "System/Subsystem Model Demonstration in Relevant Environment",
        "category": "Engineering Prototype",
        "definition": "Representative model or prototype system, which is well beyond that of TRL 5, is tested in a relevant environment. Represents a major step up in a technology's demonstrated readiness.",
        "milestones": [
            "Full engineering prototype / engineering development model (EDM) built",
            "Demonstration in relevant operational-like environment (e.g. mobile field rig, test aircraft)",
            "System-level performance envelope and margin quantified",
        ],
        "keywords": [
            "engineering prototype", "prototype demonstration", "engineering development model",
            "edm", "relevant environment demonstration", "field test", "subscale flight test",
            "pilot plant run", "mobile testbed", "dynamometer test", "full-scale model",
            "subsystem demonstration", "environmental qualification test", "system-level testing"
        ],
        "speculative_discount_weight": 0.75,
    },
    7: {
        "title": "System Prototype Demonstration in Operational Environment",
        "category": "Operational Demonstration",
        "definition": "Prototype near, or at, planned operational system. Represents a major step up from TRL 6, requiring demonstration of an actual system prototype in an operational environment such as in an aircraft, vehicle, or in space.",
        "milestones": [
            "Full-scale operational prototype tested in actual operating environment",
            "Integration with host operational platform (real aircraft, ground vehicle, production grid)",
            "Demonstration under genuine mission/flight/field operating profiles",
        ],
        "keywords": [
            "operational environment", "flight demonstration", "operational vehicle", "flight test",
            "live grid deployment", "clinical trial phase iii", "real-world operating condition",
            "operational prototype", "sea trial", "road test fleet", "field demonstration",
            "full-scale operational", "integrated into vehicle", "in-flight validation"
        ],
        "speculative_discount_weight": 0.85,
    },
    8: {
        "title": "Actual System Completed and Qualified through Test and Demonstration",
        "category": "Qualification & Pre-Deployment",
        "definition": "Technology has been proven to work in its final form and under expected conditions. In almost all cases, this TRL represents the end of true system development. Examples include developmental test and evaluation of the system.",
        "milestones": [
            "Final production-standard hardware and software completed",
            "Formal qualification testing (compliance, safety, environmental standards) passed",
            "System documentation, manufacturing process, and operating manuals finalized",
        ],
        "keywords": [
            "flight qualified", "type certification", "qualification testing", "qualified through test",
            "acceptance test", "mil-std", "iso 9001", "regulatory approval", "fda clearance",
            "ce mark", "production standard", "pre-production run", "safety certification",
            "environmental qualification", "manufacturing readiness", "final design freeze"
        ],
        "speculative_discount_weight": 0.92,
    },
    9: {
        "title": "Actual System Proven through Successful Mission Operations",
        "category": "Commercial & Mission Operations",
        "definition": "Actual application of the technology in its final form and under mission conditions, such as those encountered through operational mission flights or commercial rollout.",
        "milestones": [
            "Operational mission flights or commercial service sustained with zero critical faults",
            "Mass production, fleet deployment, or broad public/industrial adoption",
            "Reliability, maintenance, and lifetime statistics empirically validated in field",
        ],
        "keywords": [
            "mission proven", "commercial deployment", "operational mission", "flight proven",
            "commercial production", "mass deployment", "in-service operation", "fleet operations",
            "commercial launch", "routine operation", "market deployment", "operational uptime",
            "deployed across", "thousands of flight hours", "commercial revenue", "proven track record"
        ],
        "speculative_discount_weight": 0.98,
    }
}

# Empirical action verbs that indicate verified results
EMPIRICAL_VERBS = [
    "measured", "demonstrated", "achieved", "observed", "tested", "validated", "conducted",
    "recorded", "fabricated", "synthesized", "quantified", "operated", "verified", "evaluated",
    "certified", "deployed", "calibrated", "installed", "passed", "monitored", "executed"
]

# Speculative / future modal indicators that signal unverified claims
SPECULATIVE_MARKERS = [
    "will be", "could be", "aims to", "is expected to", "planned for", "future work",
    "we propose", "hypothesize", "anticipate", "envision", "scheduled to", "in progress",
    "next phase will", "objective is to", "potential to", "may enable", "promising avenue"
]

# Domain categories for technical papers
TECHNICAL_DOMAINS = [
    "Aerospace & Defence",
    "Energy & Clean Tech",
    "Biomedical & Pharmaceuticals",
    "Advanced Materials & Nanotechnology",
    "Electronics & Semiconductors",
    "Robotics & Autonomous Systems",
    "Information Technology & AI",
    "Chemical Engineering"
]
