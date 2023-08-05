import numpy as np
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import xlsxwriter
import errno
import os
import shutil
import logging
from Incident import Incident
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from datetime import datetime
from string import ascii_lowercase
from statistics import mean

import time
ELAPSED_TIME = 0

# Fixing:
# FutureWarning:
# - Using an implicitly registered datetime converter for a matplotlib plotting method.
# - The converter was registered by pandas on import.
# - Future versions of pandas will require you to explicitly register matplotlib converters.
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 7)

TIMETABLE_DESC = "This table contains an overview of cycles before and after EVP. Each row differentiates 5 seconds. Colored cells indicate a EV status. EV Accepted: EV request is accepted by STREAMS. EV Running: STREAMS has started to "
CYCLES_DESC = "Displayed are the cycles in the chosen interval. Here you can see the changes made do adapt to the EVP. The cycle in the middle row displays the cycle of the EVP."
PHASEDUR_DESC = "Visualization of each phases' duration in the cycle where the EVP occured. The table describes each phases duration and its duration in comparison with the other cycles phases (in the interval). This is to see how the cycles was modified to work with EVP."
EVOVERTIME_DESC = "Displays information on phase duration in addition to EV overtime in seconds. Below is an overview of all overtime (ETA before Terminated and the opposite) from the whole dataset."

COLOR_SEQUENCE = {
    "1A" : "#3498db", # 1A PETER RIVER
    "1B" : "#f39c12", # 1B ORANGE
    "1C" : "#27ae60", # 1C NEPHRITIS
    "1D" : "#e74c3c", # 1D ALIZARIN
    "1E" : "#9b59b6", # 1E AMETHYST
    "1F" : "#1abc9c", # 1F TURQUOISE

    "2A" : "#3498db", # 2A PETER RIVER
    "2B" : "#f39c12", # 2B ORANGE
    "2C" : "#2ecc71", # 2C EMERALD
    "2D" : "#e74c3c", # 2D ALIZARIN
    "2E" : "#9b59b6", # 2E AMETHYST
    "2F" : "#1abc9c", # 2F TURQUOISE
}

COLOR_STATUS = {
    "accepted"  :   "#3498db",
    "running"   :   "#be2edd",  #2ecc71
    "eta"       :   "#f39c12",
    "cancelled" :   "#e74c3c",  #22a6b3
    "terminated":   "#6ab04c"   #e74c3c
}

LETTERS = {str(index): letter for index, letter in enumerate(ascii_lowercase, start=1)}

i_main = None;
i_det = None;
i_sum = None;
i_vpp = None;
i_io = None;

CSV_MAIN_PATH_GVAL = ""
CSV_DETAILS_PATH_GVAL = ""
CSV_SUMMARY_PATH_GVAL = ""
CSV_VPP_PATH_GVAL = ""
XLSX_IO_PATH_GVAL = ""
INTERSECTION_GVAL = ""
OUTPUT_FOLDER_GVAL = ""
TIMETABLE_INTERVAL_GVAL = 5
NO_CYCLE_INTERVALS_GVAL = 4

VALIDATION_WORKBOOK = None
VALIDATION_WORKSHEET = None
VALIDATION_WORKBOOK_INDEX = 0


#-------------------- TMREVPVIZ FUNCTIONS SETUP ------------------------------

