"""Curated benchmark dataset for Technology Readiness Level (TRL 1-9) Classification.

This module provides a reproducible, diverse dataset spanning scientific research papers,
laboratory reports, patent filings, prototype engineering trials, flight tests,
qualification reports, and commercial mission logs across 8 engineering domains.
"""

from typing import List, Dict, Any
import numpy as np

BENCHMARK_SAMPLES: List[Dict[str, Any]] = [
    # ==================== TRL 1: Basic Principles Observed ====================
    {
        "id": "TRL1-AERO-01",
        "trl": 1,
        "domain": "Aerospace & Defence",
        "title": "Theoretical Formulation of Magnetoplasmadynamic Surface Boundary Effects",
        "text": "In this paper we present a mathematical formulation and first-principles study of magnetoplasmadynamic coupling in hypersonic boundary layers. Using the Boltzmann transport equations, we observe and calculate theoretical plasma sheath dissipation coefficients. No physical hardware has been built or experimentally tested. This paper review identifies fundamental governing physics for potential future research.",
        "key_evidence": "Using the Boltzmann transport equations, we observe and calculate theoretical plasma sheath dissipation coefficients. No physical hardware has been built or experimentally tested.",
        "split": "train"
    },
    {
        "id": "TRL1-MAT-02",
        "trl": 1,
        "domain": "Advanced Materials & Nanotechnology",
        "title": "Ab Initio Density Functional Theory of 2D Borophene Superconductivity",
        "text": "We report quantum mechanical density functional theory (DFT) calculations investigating the theoretical possibility of phonon-mediated superconductivity in monolayer borophene. The electron-phonon coupling constant was computed analytically from first principles. The results represent a purely theoretical observation of physical properties without experimental synthesis.",
        "key_evidence": "The results represent a purely theoretical observation of physical properties without experimental synthesis.",
        "split": "train"
    },
    {
        "id": "TRL1-ENERGY-03",
        "trl": 1,
        "domain": "Energy & Clean Tech",
        "title": "Thermodynamic Limit Calculations for Photochemical Triplet-Triplet Annihilation",
        "text": "A rigorous thermodynamic analysis of upconversion efficiency limits in organic multi-chromophore systems is performed. Mathematical derivations show the theoretical upper bound of conversion efficiency under non-concentrated solar illumination. This paper studies basic principles of energy transfer; no experimental photochemical cells were assembled.",
        "key_evidence": "This paper studies basic principles of energy transfer; no experimental photochemical cells were assembled.",
        "split": "val"
    },
    {
        "id": "TRL1-BIO-04",
        "trl": 1,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "Mathematical Modeling of Conformational Dynamics in Prion Misfolding",
        "text": "We formulate stochastic differential equations to simulate the statistical mechanics of peptide backbone folding. The mathematical framework reproduces the theoretical energy barrier between alpha-helix and beta-sheet states. These fundamental thermodynamic principles describe the molecular phenomenon, serving as an initial scientific hypothesis.",
        "key_evidence": "These fundamental thermodynamic principles describe the molecular phenomenon, serving as an initial scientific hypothesis.",
        "split": "test"
    },

    # ==================== TRL 2: Concept Formulated ====================
    {
        "id": "TRL2-ENERGY-01",
        "trl": 2,
        "domain": "Energy & Clean Tech",
        "title": "Conceptual Design of a Direct Formic Acid Fuel Cell for Micro-Sensors",
        "text": "We formulate a practical concept and system architecture for a microfluidic direct formic acid fuel cell intended for autonomous environmental sensors. We propose a schematic functional block diagram incorporating a flow channel network and multi-layer membrane. Preliminary numerical simulations suggest energy density up to 450 Wh/L, but no physical components or catalysts have been synthesized or measured experimentally.",
        "key_evidence": "We propose a schematic functional block diagram incorporating a flow channel network and multi-layer membrane, but no physical components or catalysts have been synthesized.",
        "split": "train"
    },
    {
        "id": "TRL2-AERO-02",
        "trl": 2,
        "domain": "Aerospace & Defence",
        "title": "System Concept for Closed-Loop Cryogenic Boil-Off Re-liquefaction",
        "text": "This patent disclosure describes an architectural concept for cryogenic propellant conservation on long-duration orbital stages. The practical application uses a reverse Brayton cryocooler linked to a multi-point heat exchanger. We formulate mass-balance calculations and preliminary design requirements. Physical hardware synthesis has not yet begun.",
        "key_evidence": "The practical application uses a reverse Brayton cryocooler linked to a multi-point heat exchanger. Physical hardware synthesis has not yet begun.",
        "split": "train"
    },
    {
        "id": "TRL2-ROBOT-03",
        "trl": 2,
        "domain": "Robotics & Autonomous Systems",
        "title": "Architectural Framework for Distributed Tactile Skin in Soft Grippers",
        "text": "We outline a proposed technology concept for embedding conductive polymer piezoresistive arrays into compliant elastomer fingers. The application is conceptualized for delicate agricultural harvesting. While the CAD layouts and kinematic transfer functions are established, experimental fabrication of the tactile arrays remains future work.",
        "key_evidence": "While the CAD layouts and kinematic transfer functions are established, experimental fabrication of the tactile arrays remains future work.",
        "split": "val"
    },
    {
        "id": "TRL2-IT-04",
        "trl": 2,
        "domain": "Information Technology & AI",
        "title": "Conceptual Architecture for Neuromorphic Optical Ternary Logic Gates",
        "text": "An invention concept for ultra-fast all-optical ternary logic using phase-change materials is formulated. We present the conceptual layout of optical waveguide junctions and theoretical truth tables. No integrated silicon-photonic dies have been fabricated to date; the application is at the conceptual design phase.",
        "key_evidence": "No integrated silicon-photonic dies have been fabricated to date; the application is at the conceptual design phase.",
        "split": "test"
    },

    # ==================== TRL 3: Analytical & Experimental Proof of Concept ====================
    {
        "id": "TRL3-MAT-01",
        "trl": 3,
        "domain": "Advanced Materials & Nanotechnology",
        "title": "Experimental Proof-of-Concept for Self-Healing Graphene Epoxy Composites",
        "text": "Active experimental R&D was initiated to validate microencapsulated healing agents in graphene-reinforced epoxy resin. Laboratory benchtop experiments demonstrated 78% fracture toughness recovery after crack induction under controlled 3-point bend tests. Measured spectroscopic data confirmed localized polymerization. This successful small-scale laboratory experiment provides initial proof of concept.",
        "key_evidence": "Laboratory benchtop experiments demonstrated 78% fracture toughness recovery after crack induction under controlled 3-point bend tests.",
        "split": "train"
    },
    {
        "id": "TRL3-ENERGY-02",
        "trl": 3,
        "domain": "Energy & Clean Tech",
        "title": "Laboratory Validation of Silicon-Carbon Nanocomposite Anodes",
        "text": "We synthesized silicon-carbon composite nanoparticles at 5-gram lab batch scale and tested critical electrochemical proof of concept in half-cell coin configurations. The laboratory experiment demonstrated a reversible specific capacity of 1,420 mAh/g over 50 cycles at C/5 rate. These synthetic benchtop measurements corroborate analytical predictions of lithium intercalation kinetics.",
        "key_evidence": "The laboratory experiment demonstrated a reversible specific capacity of 1,420 mAh/g over 50 cycles at C/5 rate in half-cell coin configurations.",
        "split": "train"
    },
    {
        "id": "TRL3-BIO-03",
        "trl": 3,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "In Vitro Proof-of-Concept for Magnetic Nanoparticle Hyperthermia",
        "text": "We performed in vitro cell culture studies to test targeted iron-oxide nanoparticle heating under alternating magnetic fields. In 24-well culture plates, cellular uptake was validated and cancer cell viability dropped by 84% under 300 kHz excitation for 15 minutes. This bench-scale experiment verifies the critical therapeutic mechanism.",
        "key_evidence": "In 24-well culture plates, cellular uptake was validated and cancer cell viability dropped by 84% under 300 kHz excitation for 15 minutes.",
        "split": "val"
    },
    {
        "id": "TRL3-CHEM-04",
        "trl": 3,
        "domain": "Chemical Engineering",
        "title": "Lab-Scale Experimental Feasibility of Photocatalytic Ammonia Synthesis",
        "text": "A 100 mL quartz batch reactor was set up to test nitrogen reduction on defective titanium oxide catalysts under simulated UV-visible light. Reproducible ammonia yields of 42 micromoles per gram per hour were measured by indophenol spectrophotometry. Analytical models matched experimental rate kinetics, confirming analytical proof-of-concept.",
        "key_evidence": "Reproducible ammonia yields of 42 micromoles per gram per hour were measured by indophenol spectrophotometry in a 100 mL quartz batch reactor.",
        "split": "test"
    },

    # ==================== TRL 4: Component/Breadboard in Lab Environment ====================
    {
        "id": "TRL4-ELEC-01",
        "trl": 4,
        "domain": "Electronics & Semiconductors",
        "title": "Breadboard Integration and Lab Testing of 100 GHz Radar Transceiver",
        "text": "Individual MMIC amplifier chips, a phase shifter, and planar antenna arrays were integrated into an ad-hoc breadboard test rig in the laboratory environment. The integrated breadboard demonstrated stable continuous beam-steering across +/-45 degrees with an output power of 18 dBm on the laboratory bench. Oscilloscope and network analyzer measurements confirmed multi-component interoperability under lab ambient temperatures.",
        "key_evidence": "Integrated into an ad-hoc breadboard test rig in the laboratory environment; demonstrated stable continuous beam-steering across +/-45 degrees on the lab bench.",
        "split": "train"
    },
    {
        "id": "TRL4-ROBOT-02",
        "trl": 4,
        "domain": "Robotics & Autonomous Systems",
        "title": "Laboratory Breadboard Validation of Tendon-Driven Dexterous Gripper",
        "text": "We assembled a low-fidelity benchtop breadboard combining Feetech smart servos, tendon routing pullies, and a custom microcontroller board on an optical bench. The integrated lab assembly successfully grasped 12 distinct geometric objects, verifying inter-component communications and force feedback control in a benchtop laboratory setting.",
        "key_evidence": "Assembled a low-fidelity benchtop breadboard; the integrated lab assembly successfully grasped 12 distinct geometric objects in a benchtop laboratory setting.",
        "split": "train"
    },
    {
        "id": "TRL4-AERO-03",
        "trl": 4,
        "domain": "Aerospace & Defence",
        "title": "Lab Breadboard Testing of Optical Air Data Sensing Subsystem",
        "text": "A laboratory breadboard system consisting of a continuous-wave laser diode, fiber coupler, and balanced photodetectors was integrated on an optical table. Synthetic aerosol injection into a small bench wind-tunnel was used to evaluate velocity estimation. Interfacing between optical sensors and DSP boards operated continuously for 8 hours under lab conditions.",
        "key_evidence": "Laboratory breadboard system integrated on an optical table; interfacing between optical sensors and DSP boards operated continuously for 8 hours under lab conditions.",
        "split": "val"
    },
    {
        "id": "TRL4-ENERGY-04",
        "trl": 4,
        "domain": "Energy & Clean Tech",
        "title": "Integration and Lab Validation of Flow Battery Stack and Electrolyte Pump",
        "text": "A 500-watt vanadium redox flow battery breadboard was constructed by integrating a 5-cell stack, peristaltic pumps, and analog state-of-charge monitors in a dedicated lab test stand. The breadboard demonstrated 74% round-trip Coulombic efficiency over 20 consecutive charge-discharge cycles in controlled room temperature.",
        "key_evidence": "A 500-watt vanadium redox flow battery breadboard was constructed and demonstrated 74% round-trip Coulombic efficiency in a dedicated lab test stand.",
        "split": "test"
    },

    # ==================== TRL 5: Component/Breadboard in Relevant Environment ====================
    {
        "id": "TRL5-AERO-01",
        "trl": 5,
        "domain": "Aerospace & Defence",
        "title": "Thermal Vacuum Chamber Validation of High-Power CubeSat Transceiver",
        "text": "A high-fidelity brassboard unit of the S-band CubeSat transceiver was placed inside an environmental thermal vacuum (TVAC) chamber simulating low Earth orbit conditions. The brassboard underwent 12 thermal cycles between -40 deg C and +85 deg C at 1e-6 Torr while actively transmitting at 5W RF power. Measured bit error rate remained below 1e-7 with no thermal runaway, validating component fidelity in a relevant space environment.",
        "key_evidence": "A high-fidelity brassboard unit underwent 12 thermal cycles between -40 deg C and +85 deg C at 1e-6 Torr in an environmental thermal vacuum (TVAC) chamber.",
        "split": "train"
    },
    {
        "id": "TRL5-ENERGY-02",
        "trl": 5,
        "domain": "Energy & Clean Tech",
        "title": "High-Pressure Simulated Flue Gas Testing of Solid Amine Sorbent Canister",
        "text": "A 10 kW-thermal equivalent brassboard carbon capture canister was tested in a relevant simulated coal flue gas environment with 14% CO2, 5% O2, and 85% relative humidity at 65 deg C. The integrated sorbent system demonstrated 91% CO2 capture efficiency across 100 continuous adsorption-regeneration cycles under realistic dynamic gas velocities.",
        "key_evidence": "Tested in a relevant simulated coal flue gas environment; demonstrated 91% CO2 capture efficiency across 100 continuous adsorption-regeneration cycles.",
        "split": "train"
    },
    {
        "id": "TRL5-BIO-03",
        "trl": 5,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "In Vivo Biocompatibility Testing in Porcine Organ Perfusion Loop",
        "text": "A prototype bio-artificial liver hollow fiber cartridge was integrated into an ex vivo normothermic porcine liver perfusion circuit simulating acute hepatic failure hemodynamics. Over 48 hours of continuous circulation at 37 deg C with pulsatile flow, albumin synthesis was 18 mg/hr and clearance of ammonia exceeded 65%, demonstrating component functionality in a relevant physiological environment.",
        "key_evidence": "Integrated into an ex vivo normothermic porcine liver perfusion circuit simulating acute hepatic failure hemodynamics over 48 hours of continuous circulation.",
        "split": "val"
    },
    {
        "id": "TRL5-ROBOT-04",
        "trl": 5,
        "domain": "Robotics & Autonomous Systems",
        "title": "Relevant Environment Climatic Mud and Dust Ingress Testing of Wheel Drive",
        "text": "An agricultural robot planetary hub motor brassboard was mounted in a simulated outdoor environmental test chamber subjected to IP67 water spray, fine ISO Arizona road dust, and slurry immersion at -10 deg C to +50 deg C for 200 hours. The sealed brassboard preserved torque output without seal compromise or electrical degradation.",
        "key_evidence": "Mounted in a simulated outdoor environmental test chamber subjected to IP67 water spray, fine dust, and slurry immersion for 200 hours.",
        "split": "test"
    },

    # ==================== TRL 6: Prototype Demonstration in Relevant Environment ====================
    {
        "id": "TRL6-AERO-01",
        "trl": 6,
        "domain": "Aerospace & Defence",
        "title": "Field Test of Subscale Hypersonic Scramjet Combustor on Rocket Sled",
        "text": "A full engineering development model (EDM) prototype of an ethylene-fueled scramjet combustor was mounted onto a high-speed rocket sled at Holloman AFB. During a Mach 4.2 sprint through atmospheric conditions, the prototype ignited autonomously, sustained supersonic combustion for 4.8 seconds, and generated 2.1 kN of net positive thrust. This field demonstration confirmed system-level aerodynamic and thermal performance in a relevant operational flight regime.",
        "key_evidence": "A full engineering development model (EDM) prototype was mounted onto a high-speed rocket sled, sustained supersonic combustion for 4.8 seconds, generating 2.1 kN thrust.",
        "split": "train"
    },
    {
        "id": "TRL6-ENERGY-02",
        "trl": 6,
        "domain": "Energy & Clean Tech",
        "title": "Pilot Plant Demonstration of 1 MW Supercritical CO2 Power Turbine",
        "text": "An engineering prototype of a 1 MWe axial supercritical CO2 turbine skid was connected to a closed industrial loop at an offsite thermal test facility. The prototype ran continuously for 120 hours at 550 deg C and 200 bar, achieving 31.8% thermal-to-electric conversion efficiency under realistic fluctuating heat source conditions. Transient shutdown and startup protocols were successfully proven.",
        "key_evidence": "An engineering prototype of a 1 MWe axial turbine ran continuously for 120 hours at 550 deg C and 200 bar at an offsite thermal test facility.",
        "split": "train"
    },
    {
        "id": "TRL6-ROBOT-03",
        "trl": 6,
        "domain": "Robotics & Autonomous Systems",
        "title": "Field Demonstration of Autonomous Underground Mining Hauler Prototype",
        "text": "A full-scale engineering prototype autonomous haul truck equipped with multispectral LiDAR, radar, and stereo cameras was demonstrated inside an inactive limestone mine. The vehicle completed 40 autonomous hauling cycles across unpaved 12% grade declines with GPS-denied SLAM localization, maintaining sub-15 cm path tracking accuracy in dusty low-light conditions.",
        "key_evidence": "A full-scale engineering prototype autonomous haul truck completed 40 autonomous hauling cycles inside an inactive limestone mine with GPS-denied SLAM.",
        "split": "val"
    },
    {
        "id": "TRL6-BIO-04",
        "trl": 6,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "Non-Human Primate Preclinical Trial of Implantable Neural Decoder Prototype",
        "text": "A fully encapsulated 64-channel wireless neural recording engineering prototype was surgically implanted in rhesus macaques. Over a 90-day relevant animal physiological evaluation, real-time spike sorting enabled kinematic decoding of 2D arm trajectories with a correlation coefficient of r = 0.88, demonstrating system-level stability.",
        "key_evidence": "A fully encapsulated 64-channel wireless neural recording engineering prototype was surgically implanted in rhesus macaques over a 90-day relevant animal evaluation.",
        "split": "test"
    },

    # ==================== TRL 7: Prototype in Operational Environment ====================
    {
        "id": "TRL7-AERO-01",
        "trl": 7,
        "domain": "Aerospace & Defence",
        "title": "Flight Demonstration of Optical Lasercom Terminal on Commercial Airliner",
        "text": "An operational prototype of a free-space optical communications terminal was installed on an active commercial Boeing 777 passenger aircraft during scheduled transcontinental flights. The prototype successfully acquired, tracked, and established a 10 Gbps bidirectional laser downlink with an ESA optical ground station at an altitude of 36,000 feet through turbulent cloud layers, demonstrating operational performance in real flight.",
        "key_evidence": "Installed on an active commercial Boeing 777 passenger aircraft during scheduled flights; established a 10 Gbps bidirectional laser downlink at 36,000 feet.",
        "split": "train"
    },
    {
        "id": "TRL7-ENERGY-02",
        "trl": 7,
        "domain": "Energy & Clean Tech",
        "title": "Operational Grid Demonstration of 5 MW Flow Battery at Substation",
        "text": "A full-scale 5 MW / 20 MWh operational prototype zinc-bromine flow battery was integrated directly into the municipal transmission substation in Austin, Texas. Over 6 months of live operational grid service, the battery executed real-time frequency regulation and peak shaving commands issued by ERCOT, completing 180 full dispatch cycles with 98.4% grid availability.",
        "key_evidence": "Integrated directly into the municipal transmission substation in Austin, Texas; completed 180 full dispatch cycles over 6 months of live operational grid service.",
        "split": "train"
    },
    {
        "id": "TRL7-ROBOT-03",
        "trl": 7,
        "domain": "Robotics & Autonomous Systems",
        "title": "Operational Sea Trials of Autonomous Offshore Inspection Submersible",
        "text": "An operational prototype hybrid autonomous underwater vehicle (AUV) was deployed from a commercial offshore support vessel at the Dogger Bank offshore wind farm in the North Sea. The submersible autonomously inspected 14 monopile foundations in Sea State 4 (waves up to 2.5 meters), executing cathodic protection probing and real-time defect segmentation without umbilical tethering.",
        "key_evidence": "Deployed from a commercial offshore support vessel at the Dogger Bank offshore wind farm; autonomously inspected 14 monopile foundations in Sea State 4.",
        "split": "val"
    },
    {
        "id": "TRL7-BIO-04",
        "trl": 7,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "Multicenter Phase III Clinical Trial of Automated Insulin Delivery Algorithm",
        "text": "An operational system prototype artificial pancreas running predictive low-glucose suspend algorithms was deployed in a randomized multicenter Phase III clinical trial involving 240 Type 1 diabetes patients across 12 hospitals. Over 6 months of unconstrained daily home use, time-in-range (70-180 mg/dL) increased significantly from 61% to 77% with zero severe hypoglycemia events.",
        "key_evidence": "Deployed in a randomized multicenter Phase III clinical trial involving 240 patients over 6 months of unconstrained daily home use.",
        "split": "test"
    },

    # ==================== TRL 8: Actual System Completed & Qualified ====================
    {
        "id": "TRL8-AERO-01",
        "trl": 8,
        "domain": "Aerospace & Defence",
        "title": "FAA Type Certification and Final Qualification of High-Efficiency Turbofan Blades",
        "text": "The final production-standard composite fan blade system completed all formal developmental test and evaluation requirements. The design successfully passed rigorous FAA FAR Part 33 qualification testing, including medium flocking bird ingestion, blade-out containment at 105% redline RPM, and severe icing tunnel compliance. Complete manufacturing drawings and AS9100 quality documentation have been frozen and certified.",
        "key_evidence": "Completed all formal developmental test and evaluation; successfully passed rigorous FAA FAR Part 33 qualification testing including bird ingestion and blade-out.",
        "split": "train"
    },
    {
        "id": "TRL8-BIO-02",
        "trl": 8,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "FDA 510(k) Clearance and IEC 60601-1 Medical Safety Qualification of AI Echocardiogram",
        "text": "The commercial-standard handheld ultrasound hardware and neural ejection fraction analysis software received formal FDA 510(k) clearance (K234190). The complete device successfully passed ISO 13485 medical device quality management audits, IEC 60601-1 electrical safety, and EMC qualification testing. Design freeze, packaging validation, and production assembly lines are fully established.",
        "key_evidence": "Received formal FDA 510(k) clearance; passed ISO 13485 audits, IEC 60601-1 electrical safety, and EMC qualification testing.",
        "split": "train"
    },
    {
        "id": "TRL8-ELEC-03",
        "trl": 8,
        "domain": "Electronics & Semiconductors",
        "title": "AEC-Q100 Grade 0 Qualification of 1200V Silicon Carbide Inverter Module",
        "text": "The final production-grade 1200V SiC power module completed full automotive qualification under AEC-Q100 Grade 0 (-40 deg C to +150 deg C). Testing included 2,000 hours of High Temperature Reverse Bias (HTRB), 1,000 thermal shock cycles, and vibration per ISO 16750-3 with zero parametric drift. The production line at the certified foundry is released for volume manufacturing.",
        "key_evidence": "Completed full automotive qualification under AEC-Q100 Grade 0; 2,000 hours HTRB and 1,000 thermal shock cycles passed with zero parametric drift.",
        "split": "val"
    },
    {
        "id": "TRL8-ENERGY-04",
        "trl": 8,
        "domain": "Energy & Clean Tech",
        "title": "IEC 61400-22 Type Qualification and Pre-Commissioning of 15 MW Wind Nacelle",
        "text": "The series-production 15 MW offshore wind turbine nacelle completed full-scale structural dynamic qualification at the national offshore renewable testing facility. DNV issued the formal A-Design and Type Certificate in accordance with IEC 61400-22 following extreme blade pitch fatigue tests, 100-year storm gale simulations, and grid code compliance verification.",
        "key_evidence": "DNV issued formal A-Design and Type Certificate in accordance with IEC 61400-22 following extreme fatigue tests and grid code compliance.",
        "split": "test"
    },

    # ==================== TRL 9: Actual System Mission Proven / Commercial ====================
    {
        "id": "TRL9-AERO-01",
        "trl": 9,
        "domain": "Aerospace & Defence",
        "title": "Mission Proven Star Tracker Performance across 5 Years of Orbital Service",
        "text": "The autonomous star tracker system has achieved full TRL 9 mission-proven status through continuous operational service aboard 48 commercial telecommunication satellites in geostationary orbit. Over 5.2 million cumulative on-orbit operating hours, the flight units maintained 99.999% attitude determination availability, surviving solar flare proton storms without single-event latchups. Millions of commercial customers rely on these deployed operational units daily.",
        "key_evidence": "Continuous operational service aboard 48 commercial satellites; over 5.2 million cumulative on-orbit operating hours with 99.999% availability.",
        "split": "train"
    },
    {
        "id": "TRL9-ENERGY-02",
        "trl": 9,
        "domain": "Energy & Clean Tech",
        "title": "Commercial Fleet Operations Report: 10,000 MW Global Inverter Deployment",
        "text": "The commercial 250 kW utility string solar inverter has been mass-produced and deployed globally across 120 commercial solar plants in 18 countries, exceeding 10 GW of cumulative operating capacity. Field service logs over 4 continuous years confirm an operational uptime of 99.87% and Mean Time Between Failures (MTBF) exceeding 350,000 hours under extreme desert and coastal environments.",
        "key_evidence": "Mass-produced and deployed globally across 120 commercial plants in 18 countries exceeding 10 GW; 4 continuous years of field operational uptime at 99.87%.",
        "split": "train"
    },
    {
        "id": "TRL9-IT-03",
        "trl": 9,
        "domain": "Information Technology & AI",
        "title": "Global Deployment Statistics of Cloud Speech Recognition Infrastructure",
        "text": "The production transformer speech-to-text inference engine is deployed across 14 distributed data centers worldwide, serving over 2 billion live API requests daily for commercial enterprise clients. Continuous mission operations over 36 consecutive months demonstrated 99.995% service level agreement (SLA) compliance with p99 latency below 120 milliseconds.",
        "key_evidence": "Deployed across 14 data centers worldwide, serving over 2 billion live API requests daily over 36 consecutive months of commercial operations.",
        "split": "val"
    },
    {
        "id": "TRL9-BIO-04",
        "trl": 9,
        "domain": "Biomedical & Pharmaceuticals",
        "title": "Post-Market Surveillance and Commercial Deployment of Robotic Surgical Console",
        "text": "The commercial multi-arm laparoscopic robotic surgery system is installed in over 850 hospitals globally, with more than 350,000 successful clinical procedures completed in routine surgical operations. Five-year post-market surveillance data submitted to health authorities confirms adverse event rates below 0.01%, establishing proven commercial mission operations.",
        "key_evidence": "Installed in over 850 hospitals globally, with more than 350,000 successful clinical procedures completed in routine surgical operations.",
        "split": "test"
    }
]

def get_dataset(split: str = None) -> List[Dict[str, Any]]:
    """Return dataset filtered by split, or full dataset if split is None."""
    if split is None:
        return BENCHMARK_SAMPLES
    return [s for s in BENCHMARK_SAMPLES if s.get("split") == split]
