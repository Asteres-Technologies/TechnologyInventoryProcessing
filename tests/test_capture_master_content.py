"""
This module tests the capture_master_content function from the inventory_processor module.

The purpose is to ensure:
- All of the content is represented in the output.
- All of the row IDs are present and correctly mapped.
- All of the columns are present in the output.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inventory_processor import capture_master_content
import pandas as pd


DATA_DIR = 'data'
INVENTORY_PATH = '../data/INVENTORY.xlsx'

#June 2025 Snapshot Variables
TOTAL_ROWS = 15298
KNOWN_ROW_IDS = [2345, 8762, 12001, 500, 15297, 3012, 9999, 14567, 7123, 10000]

def test_capture_master_content():
    global captured_data
    captured_data = capture_master_content(INVENTORY_PATH, DATA_DIR)
    assert isinstance(captured_data, pd.DataFrame), "Captured data should be a DataFrame"
    assert not captured_data.empty, "Captured data should not be empty"

def test_columns_present():
    expected_columns = [
        "Technology Name", "Tech Producer", "Description", "Existing Technology", 
        "Level One Category", "Level Two Category", "Level Three Category", "TRL", 
        "Level One Functional Category", "Level Two Functional Category"]
    assert all(col in captured_data.columns for col in expected_columns), "Not all expected columns are present"

def test_row_count():
    assert len(captured_data) == TOTAL_ROWS, f"Expected {TOTAL_ROWS} rows, got {len(captured_data)}"
    assert len(captured_data.index.unique()) == TOTAL_ROWS, "Row indices should be unique and match the total row count"
    assert captured_data.index.isin([TOTAL_ROWS-1]).any(), f"Last row ID {TOTAL_ROWS-1} should be present in the DataFrame"

def test_row_ids_are_present():
    for row_id in KNOWN_ROW_IDS:
        assert row_id in captured_data.index, f"Row {row_id} is missing from the captured data"

def test_row_data_correctness():
    row_2345 = {
        "Technology Name": "High Yield, High Efficiency Epitaxial Lift-Off Solar Cells for LILT Applications",
        "Tech Producer": "MicroLink Devices, Inc. (Industry)",
        "Description": "As the world leader in the production of epitaxial lift-off (ELO) inverted metamorphic (IMM) solar cells, MicroLink Devices proposes to develop large-area ELO-IMM solar cell designed specifically for low intensity, low temperature (LILT) space applications. These solar cells will achieve 45% power conversion efficiency (at –125°C and 5.2 AU) with high production yields, enabling substantial solar array costs for future NASA outer planetary space missions. The proposed LILT ELO-IMM solar cells will benefit future NASA missions to the outer solar system where solar cells will operate under LILT conditions. These solar cells will enable substantial solar array cost reductions making them especially suitable for large-scale SEP (solar electric propulsion) spacecrafts operating in LILT conditions. Manufacturers of commercial satellites and unmanned aerial vehicles (UAVs) are interested in MicroLink's low mass and power dense ELO solar cell technology for the potential to reduce costs while improving the efficiency compared to commercially available Ge-based cells. Attractive military and civilian applications include the ability to recharge batteries in remote locations.",
        "Existing Technology": "Yes",
        "Level One Category": "TX03: Aerospace Power and Energy Storage",
        "Level Two Category": "TX03.1: Power Generation and Energy Conversion",
        "Level Three Category": "TX03.1.1: Photovoltaic Electrical Power",
        "TRL": 4,
        "Level One Functional Category": pd.NA,
        "Level Two Functional Category": pd.NA,
    }
    row_8762 = {
        "Technology Name": "Investigation of spin manipulation in phase-engineered monolayer Janus TMDCs for low power device operation in extreme environments",
        "Tech Producer": "University of South Florida-Main Campus (Academia)",
        "Description": "The electron's spin degree of freedom opens pathways to spin electronic (spintronics) devices which require less energy, resulting in high-speed operation in information communication applications. While a notable aspect for terrestrial functions is the enhancement in communication speeds, the real advantage of spintronics comes from its performance in space environments saturated with radiation. Compared to conventional electronics, which focus on measuring and controlling electron charge quantities, alternative devices designed to measure and manipulate electron spin polarization have demonstrated more robust performance in high radiation environments. The proposed project will develop a scalable approach for Janus TMDC 2DLM synthesis for spintronic architectures through ultrahigh vacuum (UHV) molecular beam epitaxy (MBE), high quality material growth. In optimizing a growth process, the effects of structural phase on radiation hardness and spin manipulation will be investigated. The proposed project will generate new understandings into how fundamental process parameters can facilitate the development of phase-engineered 2DLM systems, which exhibit unique spin manipulation and radiation tolerance behaviors. This area remains relatively unexplored due to the complex nature of the proposed studies. The developed process for phase-engineering films within the proposed project plan will introduce 2DLM manufacturing techniques with new ȧngström-precision. In addition, this proposed process will advance the field of spintronics for practical application on future long-term, deep space exploration missions. Furthermore, material characterizations will provide new knowledge on behaviors of phase-tuned films in regards to spin manipulation and radiation hardness. ",
        "Existing Technology": "Yes",
        "Level One Category": "TX08: Sensors and Instruments",
        "Level Two Category": "TX08.1: Remote Sensing Instruments and Sensors",
        "Level Three Category": "TX08.1.2: Electronics",
        "TRL": 2,
        "Level One Functional Category": pd.NA,
        "Level Two Functional Category": pd.NA,
    }

    row_12001 = {
        "Technology Name": "Evidence-based Metrics Toolkit for Measuring Safety and Efficiency in Human-Automation Systems--NNX13AO51G",
        "Tech Producer": "Ames Research Center (NASA Center)",
        "Description": "Specific aims of this proposal are threefold: (1) develop a framework for human-systems integration requirements, (2) identify and develop a metrics criteria in which safety and efficiency can be characterized in human-automation teams, and (3) design, develop, and validate a theoretically-driven, empirically-based metrics toolkit that characterizes the safety and efficiency of human automation interactions. This proposal meets NASA goals and objectives by mitigating the risk of inadequate design of human and automation/robotic integration through the development of safety and efficiency metrics for human-automation systems. The proposal is divided into three primary phases. Phase 1 will consist of synthesizing and translating findings from the extant literature relevant to human automation/robotic integration. The result of this effort will be the development of objective metrics generalizable to individual and team levels that characterize the safety and efficiency of a human automation interaction. The final outcome of Phase 1 will be the development of a human automation interaction metrics (HAIM) toolkit. Phase 2 focused on preparation and execution of subject matter experts (SME) interviews, which will be used to inform the design of the toolkit and selection of metrics. The central outcome of Phase 2 will be the completion of a whitepaper presenting the results of the SME interviews and the implications of these results to the design of the metrics toolkit. Phase 3 will focus on final validation of the metrics toolkit through usability testing using a relevant user group. This will include the design and execution of a set of usability studies aimed at validating the metrics toolkit. The validation studies will focus on testing users progression through the toolkit using a variety of different selection scenarios. The outcome of the proposed effort will provide NASA a set of evidence-based, empirically-validated measurement toolkit containing measures and measuring guidelines for mitigating the risk of inadequate design of human and automation/robotic integration as it pertains to the development of safety and efficiency metrics for human automation systems. This technology is currently in development. When additional publically releasable information becomes available, it will be posted on TechPort.",
        "Existing Technology": "Yes",
        "Level One Category": "TX11: Software, Modeling, and Simulation",
        "Level Two Category": "TX11.2: Modeling",
        "Level Three Category": "TX11.2.3: Human-System Performance Modeling",
        "TRL": 4,
        "Level One Functional Category": pd.NA,
        "Level Two Functional Category": pd.NA,
    }

    row_500 = {
        "Technology Name": pd.NA,
        "Tech Producer": "NEADL (Near Earth Asset Discovery Labs)",
        "Description": "Prospecting firm in the nascent asteroid mining industry. Our goal is to accurately identify near-earth asteroids that are rich in natural resources and, therefore, worth mining. We place a specific emphasis on locating water-rich asteroids.NEADL believes asteroid mining will eventually become a common and necessary practice as humankind makes its inevitable journey beyond Earth. While this may currently sound like something out of a sci-fi novel, several private companies are already planning on exploring near-earth asteroids by the end of 2029.  Our goal is not to compete with these mining companies but instead to provide asteroid miners with accurate insight into which asteroids are actually worth mining.",
        "Existing Technology": "Yes",
        "Level One Category": "TX07: Exploration Destination Systems",
        "Level Two Category": "TX07.1 In-Situ Resource Utilization",
        "Level Three Category": "TX07.1.2\xa0Resource Acquisition, Isolation, and Preparation",
        "TRL": pd.NA,
        "Level One Functional Category": "FN04: Manufacturing",
        "Level Two Functional Category": pd.NA,
    }
    row_15297 = {
        "Technology Name": "Rendezvous & Docking Avionics Unit (RDAU) for MEV",
        "Tech Producer": "Southwest Research Institute (SwRI)",
        "Description": "The MEV can have as many as 3 Kalman filters (KF) running simultaneously – with each one utilizing a different sensor set (LIDAR, IR, or Visible). One KF is designated as primary and is used to autonomously control the MEV during maneuvering from waypoint-to-waypoint and stable positioning/pointing at the hold points. For the two successful MEV dockings the wide field-of-view IR sensor pair was used as the primary sensor set (MEV-1) and the LIDAR was used as the primary sensor (MEV-2).",
        "Existing Technology": "Yes",
        "Level One Category": pd.NA,
        "Level Two Category": pd.NA,
        "Level Three Category": 9,
        "TRL": pd.NA,
        "Level One Functional Category": pd.NA,
        "Level Two Functional Category": pd.NA,
    }

    expected_rows = [row_2345, row_8762, row_12001, row_500, 
                     row_15297]
    for row_id, expected_row in zip(KNOWN_ROW_IDS[0:5], expected_rows):
        captured = captured_data.loc[row_id].to_dict()
        for key, value in expected_row.items():
            if pd.isna(value):
                assert pd.isna(captured[key]), f"Row {row_id} - {key} expected to be NA, got {captured[key]}"
            else:
                if captured[key] != value:
                    print("DEBUG:", repr(captured[key]), repr(value))
                assert captured[key] == value, f"Row {row_id} - {key} mismatch: expected {value}, got {captured[key]}"