def tmrevpviz_run(CSV_MAIN_PATH_INPUT, CSV_DETAILS_PATH_INPUT, CSV_SUMMARY_PATH_INPUT, CSV_VPP_PATH_INPUT, XLSX_IO_PATH_INPUT, INTERSECTION_INPUT, TIMETABLE_INTERVAL_INPUT, NO_CYCLE_INTERVALS_INPUT, OUTPUT_FOLDER_INPUT, VALIDATE_BOOL):

    global CSV_MAIN_PATH_GVAL
    global CSV_DETAILS_PATH_GVAL
    global CSV_SUMMARY_PATH_GVAL
    global CSV_VPP_PATH_GVAL
    global XLSX_IO_PATH_GVAL
    global INTERSECTION_GVAL
    global OUTPUT_FOLDER_GVAL
    global TIMETABLE_INTERVAL_GVAL
    global NO_CYCLE_INTERVALS_GVAL
    global VALIDATION_WORKBOOK
    global VALIDATION_WORKBOOK_INDEX

    CSV_MAIN_PATH_GVAL = CSV_MAIN_PATH_INPUT
    CSV_DETAILS_PATH_GVAL = CSV_DETAILS_PATH_INPUT
    CSV_SUMMARY_PATH_GVAL = CSV_SUMMARY_PATH_INPUT
    CSV_VPP_PATH_GVAL = CSV_VPP_PATH_INPUT
    XLSX_IO_PATH_GVAL = XLSX_IO_PATH_INPUT
    INTERSECTION_GVAL = INTERSECTION_INPUT
    OUTPUT_FOLDER_GVAL = OUTPUT_FOLDER_INPUT
    TIMETABLE_INTERVAL_GVAL = TIMETABLE_INTERVAL_INPUT
    NO_CYCLE_INTERVALS_GVAL = NO_CYCLE_INTERVALS_INPUT

    global i_main
    global i_det
    global i_sum
    global i_vpp
    global i_io

    global feedback_text

    mkdir_p(OUTPUT_FOLDER_GVAL, 'png')

    logger = logging.getLogger('TMREVPVIZ_ERROR_LOG')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(OUTPUT_FOLDER_GVAL + r'\TMREVPVIZ_ERROR_LOG.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


    #######################################################################
    # ----------------- FETCH CSV FILES------------------------------------
    try:
        i_main = pd.read_csv(CSV_MAIN_PATH_GVAL, skiprows=7)
    except FileNotFoundError as e:
        feedback_text.set("Error: Can't find CSV_MAIN_PATH at file path: '" + CSV_MAIN_PATH_GVAL + "'")
        logger.info("Error: Can't find CSV_MAIN_PATH at file path: '" + CSV_MAIN_PATH_GVAL + "'")
        return

    try:
        i_det = pd.read_csv(CSV_DETAILS_PATH_GVAL)
    except FileNotFoundError as e:
        feedback_text.set("Error: Can't find CSV_DETAILS_PATH at file path: '" + CSV_DETAILS_PATH_GVAL + "'")
        logger.info("Error: Can't find CSV_DETAILS_PATH at file path: '" + CSV_DETAILS_PATH_GVAL + "'")
        return

    try:
        i_sum = pd.read_csv(CSV_SUMMARY_PATH_GVAL)
    except FileNotFoundError as e:
        feedback_text.set("Error: Can't find CSV_SUMMARY_PATH at file path: '" + CSV_SUMMARY_PATH_GVAL + "'")
        logger.info("Error: Can't find CSV_SUMMARY_PATH at file path: '" + CSV_SUMMARY_PATH_GVAL + "'")
        return

    # If validation checkbox is checked, check for files
    print("VALIDATE_BOOL: ", VALIDATE_BOOL)
    if VALIDATE_BOOL:
        try:
            i_vpp = pd.read_csv(CSV_VPP_PATH_GVAL)
        except FileNotFoundError as e:
            feedback_text.set("Error: Can't find CSV_VPP_PATH at file path: '" + CSV_VPP_PATH_GVAL + "'")
            logger.info("Error: Can't find CSV_VPP_PATH at file path: '" + CSV_VPP_PATH_GVAL + "'")
            return

        try:
            i_io = pd.read_excel(XLSX_IO_PATH_GVAL)
        except FileNotFoundError as e:
            feedback_text.set("Error: Can't find XLSX_IO_PATH at file path: '" + XLSX_IO_PATH_GVAL + "'")
            logger.info("Error: Can't find XLSX_IO_PATH at file path: '" + XLSX_IO_PATH_GVAL + "'")
            return
    # ----------------- FETCH CSV FILES END--------------------------------
    #######################################################################


    i_main['Time'] = pd.to_datetime(i_main['Time'], format='%d/%m/%Y %I:%M:%S %p')
        # i_det
    i_det['Update Time'] = pd.to_datetime(i_det['Update Time'], format='%d/%m/%Y %I:%M:%S %p')
    i_det['ETA'] = pd.to_datetime(i_det['ETA'], format='%d/%m/%Y %I:%M:%S %p')
    i_det.sort_values(by="Update Time", inplace=True)

        # i_sum
    i_sum['Running Start Time'] = pd.to_datetime(i_sum['Running Start Time'], format='%d/%m/%Y %I:%M:%S %p')
    i_sum['ETA at Run Start'] = pd.to_datetime(i_sum['ETA at Run Start'], format='%d/%m/%Y %I:%M:%S %p')
    i_sum['Terminated/Cancelled Time'] = pd.to_datetime(i_sum['Terminated/Cancelled Time'], format='%d/%m/%Y %I:%M:%S %p')

    incident_ids = get_incident_ids_in_csv()
    print("Number of ids: {}".format(len(incident_ids))) #INCIDENTLOG
    if len(incident_ids) == 0:
        feedback_text.set("Error: Zero ids fetched from file {}".format(CSV_DETAILS_PATH_GVAL))
        print("Error: Zero phases fetched from dataframe - get_cycle_phase_values")

    if VALIDATE_BOOL:
        VALIDATION_WORKBOOK = xlsxwriter.Workbook(OUTPUT_FOLDER_GVAL + '/{}_VALIDATION.xlsx'.format(INTERSECTION_GVAL))
        VALIDATION_WORKSHEET = VALIDATION_WORKBOOK.add_worksheet('VALIDATION')
        VALIDATION_WORKSHEET.write(VALIDATION_WORKBOOK_INDEX, 0, 'ID')
        VALIDATION_WORKSHEET.write(VALIDATION_WORKBOOK_INDEX, 1, 'CYCLE START')
        VALIDATION_WORKSHEET.write(VALIDATION_WORKBOOK_INDEX, 2, 'ANOMALY ID')
        VALIDATION_WORKSHEET.write(VALIDATION_WORKBOOK_INDEX, 3, 'ANOMALY COMMENT')
        VALIDATION_WORKBOOK_INDEX += 1

    incident_complete_count = 0
    for incident_id in incident_ids:
        create_incident_workbook(INTERSECTION_GVAL, incident_id, VALIDATE_BOOL, logger)
        incident_complete_count += 1
        feedback_text.set("Visualized {}/{} incidents.".format(incident_complete_count, len(incident_ids)))


    shutil.rmtree(OUTPUT_FOLDER_GVAL + '/png', ignore_errors=True)
    VALIDATION_WORKBOOK.close()

    if VALIDATE_BOOL:
        generate_anomaly_statistics(INTERSECTION_GVAL)

    print("All workbooks completed!")
    feedback_text.set("All workbooks completed!")

def mkdir_p(path, folder):
    path = path + '/' + folder
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            global feedback_text
            feedback_text.set("Error: Tried to create folder: '{}', but was not allowed by the system.".format(folder))
            raise

def get_incident_ids_in_csv():
    return i_det["Incident Id"].unique().tolist()

def calculate_deg_for_datetime(cycle_start, end_time, s_array):
    timediff = (end_time - cycle_start).total_seconds()
    if timediff < 0 or timediff > sum(s_array):
        return False
    else:
        return (90 - 360*(timediff/sum(s_array)))

def visualize_incident_timetable(incident, workbook, formatting_dict):
    worksheet = workbook.add_worksheet('Time Table')

    # Fetch interval
    incident_id = incident.get_incident_id()
    i_interval = incident.get_incident_cycle_interval()

    if type(i_interval) == bool:
        if (i_interval == False):
            print("Error: Trouble fetching incident interval - visualize_incident_timetable")
            return False

    # Fetch EV interaction cycle
    i_cycle_no = i_interval.iloc[np.floor(len(i_interval.index)/2).astype(int)]["Cycle No"]

    # Loop through cycles in interval and add df to list
    timetable_df_list = []
    for c_i in range(1, i_interval.shape[0]):

        # Fetch cycle info
        c_info = i_interval.iloc[c_i-1]
        c_start = c_info["Time"]
        c_end = c_start + pd.Timedelta(seconds=c_info["Cycle Length"]-1)
        labels, phases = incident.get_cycle_phase_values(c_info)

        # Create df to insert time data
        t_df = pd.DataFrame(columns=["letter1", "letter2", "time", "phase", "format"])

        # Fetch xslxwriter column data
        letter_index_1 = (2*c_i)-1
        letter_index_2 = letter_index_1+1

        # Loop through phases in cycle and add time and phases into DF
        current_time = c_start
        for p_i in range(0, len(phases)):
            for sec in range(0, np.ceil(phases[p_i]/TIMETABLE_INTERVAL_GVAL).astype(int)+1):
                time = current_time + pd.Timedelta(seconds=sec*TIMETABLE_INTERVAL_GVAL)
                if time >= current_time + pd.Timedelta(seconds=phases[p_i]):
                    t_df.loc[t_df.shape[0]] = [letter_index_1, letter_index_2, current_time + pd.Timedelta(seconds=phases[p_i]-1), labels[p_i], "Standard Date End"]
                else:
                    t_df.loc[t_df.shape[0]] = [letter_index_1, letter_index_2, time, labels[p_i], "Standard Date"]

            current_time += pd.Timedelta(seconds=phases[p_i])

        timetable_df_list.append(t_df)

    # Populate status_df
    s_df = incident.get_ev_status_datetimes()

    # Insert status datetimes into time lists
    li_i = 0
    while ((li_i < len(timetable_df_list)) and (len(s_df) > 0)):
        t_list = timetable_df_list[li_i]
        li_s = t_list.iloc[0]["time"]
        li_e = t_list.iloc[t_list.shape[0]-1]["time"]

        # Check if first status element datetime is within list datetime
        if (li_s < s_df.iloc[0]["time"]) and (s_df.iloc[0]["time"] < li_e):

            prev_row = t_list.iloc[0]
            r_index = 0
            li_len = t_list.shape[0]
            while r_index < li_len:

                row = t_list.iloc[r_index]
                if row["time"] == s_df.iloc[0]["time"]:
                    # If datetime already exists in statuses - add formatting
                    timetable_df_list[li_i].at[r_index, "format"] = s_df.iloc[0]["status"]
                    # Drop first element in status list and reset index
                    s_df = s_df.drop([0], axis=0).reset_index(drop=True)
                    # Reduce li_i to check the same list
                    li_i -= 1
                    break

                elif (prev_row["time"] < s_df.iloc[0]["time"]) and (s_df.iloc[0]["time"] < row["time"]):
                    # If datetime is between two datetimes, insert between
                    line = pd.DataFrame({"letter1":prev_row["letter1"], "letter2":prev_row["letter2"], "time": s_df.iloc[0]["time"], "phase": prev_row["phase"], "format":s_df.iloc[0]["status"]}, index=[r_index])
                    timetable_df_list[li_i] = pd.concat([timetable_df_list[li_i].iloc[:r_index], line, timetable_df_list[li_i].iloc[r_index:]], sort=False).reset_index(drop=True)
                    # Drop first element in status list and reset index
                    s_df = s_df.drop([0], axis=0).reset_index(drop=True)
                    # Reduce li_i to check the same list
                    li_i -= 1
                    break

                prev_row = row
                li_len = t_list.shape[0]
                r_index += 1

        li_i += 1

    # Increment and write to Excel-sheet
    for list_index in range(0, len(timetable_df_list)):
        timetable_df_list[list_index].index = timetable_df_list[list_index].index + 2

        # Create merge information
        merge_from_letter = timetable_df_list[list_index].iloc[0]["letter2"]
        merge_from_row = 2
        prev_phase = timetable_df_list[0].iloc[0]["phase"]

        for index, row in timetable_df_list[list_index].iterrows():
            # Fetch necessary Excel information
            letter1 = row["letter1"]
            letter2 = row["letter2"]
            # Write column names
            worksheet.write(1, letter1, 'Time', formatting_dict['Standard Date'])
            worksheet.write(1, letter2, 'Phase', formatting_dict['Standard'])

            # Fetch row information
            row_number = index
            time = row["time"]
            phase = row["phase"]
            cell_format = row["format"]

            # Write datetime to Excel
            worksheet.write(row_number, letter1, time, formatting_dict[cell_format])
            worksheet.write(row_number, letter2, phase, formatting_dict['Standard'])

            # Merge phase-columns if new phase has started
            if (phase != prev_phase):
                worksheet.merge_range(merge_from_row, merge_from_letter, index-1, merge_from_letter, prev_phase, formatting_dict['Merge Format'])
                merge_from_row = index
            if (index-1 == timetable_df_list[list_index].shape[0]):
                worksheet.merge_range(merge_from_row, merge_from_letter, index, merge_from_letter, prev_phase, formatting_dict['Merge Format'])
                merge_from_row = index

            # Update merge information for next iteration
            prev_phase = phase

    # Write explanation cells
    info_i = i_interval.shape[0]*2+1
    worksheet.write(3, info_i, '  ', formatting_dict['EV Accepted'])
    worksheet.write(3, info_i+1, 'EV Accepted')

    worksheet.write(4, info_i, '  ', formatting_dict['EV Running'])
    worksheet.write(4, info_i+1, 'EV Running')

    worksheet.write(5, info_i, '  ', formatting_dict['EV ETA'])
    worksheet.write(5, info_i+1, 'EV ETA')

    worksheet.write(6, info_i, '  ', formatting_dict['EV Terminated'])
    worksheet.write(6, info_i+1, 'EV Terminated')

    worksheet.write(7, info_i, '  ', formatting_dict['EV Cancelled'])
    worksheet.write(7, info_i+1, 'EV Cancelled')

    worksheet.write(9, info_i, TIMETABLE_DESC)

    print('Cycles added to workbook.')
    return workbook

def visualize_cycle_in_excel(incident, workbook, formatting_dict):
    worksheet = workbook.add_worksheet('Sequence')
    worksheet.set_column(0, NO_CYCLE_INTERVALS_GVAL, 40)
    worksheet.set_default_row(215)

    incident_id = incident.get_incident_id()

    sheet_cols = []
    sheet_rows = []

    col_loop_val = 0
    row_loop_val = 0
    while (len(sheet_cols) < (NO_CYCLE_INTERVALS_GVAL*2)+1):
        sheet_cols.append(col_loop_val)
        sheet_rows.append(row_loop_val)

        if (len(sheet_cols) == NO_CYCLE_INTERVALS_GVAL):
            sheet_cols.append(1)
            col_loop_val = 0
        else:
            col_loop_val += 1

        if (len(sheet_rows) == NO_CYCLE_INTERVALS_GVAL):
            sheet_rows.append(1)
            row_loop_val = 2


    rows = incident.get_incident_cycle_interval()
    count = 0
    for index, row in rows.iterrows():
        c_no = row["Cycle No"]
        c_time = row["Time"]
        c_len = row["Cycle Length"]
        combo = row["Phase Combo"]

        # Prep vals for pie chart
        labels = []
        phases = []
        try:
            labels, phases = incident.get_cycle_phase_values(row)
        except Exception as e:
          global feedback_text
          feedback_text.set("Error: Problems fetching phases for incident id {}".format(incident_id))
          print("Error:", e)
          return False
          raise

        # Construct pie chart
        explode = [0.03] * len(phases)
        fig1, ax = plt.subplots(figsize=(5, 5))
        wedges = ax.pie(phases, labels=labels, explode=explode, autopct=lambda p : '{:.0f}s'.format(p * sum(phases)/100), startangle=90, counterclock=False)

        for pie_wedge in wedges[0]:
            pie_wedge.set_edgecolor('white')
            pie_wedge.set_facecolor(COLOR_SEQUENCE[pie_wedge.get_label()])

        ax.axis('equal')
        ax.set(title="Cycle #{} at {}".format(c_no, c_time))
        global OUTPUT_FOLDER_GVAL
        plt.savefig(OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id))
        size = fig1.get_size_inches()*fig1.dpi

        worksheet.insert_image(sheet_rows[count],
                               sheet_cols[count],
                               OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id),
                               {'x_scale': 0.6, 'y_scale': 0.6})
        count += 1

        worksheet.write(1, 3, CYCLES_DESC)
        plt.clf()
        plt.close()

    print("Sequence added to workbook.")
    return workbook

