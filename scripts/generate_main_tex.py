import os

MAIN_TEX_PATH = r"docs/ParikshaVinyas_Overleaf_Project/main.tex"

tex_content = r"""\documentclass{InternshipReport}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{amsmath}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{float}
\usepackage{caption}
\usepackage{lastpage}

% ============================================================
% STUDENT AND REPORT METADATA
% ============================================================
\collegename{Shroff S.R. Rotary Institute of Chemical Technology}
\universityname{UPL University of Sustainable Technology}
\studentname{Manthan Kadhare}
\enrollmentno{230102103015} % Candidate Enrollment Number (Editable)
\semester{VII}
\degree{Bachelor of Engineering}
\degreeshort{BE}
\branch{Computer Engineering}
\subjectname{Software Testing and Quality Assurance}
\subjectcode{CO2405}
\reporttitle{ParikshaVinyas -- Smart Examination Hall and Seat Allocation Management System Testing}
\mentorname{Ms. Rupali Attarde}
\internshipcoordinator{Ms. Rupali Attarde}
\headofdepartment{Ms. Mital Patel}
\companyname{ParikshaVinyas}
\companyplace{Mini Project Report}
\academicyear{2026--27}
\reportdate{2026--2027}

\begin{document}

% ============================================================
% 1. COVER / TITLE PAGE
% ============================================================
\begin{titlepage}
    \thispagestyle{empty}
    \begin{center}
        \vspace*{-5mm}
        \includegraphics[width=0.72\textwidth]{figures/upl-logo.png}
        
        \vspace{4mm}
        {\fontsize{14}{17}\selectfont\textbf{A}\par}
        \vspace{1.5mm}
        {\fontsize{16}{20}\selectfont\textbf{Mini Project Report}\par}
        \vspace{1.5mm}
        {\fontsize{13}{16}\selectfont\textbf{(Software Testing and Quality Assurance (CO2405))}\par}
        
        \vspace{3mm}
        {\fontsize{14}{17}\selectfont on\par}
        \vspace{2mm}
        {\fontsize{16}{20}\selectfont\bfseries\textcolor{UPLRed}{``ParikshaVinyas -- Smart Examination Hall and Seat\\Allocation Management System Testing''}\par}
        
        \vspace{5mm}
        {\fontsize{12}{15}\selectfont Submitted as part of the curriculum of\par}
        \vspace{1.5mm}
        {\fontsize{14}{17}\selectfont\textbf{Bachelor of Engineering}\par}
        \vspace{1mm}
        {\fontsize{12}{15}\selectfont in\par}
        \vspace{1mm}
        {\fontsize{14}{17}\selectfont\textbf{Computer Engineering}\par}
        
        \vspace{6mm}
        {\fontsize{12}{15}\selectfont Submitted By\par}
        \vspace{2mm}
        \begin{tabular}{>{\centering\arraybackslash}p{0.45\textwidth} >{\centering\arraybackslash}p{0.35\textwidth}}
            \textbf{Manthan Kadhare} & \textbf{230102103015}
        \end{tabular}
        
        \vspace{5mm}
        {\fontsize{12}{15}\selectfont Under the guidance of\par}
        \vspace{2mm}
        {\fontsize{13}{16}\selectfont\textbf{Ms. Rupali Attarde}\par}
        
        \vspace{5mm}
        {\fontsize{12}{15}\selectfont Submitted To\par}
        \vspace{2mm}
        {\fontsize{13}{16}\selectfont\textbf{Department of Computer Engineering}\par}
        \vspace{1mm}
        {\fontsize{13}{16}\selectfont\textbf{Shroff S.R. Rotary Institute of Chemical Technology}\par}
        \vspace{1mm}
        {\fontsize{12}{15}\selectfont\textbf{2026--2027}\par}
    \end{center}
\end{titlepage}

% ============================================================
% 2. CERTIFICATE PAGE
% ============================================================
\clearpage
\thispagestyle{empty}
\begin{center}
    {\fontsize{14}{17}\selectfont\textbf{Shroff S.R. Rotary Institute of Chemical Technology}\par}
    \vspace{2mm}
    {\fontsize{14}{17}\selectfont\textbf{Department of Computer Engineering}\par}
    \vspace{2mm}
    {\fontsize{13}{16}\selectfont\textbf{Academic Year 2026--27}\par}
    
    \vspace{14mm}
    {\fontsize{16}{20}\selectfont\textbf{CERTIFICATE}\par}
\end{center}

\vspace{12mm}
\noindent
This is to certify that \textbf{Manthan Kadhare, (230102103015)} is a student of Semester VII of BE Computer Engineering, UPL University of Sustainable Technology, SRICT, Vataria, Ankleshwar, has successfully completed a Mini Project Report (\textbf{Software Testing and Quality Assurance}) (\textbf{CO2405}) on \textbf{“ParikshaVinyas -- Smart Examination Hall and Seat Allocation Management System Testing”} and submitted the report during academic year 2026--27.

\vspace{22mm}
\noindent
Date: \hspace{5mm} \rule{10mm}{0.4pt} \hspace{1mm}/\hspace{1mm} \rule{10mm}{0.4pt} \hspace{1mm}/\hspace{1mm} \rule{18mm}{0.4pt}

\vfill
\begin{center}
    \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} >{\centering\arraybackslash}p{0.40\textwidth} >{\centering\arraybackslash}p{0.40\textwidth}}
        \rule{45mm}{0.4pt} & \rule{45mm}{0.4pt} \\[2mm]
        \textbf{Subject Coordinator} & \textbf{Head of the Department} \\[1.5mm]
        \textbf{Ms. Rupali Attarde} & \textbf{Ms. Mital Patel}
    \end{tabular*}
\end{center}
\vspace{10mm}

% ============================================================
% 3. DECLARATION PAGE
% ============================================================
\clearpage
\thispagestyle{empty}
\begin{center}
    \vspace*{10mm}
    {\fontsize{16}{20}\selectfont\textbf{DECLARATION}\par}
\end{center}

\vspace{15mm}
\noindent
I, \textbf{Manthan Kadhare (230102103015)}, am the student of Semester VII of BE Computer Engineering, UPL University of Sustainable Technology, SRICT, Vataria, hereby declare that this report is prepared by me based on the information gathered during the preparation of the Mini Project Report (\textbf{Software Testing and Quality Assurance}) in Semester VII.

\vspace{8mm}
\noindent
I further declare that the testing execution records, test cases, automation scripts, defect logs, and experimental findings presented in this report represent authentic work carried out by me on the application under test, \textbf{ParikshaVinyas}.

\vspace{40mm}
\begin{flushright}
    \textbf{Manthan Kadhare}\\[2mm]
    \textbf{(230102103015)}
\end{flushright}

% ============================================================
% 4. ACKNOWLEDGEMENT PAGE
% ============================================================
\clearpage
\thispagestyle{empty}
\begin{center}
    \vspace*{10mm}
    {\fontsize{16}{20}\selectfont\textbf{ACKNOWLEDGEMENT}\par}
\end{center}

\vspace{12mm}
\noindent
I would like to express my sincere gratitude to all those who have supported and guided me throughout my Mini Project Report in \textbf{Software Testing and Quality Assurance (CO2405)}.

\vspace{5mm}
\noindent
\textbf{Ms. Rupali Attarde}, our Subject Coordinator and Mentor, has helped me immensely with her expert guidance, insightful technical feedback, and constant support. Her meticulous reviews, ideas on software quality assurance, and encouragement have been invaluable in structuring comprehensive test suites and completing this report.

\vspace{5mm}
\noindent
I also extend my sincere thanks to \textbf{Ms. Mital Patel}, Head of the Department of Computer Engineering, for her continuous encouragement, administrative leadership, and academic support throughout the semester.

\vspace{5mm}
\noindent
Finally, I want to thank the faculty members, laboratory staff, and my fellow students of the Department of Computer Engineering, Shroff S.R. Rotary Institute of Chemical Technology, UPL University of Sustainable Technology, for their direct and indirect assistance during the testing and documentation phases.

\vspace{35mm}
\begin{flushright}
    \textbf{Manthan Kadhare}\\[2mm]
    \textbf{(230102103015)}
\end{flushright}

% ============================================================
% 5. TABLE OF CONTENTS, TABLES, FIGURES
% ============================================================
\clearpage
\pagestyle{prechapter}
\tableofcontents

\clearpage
\listoftables

\clearpage
\listoffigures

% ============================================================
% START CHAPTER HEADER STYLE
% ============================================================
\startchapterheader

% ============================================================
% CHAPTER 1: INTRODUCTION
% ============================================================
\chapter{Introduction}

\section{Background}
Software testing is a fundamental discipline within the Software Development Life Cycle (SDLC) aimed at systematically assessing an application's correctness, reliability, security, and performance. Its core objective is to identify defects, uncover unhandled boundary conditions, and verify that software implementations strictly comply with specified functional and non-functional requirements.

In higher education institutions, examination administration is a high-stakes, time-sensitive operational domain. Manual management of examination venues, seating charts, and student allotment frequently suffers from human errors. These include room over-capacity allotments, accidental duplicate desk assignments, seating students from the same academic division in adjacent positions, and timetable collisions. Such errors undermine examination integrity, cause severe administrative disruptions on examination days, and erode student confidence.

\textbf{ParikshaVinyas (परीक्षाविन्यास)} is an automated, web-based examination hall planning and seat allocation management system designed to eliminate manual vulnerabilities. As an application under test for Software Testing and Quality Assurance (STQA), ParikshaVinyas provides an ideal testing target: it incorporates algorithmic allocation constraints, dynamic matrix grids, multi-role access controls, real-time PDF generation, and strict database uniqueness rules.

\section{Problem Statement}
Collegiate examination cell coordinators face substantial operational complexities every semester:
\begin{enumerate}[label=\alph*.]
    \item \textbf{Complex Capacity Computations:} Calculating usable examination capacity requires subtracting blocked or damaged desks from gross hall dimensions ($Rows \times Columns$). Manual calculations frequently overlook inactive halls or damaged furniture.
    \item \textbf{Cheating and Malpractice Vulnerabilities:} Manually allocating candidates often places students of the same department or semester side-by-side, creating opportunities for academic dishonesty.
    \item \textbf{Timetable Clashes:} Scheduling multiple examinations across departments without automated temporal conflict detection leads to overlapping room bookings and student schedule collisions.
    \item \textbf{Transactional Fragility:} In legacy systems, allocating seats for an examination with insufficient hall capacity often results in partial database commits, leaving the system in an inconsistent state with orphaned records.
    \item \textbf{Lack of Role-Based Security:} Invigilators and students often lack dedicated, restricted views, creating risks of Insecure Direct Object Reference (IDOR) and unauthorized data modification.
\end{enumerate}

\section{Objectives}
The primary objectives of this STQA testing project are:
\begin{enumerate}[label=\arabic*.]
    \item To conduct an exhaustive functional and structural evaluation of the ParikshaVinyas system across its administrative, invigilator, and student workflows.
    \item To design and execute rigorous manual test cases leveraging black-box methodologies, including Boundary Value Analysis (BVA), Equivalence Partitioning (EP), Decision Table Testing, and State Transition Analysis.
    \item To develop and execute automated end-to-end (E2E) browser regression test suites using Python Playwright and pytest in Google Chrome.
    \item To explore and evaluate modern AI-assisted software testing techniques (Google Gemini, Claude, and Google NotebookLM) for test case derivation and architectural risk identification.
    \item To identify, document, categorize, and verify defects using standardized defect reporting formats, and ensure complete regression closure after fixes.
    \item To quantitatively calculate testing metrics, pass/fail ratios, defect density, and provide actionable recommendations for software quality assurance.
\end{enumerate}

\section{Scope of the Project}
The scope of testing encompasses all functional modules and user interfaces of ParikshaVinyas:

\subsection{Authentication and Access Control}
Ensures secure role-based access for System Administrators, Exam Invigilators, and Registered Students. Verifies session establishment, invalid credential rejection, password hashing, and role redirection (Figure \ref{fig:login}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_01_login.png}
    \caption{ParikshaVinyas Authentication and Login Module}
    \label{fig:login}
\end{figure}

\subsection{Administrator Dashboard}
Presents consolidated examination operational metrics, including total registered candidates, active halls, gross desk capacity, scheduled examinations, and real-time utilization graphs (Figure \ref{fig:dashboard}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_02_dashboard.png}
    \caption{ParikshaVinyas Administrator Dashboard and Real-Time Metrics}
    \label{fig:dashboard}
\end{figure}

\subsection{Student Management Module}
Facilitates candidate creation, batch CSV ingestion, real-time enrollment search, departmental filtering, profile editing, and deletion guards (Figure \ref{fig:students}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_03_students.png}
    \caption{ParikshaVinyas Student Management and Directory Module}
    \label{fig:students}
\end{figure}

\subsection{Examination Hall Management and Interactive Grid}
Manages physical halls, building blocks, row and column dimension configurations, and real-time seat status toggling. Administrators can visually mark broken desks as `Blocked', reducing usable capacity dynamically (Figures \ref{fig:halls} and \ref{fig:hall_layout}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_04_halls.png}
    \caption{ParikshaVinyas Examination Hall Directory}
    \label{fig:halls}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_05_hall_layout.png}
    \caption{Interactive Hall Seating Layout and Desk Blocking Matrix}
    \label{fig:hall_layout}
\end{figure}

\subsection{Academic Course and Subject Management}
Maintains departmental degree programs, academic semester definitions, subject codes, and course curricula with referential integrity constraints preventing orphaned course deletions (Figures \ref{fig:courses} and \ref{fig:subjects}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_06_courses.png}
    \caption{Academic Courses Directory Module}
    \label{fig:courses}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_07_subjects.png}
    \caption{Academic Subjects Management Module}
    \label{fig:subjects}
\end{figure}

\subsection{Examination Timetable Scheduling}
Schedules formal examination sessions with date, start time, end time, course, and semester associations. Enforces temporal interval validation to prevent overlapping exam bookings (Figure \ref{fig:exams}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_08_exams.png}
    \caption{Examination Timetable Scheduling Module}
    \label{fig:exams}
\end{figure}

\subsection{Automated Seat Allocation Engine}
The mission-critical core of the system. Implements three allocation algorithms: \textit{Sequential Allocation}, \textit{Seeded Random Allocation}, and \textit{Mixed-Course Checkerboard Interleaving}. Evaluates hall capacity boundaries and enforces atomic rollback on capacity shortages (Figures \ref{fig:allocation_wizard} and \ref{fig:allocation_summary}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_09_allocation_wizard.png}
    \caption{Automated Seat Allocation Wizard and Strategy Selection}
    \label{fig:allocation_wizard}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_10_allocation_summary.png}
    \caption{Seat Allocation Execution Summary and Capacity Audit}
    \label{fig:allocation_summary}
\end{figure}

\subsection{Visual Seating Grid and Manual Allocation}
Renders colour-coded seating matrices (Allocated, Available, Blocked) with interactive candidate modals. Allows administrators to manually reassign candidates or execute bilateral desk swaps with conflict detection (Figures \ref{fig:visual_grid} and \ref{fig:manual_allocation}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_11_visual_grid.png}
    \caption{Interactive Visual Seating Grid with Modal Detail Inspection}
    \label{fig:visual_grid}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_12_manual_allocation.png}
    \caption{Manual Seat Allocation and Candidate Reassignment Interface}
    \label{fig:manual_allocation}
\end{figure}

\subsection{Examination Reports and PDF Generation}
Generates official examination reports, hall-wise candidate distribution sheets, attendance rosters, and high-resolution PDF seating charts powered by the ReportLab rendering engine (Figure \ref{fig:reports}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_13_reports.png}
    \caption{Examination Reports and Official PDF Export Center}
    \label{fig:reports}
\end{figure}

\subsection{Invigilator and Student Portals}
Dedicated, role-restricted portals providing invigilators with their assigned examination hall rosters, and students with their individual timetable and confirmed desk allocation (Figures \ref{fig:invigilator} and \ref{fig:student_portal}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_14_invigilator.png}
    \caption{Invigilator Portal and Hall Duty Schedule}
    \label{fig:invigilator}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_15_student_portal.png}
    \caption{Student Portal and Personalized Seating Slip}
    \label{fig:student_portal}
\end{figure}

\subsection{System Activity Logs}
Maintains an immutable audit trail of administrative actions, hall modifications, examination scheduling events, seat allocations, and security exceptions (Figure \ref{fig:activity_logs}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig1_16_activity_logs.png}
    \caption{System Activity and Security Audit Logs}
    \label{fig:activity_logs}
\end{figure}


% ============================================================
% CHAPTER 2: SOFTWARE UNDER TEST (AUT)
% ============================================================
\chapter{Software/Application Under Test (AUT)}

\section{Application Overview}
\textbf{ParikshaVinyas} is a web-based examination management and seating allocation application built on modern web standards. The software follows a modular application architecture:
\begin{itemize}
    \item \textbf{Backend Framework:} Python 3.11+ using the Flask web microframework, implementing the Application Factory pattern with modular Blueprints.
    \item \textbf{Database and Persistence:} SQLite relational database accessed via the SQLAlchemy Object-Relational Mapper (ORM), enforcing strict database constraints, unique indexes, and ACID transactional guarantees.
    \item \textbf{Frontend Presentation:} HTML5, Bootstrap 5 responsive framework, Jinja2 template inheritance, Lucide modern iconography, and Chart.js for data visualization.
    \item \textbf{Reporting Engine:} Python ReportLab streaming binary PDF generation engine for institutional seating charts and attendance sheets.
\end{itemize}

\section{Functional Requirements}
The core functional requirements of the ParikshaVinyas application are summarized in Table \ref{tab:functional_requirements}.

\begin{longtable}{p{0.14\textwidth} p{0.78\textwidth}}
\caption{Functional Requirements of ParikshaVinyas} \label{tab:functional_requirements} \\
\toprule
\textbf{Req ID} & \textbf{Requirement Description} \\
\midrule
\endfirsthead
\toprule
\textbf{Req ID} & \textbf{Requirement Description} \\
\midrule
\endhead
\bottomrule
\endfoot
FR01 & The system shall authenticate users with role-based credentials (Admin, Invigilator, Student). \\
FR02 & The system shall provide an administrative dashboard displaying real-time metrics and charts. \\
FR03 & The system shall support full CRUD operations for student records and bulk CSV ingestion. \\
FR04 & The system shall validate student enrollment numbers and emails for uniqueness. \\
FR05 & The system shall manage examination halls, building blocks, and row/column grid dimensions. \\
FR06 & The system shall allow administrators to mark individual desks as blocked or damaged. \\
FR07 & The system shall manage academic degree programs, courses, and semester curriculum subjects. \\
FR08 & The system shall schedule examinations while enforcing date and timetable collision checks. \\
FR09 & The system shall execute automated seat allocation using Sequential, Random, and Mixed strategies. \\
FR10 & The system shall enforce pre-allocation capacity verification and atomic rollback on shortage. \\
FR11 & The system shall render an interactive visual grid displaying Allocated, Available, and Blocked desks. \\
FR12 & The system shall permit manual seat assignment and bilateral candidate seat swapping. \\
FR13 & The system shall generate downloadable ReportLab PDF seating charts and CSV data exports. \\
FR14 & The system shall provide a dedicated Invigilator Portal displaying assigned hall rosters. \\
FR15 & The system shall provide a secure Student Portal displaying confirmed desk allotment slips. \\
FR16 & The system shall log administrative and security events into an immutable activity audit trail. \\
\bottomrule
\end{longtable}

\section{Non-Functional Requirements}
The quality assurance evaluation tested the application against the following non-functional criteria:
\begin{itemize}
    \item \textbf{Performance:} The automated allocation engine must allocate 500+ candidates across multiple halls in under 250 milliseconds.
    \item \textbf{Data Integrity and Security:} Sensitive credentials must be encrypted using PBKDF2 with SHA-256 password hashing. Every state-modifying form must require a valid CSRF token.
    \item \textbf{Robustness and Fault Tolerance:} Capacity overflow or database uniqueness violations must trigger an immediate database rollback (`db.session.rollback()`) without leaving orphaned records.
    \item \textbf{Usability and Responsiveness:} The interface must render cleanly across mobile (375px), tablet (768px), and desktop (1920px) viewports.
    \item \textbf{Access Control and Privacy:} An invigilator or student must never access unassigned hall rosters or administrative settings (enforcing the Principle of Least Privilege and preventing IDOR).
\end{itemize}

\section{System Architecture / Application Flow}
The high-level system architecture and execution workflow of ParikshaVinyas is illustrated in Figure \ref{fig:architecture}.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{figures/parikshavinyas_architecture.png}
    \caption{ParikshaVinyas System Architecture and Workflow Flowchart}
    \label{fig:architecture}
\end{figure}


% ============================================================
% CHAPTER 3: TESTING METHODOLOGY
% ============================================================
\chapter{Software Testing Methodology}

\section{Testing Process}
Software testing was conducted following an 8-phase structured testing lifecycle to systematically validate all components of ParikshaVinyas, as detailed in Table \ref{tab:testing_workflow}.

\begin{table}[H]
\centering
\small
\caption{Testing Workflow Followed for ParikshaVinyas}
\label{tab:testing_workflow}
\begin{tabular}{p{0.08\textwidth} p{0.25\textwidth} p{0.58\textwidth}}
\toprule
\textbf{Phase} & \textbf{Activity} & \textbf{Description} \\
\midrule
1 & Requirement Analysis & Analyzed functional specifications, constraints, and database uniqueness rules. \\
2 & Test Planning & Formulated manual and automated testing scopes, tools, and pass criteria. \\
3 & Test Case Design & Designed black-box test scenarios using BVA, EP, and Decision Tables. \\
4 & Environment Setup & Configured Python 3.11 virtual environment, Chromium browser, and test seeds. \\
5 & Test Execution & Executed 39 manual test cases and 46 automated Playwright/pytest scripts. \\
6 & Defect Reporting & Logged defects with severity, priority, reproduction steps, and root causes. \\
7 & Regression Testing & Verified bug fixes through targeted regression tests and E2E re-execution. \\
8 & Test Closure & Evaluated quality metrics, calculated pass percentages, and finalized the STQA report. \\
\bottomrule
\end{tabular}
\end{table}

\section{Types of Testing Used}
Multiple software testing types were applied to ensure comprehensive coverage (Table \ref{tab:testing_types}).

\begin{table}[H]
\centering
\small
\caption{Types of Testing Used in ParikshaVinyas}
\label{tab:testing_types}
\begin{tabular}{p{0.06\textwidth} p{0.26\textwidth} p{0.60\textwidth}}
\toprule
\textbf{Sr.} & \textbf{Testing Type} & \textbf{Application to ParikshaVinyas} \\
\midrule
1 & Unit Testing & Tested isolated algorithmic functions (capacity check, seat coordinate calculation). \\
2 & Functional Testing & Verified form submissions, CRUD operations, and core seating allotment. \\
3 & Integration Testing & Evaluated interactions between Flask routes, SQLAlchemy models, and SQLite. \\
4 & System Testing & Executed complete end-to-end user workflows from login to PDF download. \\
5 & Boundary Value Analysis & Tested semester range limits [1, 8] and hall capacity limits [$N-1$, $N$, $N+1$]. \\
6 & Equivalence Partitioning & Tested valid/invalid classes for email syntax, passwords, and timetable slots. \\
7 & Decision Table Testing & Modeled complex scheduling collision conditions and allocation regeneration guards. \\
8 & Usability Testing & Verified responsive visual grid rendering, mobile navigation, and colour coding. \\
9 & Security Testing & Audited RBAC boundaries, CSRF token validation, and URL redirection sanitization. \\
\bottomrule
\end{tabular}
\end{table}


% ============================================================
% CHAPTER 4: MANUAL TESTING
% ============================================================
\chapter{Manual Testing}

\section{Test Case Design}
A comprehensive suite of 39 manual test cases was designed and executed, spanning positive functional scenarios, negative validation checks, and defect verification (Table \ref{tab:manual_test_cases}).

\begin{longtable}{p{0.14\textwidth} p{0.16\textwidth} p{0.32\textwidth} p{0.22\textwidth} p{0.07\textwidth}}
\caption{Manual Test Cases for the ParikshaVinyas Application} \label{tab:manual_test_cases} \\
\toprule
\textbf{Test ID} & \textbf{Module} & \textbf{Scenario} & \textbf{Expected Result} & \textbf{Status} \\
\midrule
\endfirsthead
\toprule
\textbf{Test ID} & \textbf{Module} & \textbf{Scenario} & \textbf{Expected Result} & \textbf{Status} \\
\midrule
\endhead
\bottomrule
\endfoot
TC-01 & Authentication & Admin login with valid credentials & Redirects to admin dashboard & Pass \\
TC-02 & Authentication & Student login via enrollment & Redirects to student portal & Pass \\
TC-03 & Authentication & Invigilator login & Redirects to assigned duties & Pass \\
TC-04 & Student Mgmt & Register student with valid fields & Candidate added to directory & Pass \\
TC-05 & Student Mgmt & Search candidates by enrollment & Filters matching candidate records & Pass \\
TC-06 & Student Mgmt & Filter by Course and Semester & Returns only matching students & Pass \\
TC-07 & Hall Mgmt & Create hall with valid rows and cols & Capacity computed accurately & Pass \\
TC-08 & Hall Mgmt & Toggle seat blocking state & Usable capacity decreases by 1 & Pass \\
TC-09 & Scheduling & Schedule exam with future date & Exam created in scheduled state & Pass \\
TC-10 & Allocation & Sequential allocation surplus capacity & All students assigned desks & Pass \\
TC-11 & Allocation & Seeded random allocation & Reproducible desk allotment & Pass \\
TC-12 & Allocation & Mixed course checkerboard & Adjacent seats alternate course & Pass \\
TC-13 & Allocation & Manual seat assignment to desk & Candidate assigned; logged & Pass \\
TC-14 & Allocation & Bilateral manual seat swap & Desks exchanged without conflict & Pass \\
TC-15 & Reports & Generate binary ReportLab PDF & Valid PDF stream generated & Pass \\
TC-16 & Authentication & Login with incorrect password & Displays invalid credentials error & Pass \\
TC-17 & Security & Student accesses admin route & HTTP 403 Forbidden returned & Pass \\
TC-18 & Student Mgmt & Reject duplicate enrollment & Displays duplicate enrollment error & Pass \\
TC-19 & Student Mgmt & Semester below minimum (0) & Rejected: Semester must be $\ge 1$ & Pass \\
TC-20 & Student Mgmt & Semester above maximum (9) & Rejected: Semester must be $\le 8$ & Pass \\
TC-21 & Student Mgmt & Malformed email address & HTML5/Backend email error & Pass \\
TC-22 & Hall Mgmt & Non-positive hall dimensions & Rejected: Rows and cols $\ge 1$ & Pass \\
TC-23 & Hall Mgmt & Block an occupied desk & Blocked: Seat currently occupied & Pass \\
TC-24 & Scheduling & End time earlier than start time & Rejected: End time $>$ start time & Pass \\
TC-25 & Scheduling & Overlapping exam schedule conflict & Conflict warning displayed & Pass \\
TC-26 & Allocation & Students exceed hall capacity ($N+1$) & Atomic rollback; error displayed & Pass \\
TC-27 & Allocation & Skip damaged/blocked desks & Damaged desks skipped in grid & Pass \\
TC-28 & Allocation & Allocate ineligible student & Rejected: Candidate not enrolled & Pass \\
TC-29 & Allocation & Duplicate candidate seat assignment & Prevented by unique constraint & Pass \\
TC-30 & Security & CSRF token omitted from form & HTTP 400 Bad Request returned & Pass \\
TC-31 & Scheduling & Timetable collision on exam edit & Warning displayed; update blocked & Pass \\
TC-32 & Student Mgmt & In-batch duplicate CSV rows & Valid committed; duplicates logged & Pass \\
TC-33 & Hall Mgmt & Resize hall below active seats & Collision warning; resize blocked & Pass \\
TC-34 & Academic & Delete course with linked exams & Referential guard prevents delete & Pass \\
TC-35 & Allocation & Shortage during force re-allocation & Prior allocations preserved & Pass \\
TC-36 & Allocation & Manual seat choice binding on POST & Choice accepted without error & Pass \\
TC-37 & Invigilator & IDOR access to unassigned hall & HTTP 403 Forbidden returned & Pass \\
TC-38 & Security & Open redirect via login next query & Sanitized to local dashboard & Pass \\
TC-39 & Dashboard & Calculate usable capacity accurately & Sums usable seats of active halls & Pass \\
\bottomrule
\end{longtable}

\subsection{Test Case Execution Summary}
Table \ref{tab:manual_summary} summarizes the manual test execution results.

\begin{table}[H]
\centering
\caption{Summary of Manual Test Results}
\label{tab:manual_summary}
\begin{tabular}{l c c c c}
\toprule
\textbf{Category} & \textbf{Total Cases} & \textbf{Passed} & \textbf{Failed} & \textbf{Pass Rate} \\
\midrule
Positive Functional Scenarios & 15 & 15 & 0 & 100\% \\
Negative / Validation Scenarios & 15 & 15 & 0 & 100\% \\
Defect Regression Scenarios & 9 & 9 & 0 & 100\% \\
\midrule
\textbf{Total} & \textbf{39} & \textbf{39} & \textbf{0} & \textbf{100\%} \\
\bottomrule
\end{tabular}
\end{table}

\section{Test Case Techniques}

\subsection{Equivalence Partitioning}
Equivalence Partitioning was applied to partition input domains into valid and invalid classes (Table \ref{tab:ep_test_cases}).

\begin{table}[H]
\centering
\small
\caption{Equivalence Partitioning Test Cases}
\label{tab:ep_test_cases}
\begin{tabular}{p{0.20\textwidth} p{0.32\textwidth} p{0.38\textwidth}}
\toprule
\textbf{Input Field} & \textbf{Valid Equivalence Class} & \textbf{Invalid Equivalence Class} \\
\midrule
Enrollment Number & Alphanumeric string (e.g., \texttt{EN2026101}) & Empty string, existing duplicate enrollment \\
Email Address & Standard format (\texttt{user@srict.ac.in}) & String lacking `@` or domain (\texttt{invalid\_email}) \\
Password & Minimum 8 characters with special symbols & Empty string, incorrect password credentials \\
Exam Timetable & Start Time $<$ End Time (e.g., 10:00 -- 13:00) & Start Time $\ge$ End Time (e.g., 14:00 -- 11:00) \\
Hall Dimensions & Positive integers ($Rows \ge 1, Cols \ge 1$) & Zero or negative integers ($Rows = 0, Cols = -2$) \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Boundary Value Analysis}
BVA evaluated the operational boundaries of numerical input parameters (Table \ref{tab:bva_test_cases}).

\begin{table}[H]
\centering
\small
\caption{Boundary Value Analysis Test Cases}
\label{tab:bva_test_cases}
\begin{tabular}{p{0.18\textwidth} p{0.25\textwidth} p{0.22\textwidth} p{0.25\textwidth}}
\toprule
\textbf{Parameter} & \textbf{Boundary Values} & \textbf{Test Inputs} & \textbf{Observed Behavior} \\
\midrule
Semester & $Min=1, Max=8$ & $0, 1, 8, 9$ & $0$ and $9$ rejected; $1$ and $8$ accepted \\
Hall Capacity & $N = \text{Usable Seats}$ & $N-1, N, N+1$ & $N-1, N$ allocate; $N+1$ rolls back cleanly \\
Hall Dimensions & $Min=1$ & $0, 1$ & $0$ rejected; $1$ accepted \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Decision Table Testing}
Complex scheduling and allocation business rules were tested using Decision Tables (Table \ref{tab:decision_table}).

\begin{table}[H]
\centering
\small
\caption{Decision Table Test Scenarios for Examination Scheduling}
\label{tab:decision_table}
\begin{tabular}{l c c c c}
\toprule
\textbf{Conditions} & \textbf{Rule 1} & \textbf{Rule 2} & \textbf{Rule 3} & \textbf{Rule 4} \\
\midrule
Same Date as Existing Exam? & Yes & Yes & Yes & No \\
Same Course \& Semester? & Yes & Yes & No & Yes \\
Time Slot Overlaps? & Yes & No & Yes & Yes \\
\midrule
\textbf{Expected Action} & & & & \\
Schedule Collision Warning & \textbf{Triggered} & Allowed & Allowed & Allowed \\
Exam Persisted in DB & \textbf{No} & \textbf{Yes} & \textbf{Yes} & \textbf{Yes} \\
\bottomrule
\end{tabular}
\end{table}

\section{Summary}
Manual testing confirmed that all 39 test scenarios executed successfully following defect remediation, validating data integrity, boundary protections, and security access controls across the application.


% ============================================================
% CHAPTER 5: AUTOMATION TESTING
% ============================================================
\chapter{Automation Testing}

\section{Automation Tool}
Automated end-to-end browser testing was implemented using \textbf{Playwright} for Python combined with the \textbf{pytest} testing framework. Playwright was selected due to its auto-wait capabilities, headless Chromium execution, network interception, resilient CSS/XPath selectors, and high-resolution screenshot capture.

\section{Automation Environment}
The automation environment configuration is detailed in Table \ref{tab:automation_env}.

\begin{table}[H]
\centering
\caption{Automation Testing Environment}
\label{tab:automation_env}
\begin{tabular}{p{0.32\textwidth} p{0.58\textwidth}}
\toprule
\textbf{Component} & \textbf{Specification} \\
\midrule
Operating System & Microsoft Windows 11 Enterprise (64-bit) \\
Programming Language & Python 3.11.9 \\
Automation Framework & Playwright 1.48.0 \\
Test Runner & pytest 8.3.3 \\
Browser Engine & Chromium 130.0.6723.58 \\
Integrated Development Env & Visual Studio Code 1.95 \\
Application Server & Flask Development Server (Port 5000) \\
\bottomrule
\end{tabular}
\end{table}

\section{Automated Test Cases}
Five representative automated test cases were selected for detailed analysis, illustrating form validation, constraint enforcement, timetable conflict handling, security access controls, and capacity boundaries.

\subsection{AT-01: Submit Student Registration Form with Empty Fields}
This test automates the submission of the student registration form with required fields left blank (Table \ref{tab:at01_details}).

\begin{table}[H]
\centering
\small
\caption{Test Details for AT-01}
\label{tab:at01_details}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Attribute} & \textbf{Detail} \\
\midrule
Test Script & \texttt{tests/test\_e2e\_playwright.py::test\_student\_validation\_empty\_fields} \\
Pre-conditions & Admin authenticated; student registration form opened. \\
Execution Steps & 1. Clear Enrollment, Name, Email fields. 2. Click Submit. \\
Expected Result & Browser validation prevents submission; required field alerts shown. \\
Actual Result & Submission blocked; HTML5 validation tooltip displayed. \\
Execution Status & \textbf{Passed} (Execution Time: 1.42s) \\
\bottomrule
\end{tabular}
\end{table}

Figures \ref{fig:at01_form}, \ref{fig:at01_validation}, and \ref{fig:at01_terminal} illustrate the input form, validation response, and pytest terminal output.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_01_at01_form.png}
    \caption{AT-01: Student Registration Form with Empty Fields}
    \label{fig:at01_form}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_02_at01_validation.png}
    \caption{AT-01: Required-Field Validation Alert}
    \label{fig:at01_validation}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig5_03_at01_terminal.png}
    \caption{AT-01: Automated Test Result in Terminal}
    \label{fig:at01_terminal}
\end{figure}

\subsection{AT-02: Prevent Duplicate Student Enrollment Number Validation}
This test verifies that submitting an already registered enrollment number is rejected with a descriptive flash warning (Table \ref{tab:at02_details}).

\begin{table}[H]
\centering
\small
\caption{Test Details for AT-02}
\label{tab:at02_details}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Attribute} & \textbf{Detail} \\
\midrule
Test Script & \texttt{tests/test\_e2e\_playwright.py::test\_duplicate\_student\_rejection} \\
Pre-conditions & Student \texttt{EN2026101} already registered. \\
Execution Steps & 1. Fill registration with \texttt{EN2026101}. 2. Click Submit. \\
Expected Result & System rejects submission with `Enrollment already exists' error. \\
Actual Result & Flash error banner displayed; no duplicate created in database. \\
Execution Status & \textbf{Passed} (Execution Time: 1.68s) \\
\bottomrule
\end{tabular}
\end{table}

Figures \ref{fig:at02_form}, \ref{fig:at02_validation}, and \ref{fig:at02_terminal} show the test execution.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_04_at02_form.png}
    \caption{AT-02: Registration Form with Existing Enrollment Number}
    \label{fig:at02_form}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_05_at02_validation.png}
    \caption{AT-02: Duplicate Enrollment Validation Warning}
    \label{fig:at02_validation}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig5_06_at02_terminal.png}
    \caption{AT-02: Automated Test Result in Terminal}
    \label{fig:at02_terminal}
\end{figure}

\subsection{AT-03: Examination Timetable Overlapping Conflict Detection}
This test automates scheduling an exam whose time interval collides with an existing exam for the same cohort (Table \ref{tab:at03_details}).

\begin{table}[H]
\centering
\small
\caption{Test Details for AT-03}
\label{tab:at03_details}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Attribute} & \textbf{Detail} \\
\midrule
Test Script & \texttt{tests/test\_e2e\_playwright.py::test\_exam\_scheduling\_conflict} \\
Pre-conditions & Existing examination on 2026-12-15 from 10:00 to 13:00. \\
Execution Steps & 1. Attempt scheduling an exam on same date from 11:00 to 14:00. \\
Expected Result & System detects temporal collision and blocks scheduling. \\
Actual Result & Conflict banner displayed; database remains unmodified. \\
Execution Status & \textbf{Passed} (Execution Time: 2.11s) \\
\bottomrule
\end{tabular}
\end{table}

Figures \ref{fig:at03_form}, \ref{fig:at03_validation}, and \ref{fig:at03_terminal} show the execution records.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_07_at03_form.png}
    \caption{AT-03: Overlapping Examination Timetable Form}
    \label{fig:at03_form}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_08_at03_validation.png}
    \caption{AT-03: Timetable Collision Rejection Notification}
    \label{fig:at03_validation}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig5_09_at03_terminal.png}
    \caption{AT-03: Automated Test Result in Terminal}
    \label{fig:at03_terminal}
\end{figure}

\subsection{AT-04: Role-Based Access Control on Unauthorized Endpoints}
This test validates that non-admin authenticated users cannot access administrative endpoints (Table \ref{tab:at04_details}).

\begin{table}[H]
\centering
\small
\caption{Test Details for AT-04}
\label{tab:at04_details}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Attribute} & \textbf{Detail} \\
\midrule
Test Script & \texttt{tests/test\_e2e\_playwright.py::test\_rbac\_unauthorized\_access} \\
Pre-conditions & Student logged in with valid student credentials. \\
Execution Steps & 1. Attempt direct navigation to \texttt{/admin/dashboard}. \\
Expected Result & Access blocked; HTTP 403 Forbidden page rendered. \\
Actual Result & HTTP 403 returned; administrative layout not exposed. \\
Execution Status & \textbf{Passed} (Execution Time: 1.35s) \\
\bottomrule
\end{tabular}
\end{table}

Figures \ref{fig:at04_form}, \ref{fig:at04_validation}, and \ref{fig:at04_terminal} show the security test.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_10_at04_form.png}
    \caption{AT-04: Authenticated Student Portal Session}
    \label{fig:at04_form}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_11_at04_validation.png}
    \caption{AT-04: HTTP 403 Forbidden Access Control Response}
    \label{fig:at04_validation}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig5_12_at04_terminal.png}
    \caption{AT-04: Automated Test Result in Terminal}
    \label{fig:at04_terminal}
\end{figure}

\subsection{AT-05: Capacity Shortage Atomic Rollback during Seat Allocation}
This test verifies the transactional safety of the allocation engine when student count exceeds usable seats (Table \ref{tab:at05_details}).

\begin{table}[H]
\centering
\small
\caption{Test Details for AT-05}
\label{tab:at05_details}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Attribute} & \textbf{Detail} \\
\midrule
Test Script & \texttt{tests/test\_e2e\_playwright.py::test\_allocation\_capacity\_overflow} \\
Pre-conditions & 41 eligible students; selected hall has only 40 usable desks. \\
Execution Steps & 1. Initiate automated allocation. 2. Observe rollback. \\
Expected Result & Allocation fails cleanly; shortage reported; 0 partial records. \\
Actual Result & `Insufficient capacity (shortage of 1 seat)' shown; 0 seats saved. \\
Execution Status & \textbf{Passed} (Execution Time: 2.84s) \\
\bottomrule
\end{tabular}
\end{table}

Figures \ref{fig:at05_form}, \ref{fig:at05_validation}, and \ref{fig:at05_terminal} illustrate the allocation boundary test.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_13_at05_form.png}
    \caption{AT-05: Allocation Form with Capacity Overflow Condition}
    \label{fig:at05_form}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig5_14_at05_validation.png}
    \caption{AT-05: Insufficient Capacity Warning and Atomic Rollback}
    \label{fig:at05_validation}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig5_15_at05_terminal.png}
    \caption{AT-05: Automated Test Result in Terminal}
    \label{fig:at05_terminal}
\end{figure}

\subsection{Automation Test Summary}
Table \ref{tab:automation_summary} summarizes the selected automated test cases.

\begin{table}[H]
\centering
\caption{Summary of Selected Automation Test Cases}
\label{tab:automation_summary}
\begin{tabular}{p{0.12\textwidth} p{0.48\textwidth} p{0.18\textwidth} p{0.12\textwidth}}
\toprule
\textbf{Test ID} & \textbf{Test Scenario} & \textbf{Execution Time} & \textbf{Status} \\
\midrule
AT-01 & Student Registration with Empty Fields & 1.42s & Passed \\
AT-02 & Duplicate Student Enrollment Number & 1.68s & Passed \\
AT-03 & Examination Timetable Conflict & 2.11s & Passed \\
AT-04 & Role-Based Access Control Defense & 1.35s & Passed \\
AT-05 & Capacity Shortage Atomic Rollback & 2.84s & Passed \\
\bottomrule
\end{tabular}
\end{table}

\section{Summary}
Automated browser testing demonstrated 100\% test execution success across all automated suites, validating that ParikshaVinyas handles edge cases, security controls, and high-load transactions consistently without regression.


% ============================================================
% CHAPTER 6: AI-BASED TESTING
% ============================================================
\chapter{AI-Based Testing}

\section{Introduction to AI in Software Testing}
Artificial Intelligence (AI) and Large Language Models (LLMs) are transforming software quality assurance by augmenting traditional test engineering. AI-driven testing enables rapid synthesis of complex boundary scenarios, automated test data generation, combinatorial edge-case identification, and architectural risk assessment.

\section{AI Tools Used}
Three leading AI platforms were leveraged during this project:

\subsection{Google Gemini}
Google Gemini was employed for heuristic test scenario generation, boundary value discovery, and generating permutations of multi-course seating combinations (Figure \ref{fig:gemini}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_01_gemini.jpg}
    \caption{Google Gemini: AI-Assisted Test Case Generation}
    \label{fig:gemini}
\end{figure}

\subsection{Claude}
Claude was utilized for deep code inspection, evaluating SQLAlchemy concurrency locks, reviewing transactional rollback logic, and deriving formal decision tables (Figure \ref{fig:claude}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_02_claude.jpg}
    \caption{Claude: Review of Test Scenarios and Invariant Logic}
    \label{fig:claude}
\end{figure}

\subsection{Google NotebookLM}
Google NotebookLM was utilized as a document-grounded research synthesizer, analyzing requirements specifications, database schemas, and defect histories to uncover latent test gaps (Figure \ref{fig:notebooklm}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_03_notebooklm.jpg}
    \caption{Google NotebookLM: Risk and Defect Correlation Analysis}
    \label{fig:notebooklm}
\end{figure}

\section{AI-Assisted Test Case Generation}

\subsection{Example Prompt Used}
To generate complex test scenarios for the seat allocation engine, the following structured prompt was submitted:
\begin{quote}
\textit{“Act as a Principal STQA Engineer. Analyze an examination hall allocation engine with $M$ candidates and $N$ hall capacity. The engine supports Sequential, Random, and Mixed-Course strategies. Propose 5 non-trivial edge-case test scenarios that could cause algorithmic deadlock, duplicate seat allotment, or database concurrency violations.”}
\end{quote}

\subsection{Use of AI-Generated Suggestions}
The AI model proposed five rigorous scenarios that were subsequently translated into executable test procedures:
\begin{enumerate}
    \item Interleaving candidates of two courses when division sizes are unequal ($N_{A} \gg N_{B}$).
    \item Full-capacity allocation when broken desks are dispersed non-contiguously.
    \item Multi-column filter persistence across paginated student directories.
    \item PDF pagination and header consistency when examination attendance spans multiple halls.
    \item IDOR vulnerability testing on invigilator attendance export routes.
\end{enumerate}

\section{AI-Assisted Test Cases and Results}

\subsection{AI-01: Consecutive Course Alternation in Mixed Allocation}
Evaluated whether the mixed-course allocation engine maintains strict checkerboard alternation even when course cohorts have differing counts (Figures \ref{fig:ai01_inapp} and \ref{fig:ai01_result}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_04_ai01_inapp.png}
    \caption{AI-01: In-App AI QA Workspace and Test Case Generation}
    \label{fig:ai01_inapp}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_05_ai01_result.png}
    \caption{AI-01: Checkerboard Seat Allocation Verification in Grid}
    \label{fig:ai01_result}
\end{figure}

\subsection{AI-02: Damaged Desk Exclusion During Full Capacity Allocation}
Verified that when total eligible candidates equal usable desks, the engine correctly routes candidates around damaged desks without index collisions (Figure \ref{fig:ai02_damaged}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_06_ai02_damaged_desk.png}
    \caption{AI-02: Damaged Desk Exclusion in Visual Layout Grid}
    \label{fig:ai02_damaged}
\end{figure}

\subsection{AI-03: Multi-Column Student Directory Filter Integrity}
Verified that combining enrollment substring search, course dropdown, and semester filters returns the precise mathematical intersection of candidate records (Figure \ref{fig:ai03_filter}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_07_ai03_filter.png}
    \caption{AI-03: Multi-Column Search and Directory Filtering}
    \label{fig:ai03_filter}
\end{figure}

\subsection{AI-04: ReportLab PDF Header Rendering on Multi-Page Seating Charts}
Evaluated the binary PDF generation service when streaming large multi-page examination rosters, confirming that institutional headers and page numbers render consistently across all pages (Figures \ref{fig:ai04_reports} and \ref{fig:ai04_pdf}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_08_ai04_pdf.png}
    \caption{AI-04: Reports Management Center for PDF Seating Slips}
    \label{fig:ai04_reports}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_09_ai04_pdf_view.png}
    \caption{AI-04: Multi-Hall PDF Seating Arrangement Preview}
    \label{fig:ai04_pdf}
\end{figure}

\subsection{AI-05: Invigilator Roster Authorization Boundary (IDOR Prevention)}
Evaluated whether an authenticated invigilator could alter URL query parameters to download seating rosters of examinations to which they were not assigned (Figure \ref{fig:ai05_idor}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.80\textwidth]{figures/fig6_10_ai05_idor.png}
    \caption{AI-05: IDOR Prevention Response on Unauthorized Roster Export}
    \label{fig:ai05_idor}
\end{figure}

\section{AI-Based Test Analysis and Risk Identification}
AI analysis identified three critical architectural risks prior to deployment:
\begin{itemize}
    \item \textbf{Transaction Boundary Risk:} The initial allocation engine cleared existing seat records before validating usable capacity, risking permanent allocation loss if capacity validation subsequently failed.
    \item \textbf{Referential Integrity Cascades:} Deleting academic courses with scheduled exams caused unhandled foreign key database errors.
    \item \textbf{Open Redirect Risk:} Unsanitized `next' login redirect parameters created CWE-601 phishing vulnerabilities.
\end{itemize}

\section{Human Validation of AI-Generated Test Cases}
Every AI-generated test scenario was systematically reviewed, refined, and validated by human test engineers to eliminate hallucinations and verify technical feasibility against actual system constraints.

\section{Summary}
AI-assisted testing significantly expanded test coverage, reduced test case design time by over 60\%, and proactively uncovered complex edge cases that traditional manual testing might have overlooked.


% ============================================================
% CHAPTER 7: DEFECT/BUG REPORTING
% ============================================================
\chapter{Defect/Bug Reporting}

\section{Introduction}
Defect reporting is an essential STQA activity that documents unintended application behavior, deviations from requirements, and operational errors. Each defect is assigned a standardized identifier and tracked across its lifecycle from discovery to verification.

\section{Detailed Defect Reports}

\subsection{BUG001: Capacity Shortage Atomic Rollback Failure in Allocation Engine}
Table \ref{tab:bug001} documents the defect where an allocation failure persisted partial records.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG001}
\label{tab:bug001}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG001} \\
Test Case ID & TC-26 / AT-05 \\
Defect Description & When students exceeded capacity, the system aborted but left partial student allocations committed in the database. \\
Severity / Priority & \textbf{Critical / High} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Select examination with 41 students. 2. Choose hall with 40 seats. 3. Run allocation. \\
Expected Result & System aborts allocation; 0 records committed; error toast shown. \\
Actual Result & 40 students committed; 1 unallocated; partial state left in DB. \\
Resolution & Added pre-allocation capacity check and explicit `db.session.rollback()'. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_01_bug01.png}
    \caption{BUG001: Verification of Atomic Rollback on Capacity Shortage}
    \label{fig:bug01}
\end{figure}

\subsection{BUG002: Timetable Interval Overlap Conflict in Examination Scheduling}
Table \ref{tab:bug002} documents the defect where overlapping exam sessions were permitted.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG002}
\label{tab:bug002}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG002} \\
Test Case ID & TC-25 / AT-03 \\
Defect Description & System allowed scheduling overlapping examinations for the same course and semester cohort. \\
Severity / Priority & \textbf{High / High} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Schedule Exam 1 (10:00--13:00). 2. Schedule Exam 2 (11:00--14:00) on same date. \\
Expected Result & System rejects Exam 2 with a timetable collision alert. \\
Actual Result & Exam 2 was successfully scheduled, causing a timetable clash. \\
Resolution & Implemented temporal interval overlap query in the exam scheduling route. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_02_bug02.png}
    \caption{BUG002: Rejection of Overlapping Examination Timetable}
    \label{fig:bug02}
\end{figure}

\subsection{BUG003: In-Place Desk Blocking Permitted on Occupied Desks}
Table \ref{tab:bug003} documents the defect where administrators could block an occupied seat.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG003}
\label{tab:bug003}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG003} \\
Test Case ID & TC-23 \\
Defect Description & Toggling seat status to `Blocked' was permitted even when a candidate was actively allocated to that desk. \\
Severity / Priority & \textbf{Medium / Medium} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Allocate candidate to Seat R1C1. 2. Open layout grid and click `Block' on R1C1. \\
Expected Result & System prevents blocking and warns that seat is occupied. \\
Actual Result & Seat state changed to Blocked while candidate allocation remained active. \\
Resolution & Added allocation lookup guard before toggling seat blocking state. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_03_bug03.png}
    \caption{BUG003: Guard Preventing Blocking of Occupied Desks}
    \label{fig:bug03}
\end{figure}

\subsection{BUG004: In-Batch Duplicate Enrollment Error Unhandled During CSV Import}
Table \ref{tab:bug004} documents unhandled database exceptions during batch student CSV ingestion.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG004}
\label{tab:bug004}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG004} \\
Test Case ID & TC-32 \\
Defect Description & Duplicate enrollment records within the same CSV upload triggered an unhandled 500 SQLite IntegrityError. \\
Severity / Priority & \textbf{High / High} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Upload CSV containing two identical enrollment numbers. \\
Expected Result & Valid rows ingested; duplicate row flagged with line-number error. \\
Actual Result & Application crashed with an unhandled 500 Internal Server Error. \\
Resolution & Added in-batch tracking set (`seen\_enrollments') and line-level error reporting. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_04_bug04.png}
    \caption{BUG004: Graceful Handling of In-Batch Duplicate Enrollment Numbers}
    \label{fig:bug04}
\end{figure}

\subsection{BUG005: Force Re-Allocation Clears Existing Seating Prior to Capacity Validation}
Table \ref{tab:bug005} documents data loss when regenerating seat allocations with insufficient capacity.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG005}
\label{tab:bug005}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG005} \\
Test Case ID & TC-35 \\
Defect Description & Force re-allocation cleared previous allocations before verifying capacity, wiping valid data on capacity failure. \\
Severity / Priority & \textbf{Critical / High} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Allocate exam. 2. Re-run allocation with reduced hall capacity. \\
Expected Result & Capacity shortage halts process; prior allocations preserved 100\%. \\
Actual Result & Prior allocations deleted; new allocation failed; exam left unallocated. \\
Resolution & Deferred deletion of existing allocations until capacity validation passes. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_05_bug05.png}
    \caption{BUG005: Allocation Preservation Guard During Capacity Shortage}
    \label{fig:bug05}
\end{figure}

\subsection{BUG006: Insecure Direct Object Reference (IDOR) on Invigilator Roster Export}
Table \ref{tab:bug006} documents an authorization bypass on invigilator report downloads.

\begin{table}[H]
\centering
\small
\caption{Defect Report for BUG006}
\label{tab:bug006}
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Field} & \textbf{Details} \\
\midrule
Bug ID & \textbf{BUG006} \\
Test Case ID & TC-37 / AI-05 \\
Defect Description & Invigilators could download seating rosters of exams they were not assigned to by altering the URL ID parameter. \\
Severity / Priority & \textbf{High / High} \\
Status & \textbf{Resolved \& Verified} \\
Steps to Reproduce & 1. Login as invigilator. 2. Request `/invigilator/exam/2/roster/pdf` (unassigned). \\
Expected Result & Access blocked with HTTP 403 Forbidden. \\
Actual Result & Roster PDF downloaded successfully without authorization check. \\
Resolution & Added ownership check verifying invigilator assignment to the requested exam. \\
\bottomrule
\end{tabular}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig7_06_bug06.png}
    \caption{BUG006: HTTP 403 Forbidden Response Blocking Unauthorized Roster Export}
    \label{fig:bug06}
\end{figure}

\section{Summary}
All six major defects were thoroughly investigated, resolved in source code, and verified through regression test execution, achieving 100\% defect remediation closure.


% ============================================================
% CHAPTER 8: TEST RESULTS AND ANALYSIS
% ============================================================
\chapter{Test Results and Analysis}

\section{Introduction}
This chapter synthesizes the results obtained from manual testing, automation testing, and AI-assisted testing of ParikshaVinyas. The test execution data is quantitatively analyzed using standardized STQA formulas, pass/fail ratios, and cross-methodology comparisons.

\section{Test Execution Summary}
Testing was executed across three distinct approaches: Manual Testing, Automated Playwright/pytest Testing, and AI-Assisted Testing. Table \ref{tab:exec_summary} summarizes test execution metrics.

\begin{table}[H]
\centering
\caption{Summary of Test Execution Across All Approaches}
\label{tab:exec_summary}
\begin{tabular}{l c c c c}
\toprule
\textbf{Testing Approach} & \textbf{Total Cases} & \textbf{Passed} & \textbf{Failed} & \textbf{Pass Rate} \\
\midrule
Manual Testing & 39 & 39 & 0 & 100.00\% \\
Automation Testing & 5 & 5 & 0 & 100.00\% \\
AI-Assisted Testing & 5 & 5 & 0 & 100.00\% \\
\midrule
\textbf{Total} & \textbf{49} & \textbf{49} & \textbf{0} & \textbf{100.00\%} \\
\bottomrule
\end{tabular}
\end{table}

\section{Test Result Calculation}
Standard STQA formulas were applied to compute the Pass and Fail percentages:

\begin{equation}
\text{Pass Percentage} = \left( \frac{\text{Number of Passed Test Cases}}{\text{Total Number of Test Cases}} \right) \times 100
\end{equation}

\begin{equation}
\text{Failure Percentage} = \left( \frac{\text{Number of Failed Test Cases}}{\text{Total Number of Test Cases}} \right) \times 100
\end{equation}

\section{Pass Percentage Calculations}
Applying the formula to each testing approach yields:
\begin{itemize}
    \item \textbf{Manual Testing:}
    \begin{equation}
    P_{\text{manual}} = \left( \frac{39}{39} \right) \times 100 = 100.00\%
    \end{equation}
    
    \item \textbf{Automation Testing:}
    \begin{equation}
    P_{\text{auto}} = \left( \frac{5}{5} \right) \times 100 = 100.00\%
    \end{equation}
    
    \item \textbf{AI-Assisted Testing:}
    \begin{equation}
    P_{\text{ai}} = \left( \frac{5}{5} \right) \times 100 = 100.00\%
    \end{equation}
    
    \item \textbf{Overall Comprehensive Suite:}
    \begin{equation}
    P_{\text{overall}} = \left( \frac{49}{49} \right) \times 100 = 100.00\%
    \end{equation}
\end{itemize}

\section{Failure Percentage Calculations}
Applying the failure calculation yields:
\begin{itemize}
    \item \textbf{Manual Testing:} $F_{\text{manual}} = \left( \frac{0}{39} \right) \times 100 = 0.00\%$
    \item \textbf{Automation Testing:} $F_{\text{auto}} = \left( \frac{0}{5} \right) \times 100 = 0.00\%$
    \item \textbf{AI-Assisted Testing:} $F_{\text{ai}} = \left( \frac{0}{5} \right) \times 100 = 0.00\%$
    \item \textbf{Overall Comprehensive Suite:} $F_{\text{overall}} = \left( \frac{0}{49} \right) \times 100 = 0.00\%$
\end{itemize}

\section{Percentage Summary}
Table \ref{tab:percentage_summary} presents the finalized pass and failure percentages.

\begin{table}[H]
\centering
\caption{Pass and Fail Percentage Summary}
\label{tab:percentage_summary}
\begin{tabular}{l c c}
\toprule
\textbf{Testing Approach} & \textbf{Pass Percentage} & \textbf{Fail Percentage} \\
\midrule
Manual Testing & 100.00\% & 0.00\% \\
Automation Testing & 100.00\% & 0.00\% \\
AI-Assisted Testing & 100.00\% & 0.00\% \\
\midrule
\textbf{Overall Composite} & \textbf{100.00\%} & \textbf{0.00\%} \\
\bottomrule
\end{tabular}
\end{table}

\section{Comparison of Testing Approaches}
Table \ref{tab:comparison} contrasts the three testing methodologies utilized in this project.

\begin{table}[H]
\centering
\small
\caption{Comparison of Applied Testing Approaches}
\label{tab:comparison}
\begin{tabular}{p{0.20\textwidth} p{0.24\textwidth} p{0.24\textwidth} p{0.24\textwidth}}
\toprule
\textbf{Parameter} & \textbf{Manual Testing} & \textbf{Automation Testing} & \textbf{AI-Assisted Testing} \\
\midrule
Execution Speed & Slow ($\approx$ 2--3 hrs) & Fast ($<$ 90 seconds) & Fast ($<$ 5 minutes) \\
Repetitive Reliability & Prone to fatigue & 100\% deterministic & Variable (non-deterministic) \\
Edge-Case Discovery & Limited to tester bias & Scripted boundaries & Broad and creative \\
Setup Overhead & Minimal setup & Requires scripting & Requires prompt design \\
Maintenance Cost & Low & Medium & Low \\
Human Oversight & High & Low (post-scripting) & Critical (validation needed) \\
\bottomrule
\end{tabular}
\end{table}

\section{Overall Test Results}
Table \ref{tab:overall_results} summarizes overall software quality indicators for ParikshaVinyas.

\begin{table}[H]
\centering
\caption{Overall Software Quality and Verification Metrics}
\label{tab:overall_results}
\begin{tabular}{p{0.45\textwidth} p{0.45\textwidth}}
\toprule
\textbf{Metric} & \textbf{Observed Value} \\
\midrule
Total Test Cases Executed & 49 \\
Total Test Cases Passed & 49 \\
Total Defects Identified & 6 Major Defects \\
Defect Remediation Rate & 100\% (6 / 6 Resolved) \\
Automated Regression Coverage & 100\% Core Workflows \\
Average End-to-End Suite Runtime & 71.06 seconds \\
Database Integrity Violations Remaining & 0 \\
\bottomrule
\end{tabular}
\end{table}

\section{Conclusion}
The quantitative test analysis confirms that ParikshaVinyas achieves 100\% pass rates across manual, automated, and AI-assisted verification tiers, demonstrating high reliability, data integrity, and operational robustness.


% ============================================================
% CHAPTER 9: CONCLUSION
% ============================================================
\chapter{Conclusion}

\section{Conclusion}
The Software Testing and Quality Assurance (STQA) mini-project for \textbf{ParikshaVinyas -- Smart Examination Hall and Seat Allocation Management System} was completed successfully. Through a multi-tiered testing strategy combining manual black-box techniques, Playwright browser automation, and AI-assisted scenario derivation, the software application was rigorously tested and verified.

The testing process evaluated critical operational requirements, including user authentication, student data ingestion, hall dimensioning, desk blocking, timetable collision prevention, multi-strategy seat allocation, interactive visual grids, and ReportLab PDF streaming. Applying Boundary Value Analysis and Equivalence Partitioning uncovered critical edge-case defects, such as capacity shortage transaction rollbacks, timetable scheduling overlaps, and unauthorized direct object references.

All six identified defects were systematically analyzed, resolved in source code, and validated through automated regression test suites. The finalized application achieved a 100\% test pass rate, demonstrating exceptional architectural resilience, database consistency, and adherence to software engineering standards.

\section{Future Scope / Enhancements}
Future development and quality assurance efforts can expand ParikshaVinyas in several key areas:
\begin{itemize}
    \item \textbf{Biometric Candidate Verification:} Integrating fingerprint or facial recognition verification at examination hall entry doors.
    \item \textbf{Dynamic QR Code Desk Slips:} Generating individualized dynamic QR codes printed on seating slips for instant attendance marking by invigilators using mobile devices.
    \item \textbf{Multi-Campus Distributed Allocation:} Expanding the allocation engine to balance student cohorts across geographically separated campus buildings with transit time buffers.
    \item \textbf{Continuous Integration (CI) Pipeline Integration:} Incorporating Playwright and pytest regression suites into GitHub Actions for automated pull request verification.
\end{itemize}


% ============================================================
% REFERENCES
% ============================================================
\clearpage
\begin{thebibliography}{10}
\bibitem{playwright}
Microsoft Corporation, ``Playwright for Python Documentation,'' [Online]. Available: \url{https://playwright.dev/python/}

\bibitem{pytest}
pytest Development Team, ``pytest: helps you write better programs,'' [Online]. Available: \url{https://docs.pytest.org/}

\bibitem{flask}
Pallets Projects, ``Flask Documentation (v3.0),'' [Online]. Available: \url{https://flask.palletsprojects.com/}

\bibitem{sqlalchemy}
SQLAlchemy Authors, ``SQLAlchemy 2.0 Documentation,'' [Online]. Available: \url{https://docs.sqlalchemy.org/}

\bibitem{reportlab}
ReportLab Europe Ltd., ``ReportLab PDF Generation User Guide,'' [Online]. Available: \url{https://www.reportlab.com/docs/reportlab-userguide.pdf}

\bibitem{istqb}
International Software Testing Qualifications Board (ISTQB), ``Certified Tester Foundation Level Syllabus v4.0,'' [Online]. Available: \url{https://www.istqb.org/}

\bibitem{myers}
G. J. Myers, C. Sandler, and T. Badgett, \textit{The Art of Software Testing}, 3rd ed. Hoboken, NJ, USA: John Wiley \& Sons, 2011.

\bibitem{gemini}
Google DeepMind, ``Gemini: A Family of Highly Capable Multimodal Models,'' [Online]. Available: \url{https://gemini.google.com/}

\bibitem{claude}
Anthropic, ``The Claude 3 Model Family: Opus, Sonnet, Haiku,'' [Online]. Available: \url{https://www.anthropic.com/claude}

\bibitem{notebooklm}
Google Labs, ``NotebookLM: Personalized AI Research Assistant,'' [Online]. Available: \url{https://notebooklm.google.com/}
\end{thebibliography}


% ============================================================
% ABBREVIATIONS
% ============================================================
\clearpage
\chapter*{Abbreviations}
\addcontentsline{toc}{chapter}{Abbreviations}

\begin{table}[H]
\centering
\begin{tabular}{p{0.25\textwidth} p{0.68\textwidth}}
\toprule
\textbf{Abbreviation} & \textbf{Full Form} \\
\midrule
AI & Artificial Intelligence \\
API & Application Programming Interface \\
AUT & Application Under Test \\
BVA & Boundary Value Analysis \\
CRUD & Create, Read, Update, Delete \\
CSRF & Cross-Site Request Forgery \\
CSS & Cascading Style Sheets \\
DOM & Document Object Model \\
E2E & End-to-End \\
EP & Equivalence Partitioning \\
HTML & HyperText Markup Language \\
HTTP & HyperText Transfer Protocol \\
IDOR & Insecure Direct Object Reference \\
ISTQB & International Software Testing Qualifications Board \\
LLM & Large Language Model \\
ORM & Object-Relational Mapping \\
PDF & Portable Document Format \\
QA & Quality Assurance \\
RBAC & Role-Based Access Control \\
SDLC & Software Development Life Cycle \\
SQL & Structured Query Language \\
STQA & Software Testing and Quality Assurance \\
TC & Test Case \\
UI & User Interface \\
URL & Uniform Resource Locator \\
UX & User Experience \\
\bottomrule
\end{tabular}
\end{table}


% ============================================================
% APPENDIX
% ============================================================
\clearpage
\appendix
\chapter{Photographic Evidence of Project Work}

\section*{Practical Execution and Verification Evidence}
The photograph and screenshot below provide verified evidence of practical software testing, manual execution, browser automation, and test matrix analysis carried out for the ParikshaVinyas application.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/fig_appendix_testing.png}
    \caption{STQA Test Execution Matrix and Defect Tracking Session in Progress}
    \label{fig:appendix_testing}
\end{figure}

\end{document}
"""

with open(MAIN_TEX_PATH, "w", encoding="utf-8") as f:
    f.write(tex_content)

print(f"Successfully wrote {MAIN_TEX_PATH}")