def visualize_phase_durations(incident, workbook, formatting_dict):
    worksheet = workbook.add_worksheet('Phase durations')
    # Extract values
    incident_id = incident.get_incident_id()
    row = incident.get_intervention_main_row()
    c_no = row["Cycle No"]
    c_time = row["Time"]
    c_len = row["Cycle Length"]
    combo = row["Phase Combo"]

    labels = []
    phases = []
    try:
        labels = incident.get_incident_cycle_phase_labels().copy()
        phases = incident.get_incident_cycle_phase_durations().copy()
    except Exception as e:
      global feedback_text
      feedback_text.set("Error: Problems fetching phases for incident id {}".format(incident_id))
      print("Error: Zero phases fetched from dataframe - get_cycle_phase_values")
      return False
      raise
    labels.reverse()
    phases.reverse()

    # Calculate deg for statuses
    eta = incident.get_ev_eta()
    ev_complete = incident.get_ev_complete_time()
    ev_complete_state = incident.get_ev_complete_time_state()

    timediff_deg_eta = calculate_deg_for_datetime(c_time, eta, phases)
    timediff_deg_complete = calculate_deg_for_datetime(c_time, ev_complete, phases)

    ev_status_times = [eta, ev_complete]
    ev_stats_labels = ["EV ETA", ev_complete_state]
    ev_stats_deg = [timediff_deg_eta, timediff_deg_complete]
    ev_stats_mid_deg = 0
    ev_overtime_s = 0

    # Construct pie chart
    fig, ax = plt.subplots(figsize=(8, 4))
    size = .5
        # Plot cycle
    wedges = ax.pie(phases,
           labels=labels,
           autopct=lambda p : '{:.0f}s'.format(p * sum(phases)/100),
           startangle=90,
           wedgeprops=dict(width=1, edgecolor='w'))

    for pie_wedge in wedges[0]:
        pie_wedge.set_edgecolor('white')
        pie_wedge.set_facecolor(COLOR_SEQUENCE[pie_wedge.get_label()])

        # Plot overtime interval
    patches = []
    if timediff_deg_eta < timediff_deg_complete:
        wedge = Wedge((0, 0), 1.2, timediff_deg_eta, timediff_deg_complete, width=.5, label=["OVERTIME"])
        wedge.set_label("OVERTIME")
        ev_stats_mid_deg = ((timediff_deg_complete - timediff_deg_eta) / 2) + timediff_deg_eta
        ev_overtime_s = (eta - ev_complete).total_seconds()
    else:
        wedge = Wedge((0, 0), 1.2, timediff_deg_complete, timediff_deg_eta, width=.5, label=["OVERTIME"])
        wedge.set_label("OVERTIME")
        ev_stats_mid_deg = ((timediff_deg_eta - timediff_deg_complete) / 2) + timediff_deg_complete
        ev_overtime_s = (ev_complete - eta).total_seconds()

    patches.append(wedge)
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)

    # Annotations props
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    # Plot annotation
    for i in range(0, len(ev_stats_deg)):
        if ev_stats_deg[i] != False:
            y = np.sin(np.deg2rad(ev_stats_deg[i]))
            x = np.cos(np.deg2rad(ev_stats_deg[i]))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ev_stats_deg[i])
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate("{} [{}]".format(ev_stats_labels[i], ev_status_times[i].strftime('%H:%M:%S')),
                        xy=(x, y),
                        xytext=(x*1.50, 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

    # Plot overtime seconds annotation

    y_mid = np.sin(np.deg2rad(ev_stats_mid_deg))
    x_mid = np.cos(np.deg2rad(ev_stats_mid_deg))
    ax.annotate('{}s'.format(int(ev_overtime_s)), xy=(x_mid, y_mid), xycoords='data', xytext=(x*25, 25*y), textcoords='offset points')

    ax.set(aspect="equal")
    plt.title("Cycle Overtime #{} \nStart: {}\nEnd: {}".format(c_no, c_time, c_time + pd.Timedelta(seconds=c_len)), y=1.07)
    global OUTPUT_FOLDER_GVAL
    try:
        plt.savefig(OUTPUT_FOLDER_GVAL + '/png/EV_Cycle_{}_{}_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id))
    except Exception as e:
        print("Error adding image to workbook.")
        return workbook
    worksheet.insert_image(2,
                           2,
                           OUTPUT_FOLDER_GVAL + '/png/EV_Cycle_{}_{}_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id), {'x_scale': 0.8, 'y_scale': 0.8})

    plt.clf()
    plt.close()

    worksheet.write("M3", "Phase", formatting_dict['Standard'])
    worksheet.write("N3", "Duration", formatting_dict['Standard'])
    worksheet.write("O3", "Difference", formatting_dict['Standard'])
    worksheet.write("P3", "Avg", formatting_dict['Standard'])
    worksheet.write("Q3", "%", formatting_dict['Standard'])

    timecomp = incident.get_incident_cycle_timecomp()

    for i in range(0, len(timecomp)):
        worksheet.write("M{}".format(i+4), timecomp[i][0])
        worksheet.write("N{}".format(i+4), timecomp[i][1])
        worksheet.write("O{}".format(i+4), timecomp[i][2])
        worksheet.write("P{}".format(i+4), timecomp[i][3])
        worksheet.write("Q{}".format(i+4), timecomp[i][4])

    worksheet.write("M16", PHASEDUR_DESC)

    print("Phase duration added to workbook.")
    return workbook

def visualize_ev_overtime_in_excel(incident, workbook, formatting_dict):
    worksheet = workbook.add_worksheet('EV Overtime')
    # ------------------------------------------------------------------------------
    # ----------------------------- EV STATUSES ------------------------------------
    # ------------------------------------------------------------------------------


    # Extract values
    incident_id = incident.get_incident_id()
    row = incident.get_intervention_main_row()
    c_no = row["Cycle No"]
    c_time = row["Time"]
    c_len = row["Cycle Length"]
    combo = row["Phase Combo"]

    labels = []
    phases = []
    try:
        labels = incident.get_incident_cycle_phase_labels().copy()
        phases = incident.get_incident_cycle_phase_durations().copy()
    except Exception as e:
      global feedback_text
      feedback_text.set("Error: Problems fetching phases for incident id {}".format(incident_id))
      print("Error: Zero phases fetched from dataframe - get_cycle_phase_values")
      return False
      raise
    labels.reverse()
    phases.reverse()

    # Calculate deg for statuses
    ev_status_times_df = incident.get_ev_status_datetimes()
    ev_status_times = []
    ev_stats_deg = []
    ev_stats_labels = []
    for i in range(0, len(ev_status_times_df)):
        ev_stats_labels.append(ev_status_times_df.iloc[i]["status"])
        ev_status_times.append(ev_status_times_df.iloc[i]["time"])
        timediff_deg = calculate_deg_for_datetime(c_time, ev_status_times_df.iloc[i]["time"], phases)
        ev_stats_deg.append(timediff_deg)

    # Construct pie chart
    explode = [0.03] * len(phases)
    fig1, ax = plt.subplots(figsize=(9, 5))
    wedges_texts = ax.pie(phases,
                labels=labels,
                explode=explode,
                autopct=lambda p : '{:.0f}s'.format(p * sum(phases)/100),
                startangle=90)


    for pie_wedge in wedges_texts[0]:
        pie_wedge.set_edgecolor('white')
        pie_wedge.set_facecolor(COLOR_SEQUENCE[pie_wedge.get_label()])

    wedges = wedges_texts[0]
    texts = wedges_texts[1]

    # Annotations props
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    # Plot annotation
    for i in range(0, len(ev_stats_deg)):
        if ev_stats_deg[i] != False:
            y = np.sin(np.deg2rad(ev_stats_deg[i]))
            x = np.cos(np.deg2rad(ev_stats_deg[i]))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ev_stats_deg[i])
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate("{} [{}]".format(ev_stats_labels[i], ev_status_times[i].strftime('%H:%M:%S')), xy=(x, y), xytext=(x*1.50, 1.3*y),
                         horizontalalignment=horizontalalignment, **kw)

    ax.axis('equal')
    plt.title("Cycle #{} \nStart: {}\nEnd: {}".format(c_no, c_time, c_time + pd.Timedelta(seconds=c_len)), y=1.1)
    global OUTPUT_FOLDER_GVAL
    try:
        plt.savefig(OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_status_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id))
    except Exception as e:
        print("Error adding image to workbook.")
        return workbook

    worksheet.insert_image('B2',
                           OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_status_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id), {'x_scale': 0.7, 'y_scale': 0.7})
    plt.clf()
    plt.close()

    # ------------------------------------------------------------------------------
    # ----------------------------- EV OVERTIME ------------------------------------
    # ------------------------------------------------------------------------------

    # Calculate deg for statuses
    eta = incident.get_ev_eta()
    ev_complete = incident.get_ev_complete_time()
    timediff_deg_eta = calculate_deg_for_datetime(c_time, eta, phases)
    timediff_deg_complete = calculate_deg_for_datetime(c_time, ev_complete, phases)

    ev_status_times = [eta, ev_complete]
    ev_stats_labels = ["EV ETA", "EV Terminated"]
    ev_stats_deg = [timediff_deg_eta, timediff_deg_complete]
    ev_stats_mid_deg = 0
    ev_overtime_s = 0

    # Construct pie chart
    fig, ax = plt.subplots(figsize=(9, 5))
    size = .5
        # Plot cycle
    wedges = ax.pie(phases,
           labels=labels,
           autopct=lambda p : '{:.0f}s'.format(p * sum(phases)/100),
           startangle=90,
           wedgeprops=dict(width=1, edgecolor='w'))

    for pie_wedge in wedges[0]:
        pie_wedge.set_edgecolor('white')
        pie_wedge.set_facecolor(COLOR_SEQUENCE[pie_wedge.get_label()])

        # Plot overtime interval
    patches = []
    if timediff_deg_eta < timediff_deg_complete:
        wedge = Wedge((0, 0), 1.2, timediff_deg_eta, timediff_deg_complete, width=.5, label=["OVERTIME"])
        wedge.set_label("OVERTIME")
        ev_stats_mid_deg = ((timediff_deg_complete - timediff_deg_eta) / 2) + timediff_deg_eta
        ev_overtime_s = (eta - ev_complete).total_seconds()
    else:
        wedge = Wedge((0, 0), 1.2, timediff_deg_complete, timediff_deg_eta, width=.5, label=["OVERTIME"])
        wedge.set_label("OVERTIME")
        ev_stats_mid_deg = ((timediff_deg_eta - timediff_deg_complete) / 2) + timediff_deg_complete
        ev_overtime_s = (ev_complete - eta).total_seconds()

    patches.append(wedge)
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)

    # Annotations props
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    # Plot annotation
    for i in range(0, len(ev_stats_deg)):
        if ev_stats_deg[i] != False:
            y = np.sin(np.deg2rad(ev_stats_deg[i]))
            x = np.cos(np.deg2rad(ev_stats_deg[i]))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ev_stats_deg[i])
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate("{} [{}]".format(ev_stats_labels[i], ev_status_times[i].strftime('%H:%M:%S')),
                        xy=(x, y),
                        xytext=(x*1.50, 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

    # Plot overtime seconds annotation

    y_mid = np.sin(np.deg2rad(ev_stats_mid_deg))
    x_mid = np.cos(np.deg2rad(ev_stats_mid_deg))
    ax.annotate('{}s'.format(int(ev_overtime_s)), xy=(x_mid, y_mid), xycoords='data', xytext=(x*25, 25*y), textcoords='offset points')

    ax.set(aspect="equal")
    plt.title("Cycle Overtime #{} \nStart: {}\nEnd: {}".format(c_no, c_time, c_time + pd.Timedelta(seconds=c_len)), y=1.07)
    plt.savefig(OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id))

    worksheet.insert_image('L2',
                           OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"), incident_id), {'x_scale': 0.7, 'y_scale': 0.7})

    plt.clf()
    plt.close()
    # ------------------------------------------------------------------------------
    # ----------------------------- EV AVG OVERTIME ------------------------------------
    # ------------------------------------------------------------------------------
    x = []
    y = []
    for index, row in i_sum.iterrows():
        if not pd.isnull(row["Running Start Time"]):
            y.append((row["Terminated/Cancelled Time"] - row["ETA at Run Start"]).total_seconds())
            x.append(row["Running Start Time"])

    fig, ax = plt.subplots()
    ax.bar(x, y, width=0.05)
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.set_title('EV Overtime')
    plt.savefig(OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_avg_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"),incident_id))

    worksheet.insert_image('B20',
                           OUTPUT_FOLDER_GVAL + '/png/Cycle_{}_{}_ev_avg_overtime_{}.png'.format(c_no, c_time.strftime("%H-%M-%S"),incident_id))


    plt.clf()
    plt.close()
    avg_overtime = mean(y)
    worksheet.write('L20', 'Avg. overtime: ')
    worksheet.write('L21', '{:.2f}'.format(avg_overtime))

    worksheet.write('L23', EVOVERTIME_DESC)

    print("EV avg overtime added to workbook")
    return workbook

def generate_anomaly_statistics(INTERSECTION):
    global OUTPUT_FOLDER_GVAL
    df = pd.read_excel(OUTPUT_FOLDER_GVAL + '/{}_VALIDATION.xlsx'.format(INTERSECTION))
    df['CYCLE START'] = pd.to_datetime(df['CYCLE START'], format='%d/%m/%Y %I:%M:%S %p')

    workbook = xlsxwriter.Workbook(OUTPUT_FOLDER_GVAL + '/{}_VALIDATION_STATISTICS.xlsx'.format(INTERSECTION))

    worksheet = workbook.add_worksheet('Statistics')
    bold_format = workbook.add_format({
        "bold" : True,
    })
    worksheet.write(0, 0, 'INTERVAL', bold_format)
    worksheet.write(0, 1, 'ANOMALY COUNT', bold_format)
    worksheet.write(0, 4, 'INTERVAL', bold_format)
    worksheet.write(0, 5, 'ANOMALY COUNT (A)', bold_format)
    worksheet.write(0, 8, 'INTERVAL', bold_format)
    worksheet.write(0, 9, 'ANOMALY COUNT (B)', bold_format)
    worksheet.write(0, 12, 'INTERVAL', bold_format)
    worksheet.write(0, 13, 'ANOMALY COUNT (D)', bold_format)
    worksheet.write(14, 0, 'ID', bold_format)
    worksheet.write(14, 1, 'Total count', bold_format)
    worksheet.write(15, 0, 'A', bold_format)
    worksheet.write(16, 0, 'B', bold_format)
    worksheet.write(17, 0, 'C', bold_format)
    worksheet.write(15, 4, 'The day is grouped into intervals of 3 hours. All recorded potential anomalies are counted')
    worksheet.write(16, 4, 'and added to the corresponding interval. The first table (top-left) gives an overview of all')
    worksheet.write(17, 4, 'potential anomalies, and the three next to it are specified to one anomaly type (ID).')
    worksheet.write(18, 4, 'To the left, there is also a list of the total count of the different types of anomalies.')

    a_count = len(df[df['ANOMALY ID'] == 'A'])
    b_count = len(df[df['ANOMALY ID'] == 'B'])
    d_count = len(df[df['ANOMALY ID'] == 'D'])

    worksheet.write(15, 1, a_count)
    worksheet.write(16, 1, b_count)
    worksheet.write(17, 1, d_count)

    tdf = df.groupby(pd.Grouper(key='CYCLE START')).count()
    tdf.sort_values(by='ID', ascending=False)
    tdf = tdf.reset_index()
    tdf["HOUR"] = tdf["CYCLE START"].dt.hour
    tdf = tdf.drop("CYCLE START", axis = 1)
    tdf = tdf.set_index("HOUR")
    tdf = tdf.drop(["ANOMALY ID", "ANOMALY COMMENT"], axis = 1)
    tdf = tdf.sort_index()
    tdf2 = tdf.groupby(tdf.index//3).sum()
    tdf2["INTERVAL"] = pd.cut(tdf2.index, bins = 8, labels = ["0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-00"])
    tdf2 = tdf2.set_index("INTERVAL")
    tdf2 = tdf2.rename(columns= {"HOUR": "HOUR", "ID": "ANOMALY COUNT"}, level=0)

    row_i = 1
    for i, v in tdf2.iterrows():
        print(i, v)
        worksheet.write(row_i, 0, i)
        worksheet.write(row_i, 1, v['ANOMALY COUNT'])
        row_i += 1

    anomaly_types = ['A', 'B', 'D']

    row_i = 1
    col_i = 4
    for i in range(len(anomaly_types)):
        a_id = anomaly_types[i]

        id_df = df[df["ANOMALY ID"] == a_id]
        fid_df = id_df.groupby(pd.Grouper(key='CYCLE START')).count()
        fid_df.sort_values(by='ID', ascending=False)

        fid_df = fid_df.reset_index()
        fid_df["HOUR"] = fid_df["CYCLE START"].dt.hour
        fid_df = fid_df.drop("CYCLE START", axis = 1)
        fid_df = fid_df.set_index("HOUR")
        fid_df = fid_df.drop(["ANOMALY ID", "ANOMALY COMMENT"], axis = 1)
        fid_df = fid_df.sort_index()
        fid_df2 = fid_df.groupby(fid_df.index//3).sum()
        fid_df2["INTERVAL"] = pd.cut(fid_df2.index, bins = 8, labels = ["0-3", "3-6", "6-9", "9-12", "12-15", "15-18", "18-21", "21-00"])
        fid_df2 = fid_df2.set_index("INTERVAL")
        fid_df2 = fid_df2.rename(columns= {"HOUR": "HOUR", "ID": "ANOMALY COUNT ({})".format(a_id)}, level=0)

        for i, v in fid_df2.iterrows():
            print(i, v)
            worksheet.write(row_i, col_i, i)
            worksheet.write(row_i, col_i+1, v["ANOMALY COUNT ({})".format(a_id)])
            row_i += 1

        row_i = 1
        col_i += 4

    workbook.close()

def create_incident_workbook(INTERSECTION, incident_id, VALIDATE_BOOL, logger):

    global VALIDATION_WORKBOOK
    global VALIDATION_WORKBOOK_INDEX

    print("Incident ID: ", incident_id)

    incident = Incident(incident_id, i_det[i_det["Incident Id"] == incident_id], i_main, NO_CYCLE_INTERVALS_GVAL, logger)
    if (incident.get_is_complete()):

        global INTERSECTION_GVAL
        global OUTPUT_FOLDER_GVAL

        workbook = xlsxwriter.Workbook(OUTPUT_FOLDER_GVAL + '/VISUALIZED_{}_{}.xlsx'.format(INTERSECTION_GVAL, incident_id))

        format_standard = workbook.add_format({
            "bold" : False,
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_standard = workbook.add_format({
            "num_format": "hh:mm:ss",
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_end = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : "#FFFF00",
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_accepted = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : COLOR_STATUS["accepted"],
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_running = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : COLOR_STATUS["running"],
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_eta = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : COLOR_STATUS["eta"],
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_cancelled = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : COLOR_STATUS["cancelled"],
            "border" : 2,
            "border_color" : "#000000"
        })
        date_format_terminated = workbook.add_format({
            "num_format": "hh:mm:ss",
            "bg_color" : COLOR_STATUS["terminated"],
            "border" : 2,
            "border_color" : "#000000"
        })
        merge_format = workbook.add_format({
            "bg_color" : "#FFFFFF",
            'font' : 24,
            'bold': 1,
            'border': 2,
            'align': 'center',
            'valign': 'vcenter'
        })
        text_wrap_format = workbook.add_format({
            'text_wrap': True
        })

        formatting_dict = {
            "Merge Format" : merge_format,
            "Standard" : format_standard,
            "Standard Date" : date_format_standard,
            "Standard Date End" : date_format_end,
            "EV Accepted" : date_format_accepted,
            "EV Running" : date_format_running,
            "EV ETA" : date_format_eta,
            "EV Cancelled": date_format_cancelled,
            "EV Terminated": date_format_terminated,
            'Text Wrap': text_wrap_format
        }

        workbook = visualize_incident_timetable(incident, workbook, formatting_dict)

        if (workbook == False):
            return False

        workbook = visualize_cycle_in_excel(incident, workbook, formatting_dict)
        workbook = visualize_phase_durations(incident, workbook, formatting_dict)
        workbook = visualize_ev_overtime_in_excel(incident, workbook, formatting_dict)

        if VALIDATE_BOOL:
            VALIDATION_WORKBOOK, VALIDATION_WORKBOOK_INDEX = incident.get_intersection_validation(i_vpp, i_io, VALIDATION_WORKBOOK, VALIDATION_WORKBOOK_INDEX)

        workbook.close()


#-------------------- TKINTER SETUP ------------------------------
TK_FRAME_WIDTH = 800
TK_FRAME_HEIGHT = 400

window = tk.Tk()
window.title("TMR Anomaly Detection")
window.geometry(str(TK_FRAME_WIDTH) + 'x' + str(TK_FRAME_HEIGHT))
window.configure(background = "#00817d")
window.iconbitmap(os.path.dirname(os.path.abspath(__file__)) + r'\res\logo.ico')

def set_path_to_file(textfield):
    path = askopenfilename()
    textfield.insert(0, path)

def set_path_directory(textfield):
    directoy_path = askdirectory()
    textfield.insert(0, directoy_path)

def tmrevpviz_init():
    global ELAPSED_TIME
    ELAPSED_TIME = time.time()
    tmrevpviz_run(  CSV_MAIN_PATH.get(),
                CSV_DETAILS_PATH.get(),
                CSV_SUMMARY_PATH.get(),
                CSV_VPP_PATH.get(),
                XLSX_IO_PATH.get(),
                INTERSECTION.get(),
                int(TIMETABLE_INTERVAL.get()),
                int(NO_CYCLE_INTERVALS.get()),
                OUTPUT_FOLDER.get(),
                validate_bool.get())
    print("--- %s seconds ---" % (time.time() - ELAPSED_TIME))


tk.Label(window,
         text="CSV_MAIN_PATH",  bg="#00817d", fg="white", anchor="e").grid(row=0)
tk.Label(window,
         text="CSV_DETAILS_PATH",  bg="#00817d", fg="white", anchor="e").grid(row=1)
tk.Label(window,
         text="CSV_SUMMARY_PATH",  bg="#00817d", fg="white", anchor="e").grid(row=2)
tk.Label(window,
         text="CSV_VPP_PATH",  bg="#00817d", fg="white", anchor="e").grid(row=3)
tk.Label(window,
         text="XLSX_IO_PATH",  bg="#00817d", fg="white", anchor="e").grid(row=4)
tk.Label(window,
         text="INTERSECTION",  bg="#00817d", fg="white", anchor="e").grid(row=5)
tk.Label(window,
         text="TIMETABLE_INTERVAL",  bg="#00817d", fg="white", anchor="e").grid(row=6)
tk.Label(window,
         text="NO_CYCLE_INTERVALS",  bg="#00817d", fg="white", anchor="e").grid(row=7)
tk.Label(window,
         text="Output folder",  bg="#00817d", fg="white", anchor="e").grid(row=8)

feedback_text = tk.StringVar()
feedback_label = tk.Label(window, textvariable=feedback_text,  bg="#00817d", fg="white", anchor="e").grid(column=0, row=12, columnspan=4)

CSV_MAIN_PATH = tk.Entry(window)
CSV_DETAILS_PATH = tk.Entry(window)
CSV_SUMMARY_PATH = tk.Entry(window)
CSV_VPP_PATH = tk.Entry(window)
XLSX_IO_PATH = tk.Entry(window)
INTERSECTION = tk.Entry(window)
TIMETABLE_INTERVAL = tk.Entry(window)
NO_CYCLE_INTERVALS = tk.Entry(window)
OUTPUT_FOLDER = tk.Entry(window)

CSV_MAIN_PATH.grid(row=0, column=2)
CSV_DETAILS_PATH.grid(row=1, column=2)
CSV_SUMMARY_PATH.grid(row=2, column=2)
CSV_VPP_PATH.grid(row=3, column=2)
XLSX_IO_PATH.grid(row=4, column=2)
INTERSECTION.grid(row=5, column=2)
TIMETABLE_INTERVAL.grid(row=6, column=2)
NO_CYCLE_INTERVALS.grid(row=7, column=2)
OUTPUT_FOLDER.grid(row=8, column=2)

CSV_MAIN_PATH_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_to_file(CSV_MAIN_PATH)).grid(row=0, column=3)
CSV_DETAILS_PATH_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_to_file(CSV_DETAILS_PATH)).grid(row=1, column=3)
CSV_SUMMARY_PATH_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_to_file(CSV_SUMMARY_PATH)).grid(row=2, column=3)
CSV_VPP_PATH_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_to_file(CSV_VPP_PATH)).grid(row=3, column=3)
XLSX_IO_PATH_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_to_file(XLSX_IO_PATH)).grid(row=4, column=3)
OUTPUT_FOLDER_BUTTON = tk.Button(window, text="Select file", command = lambda: set_path_directory(OUTPUT_FOLDER)).grid(row=8, column=3)

validate_bool = tk.IntVar()
VALIDATE_CHECKBOX = tk.Checkbutton(window, text='Validate for anomalies?', variable=validate_bool).grid(row=9, column=2)

tk.Button(window,
          text='Quit',
          command=window.quit).grid(row=10,
                                    column=0,
                                    sticky=tk.W,
                                    pady=4)
tk.Button(window,
          text='Show', command=tmrevpviz_init).grid(row=10,
                                                       column=1,
                                                       sticky=tk.W,
                                                       pady=4)

tk.mainloop()
#-----------------------------------------------------------------









####
