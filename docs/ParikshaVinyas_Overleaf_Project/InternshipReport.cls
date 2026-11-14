% ============================================================
% UPL UNIVERSITY OF SUSTAINABLE TECHNOLOGY
% INTERNSHIP REPORT LaTeX CLASS
%
% Student Template
% ============================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{InternshipReport}[UPL Internship Report Class]

% ============================================================
% BASE CLASS
% ============================================================

\LoadClass[12pt,a4paper,openany]{report}

% ============================================================
% PACKAGES
% ============================================================

\RequirePackage[
    a4paper,
    left=25mm,
    right=20mm,
    top=25mm,
    bottom=25mm
]{geometry}

\RequirePackage{fix-cm}
\RequirePackage{graphicx}
\RequirePackage{array}
\RequirePackage{setspace}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\RequirePackage{eso-pic}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{caption}
\RequirePackage{float}
\RequirePackage{longtable}
\RequirePackage{booktabs}
\RequirePackage{enumitem}
\RequirePackage{lastpage}
\RequirePackage{hyperref}
\RequirePackage{listings}
\RequirePackage{xcolor}

% ============================================================
% LINE SPACING
% ============================================================

\onehalfspacing

% Paragraph formatting: no first-line indentation, matching the reference report style.
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.55em}

% ============================================================
% COLORS
% ============================================================

\definecolor{UPLBlue}{RGB}{28,78,121}
\definecolor{UPLRed}{RGB}{150,30,30}

% ============================================================
% STUDENT / REPORT INFORMATION
% ============================================================

\newcommand{\studentname}[1]{\def\StudentName{#1}}
\newcommand{\enrollmentno}[1]{\def\EnrollmentNo{#1}}

\newcommand{\reporttitle}[1]{\def\ReportTitle{#1}}
\newcommand{\mentorname}[1]{\def\MentorName{#1}}

\newcommand{\degree}[1]{\def\DegreeName{#1}}
\newcommand{\degreeshort}[1]{\def\DegreeShortName{#1}}
\newcommand{\branch}[1]{\def\BranchName{#1}}


\newcommand{\collegename}[1]{\def\CollegeName{#1}}
\newcommand{\universityname}[1]{\def\UniversityName{#1}}

\newcommand{\subjectname}[1]{\def\SubjectName{#1}}
\newcommand{\subjectcode}[1]{\def\SubjectCode{#1}}

\newcommand{\companyname}[1]{\def\CompanyName{#1}}
\newcommand{\companyplace}[1]{\def\CompanyPlace{#1}}

\newcommand{\academicyear}[1]{\def\AcademicYear{#1}}
\newcommand{\reportdate}[1]{\def\ReportDate{#1}}


\newcommand{\semester}[1]{\def\Semester{#1}}

% ============================================================
% CERTIFICATE INFORMATION
% ============================================================

\newcommand{\internshipcoordinator}[1]{\def\InternshipCoordinator{#1}}
\newcommand{\headofdepartment}[1]{\def\HeadOfDepartment{#1}}

% ============================================================
% DEFAULT VALUES
% ============================================================

\studentname{Student Name}
\enrollmentno{Enrollment Number}

\reporttitle{Mention the name of topic}

\mentorname{Name of Mentor}
\semester{III}

\degree{Bachelor of Engineering}
\degreeshort{BE}
\branch{Computer Engineering}


\collegename{Shroff S.R. Rotary Institute of Chemical Technology}

\universityname{UPL University of Sustainable Technology}


\subjectname{Summer Internship}

\companyname{Company Name}
\companyplace{Place}

\academicyear{2026--27}
\reportdate{July 2026}

\internshipcoordinator{Ms. Glace Babu}
\headofdepartment{Ms. Mital Patel}

% ============================================================
% PAGE BORDER
% ============================================================

\newcommand{\UPLPageBorder}{%
    \AddToShipoutPictureBG{%
        \begin{tikzpicture}[remember picture,overlay]

            % Outer border
            \draw[
                line width=0.8pt
            ]
            ([xshift=8mm,yshift=-8mm]current page.north west)
            rectangle
            ([xshift=-8mm,yshift=8mm]current page.south east);

            % Inner border
            \draw[
                line width=0.35pt
            ]
            ([xshift=10mm,yshift=-10mm]current page.north west)
            rectangle
            ([xshift=-10mm,yshift=10mm]current page.south east);

        \end{tikzpicture}%
    }%
}

% Apply border to every page
\UPLPageBorder

% ============================================================
% CHAPTER FORMATTING
% ============================================================

\titleformat{\chapter}
    [display]
    {\bfseries\centering\fontsize{16}{19}\selectfont}
    {Chapter \thechapter}
    {8pt}
    {\MakeUppercase}

\titlespacing*{\chapter}
    {0pt}
    {0pt}
    {20pt}

% ============================================================
% SECTION FORMATTING
% ============================================================

\titleformat{\section}
    {\bfseries\fontsize{14}{17}\selectfont}
    {\thesection}
    {0.6em}
    {}

\titleformat{\subsection}
    {\bfseries\fontsize{13}{16}\selectfont}
    {\thesubsection}
    {0.6em}
    {}

% ============================================================
% FIGURE AND TABLE CAPTIONS
% ============================================================

\captionsetup{
    font=small,
    labelfont=bf,
    justification=centering
}
% ============================================================
% APPENDIX FIGURE NUMBERING
% ============================================================

\AtBeginDocument{%
    \let\oldappendix\appendix
    \renewcommand{\appendix}{%
        \oldappendix
        \renewcommand{\thefigure}{\thechapter.\arabic{figure}}%
        \renewcommand{\thetable}{\thechapter.\arabic{table}}%
    }%
}

% ============================================================
% COMMON CODE LISTING FORMAT
% ============================================================

% Code colors
\definecolor{CodeGreen}{RGB}{0,120,0}
\definecolor{CodeBlue}{RGB}{0,70,150}
\definecolor{CodeGray}{RGB}{90,90,90}
\definecolor{CodeBackground}{RGB}{245,245,245}

% Common code style
\lstdefinestyle{code}{
    backgroundcolor=\color{CodeBackground},
    basicstyle=\ttfamily\small,
    keywordstyle=\color{CodeBlue}\bfseries,
    commentstyle=\color{CodeGreen},
    stringstyle=\color{CodeGray},
    numbers=left,
    numberstyle=\tiny\color{gray},
    numbersep=8pt,
    frame=single,
    framesep=5pt,
    rulecolor=\color{gray},
    breaklines=true,
    breakatwhitespace=false,
    showstringspaces=false,
    tabsize=4,
    keepspaces=true,
    columns=fullflexible,
    captionpos=b
}

% ------------------------------------------------------------
% Student Code Environment
%
% Usage:
% \begin{studentcode}{Python}
% ...
% \end{studentcode}
%
% Supported:
% Python, C, C++, Java, HTML, SQL, JavaScript, PHP, etc.
% ------------------------------------------------------------

\lstnewenvironment{code}[1]
{%
    \lstset{
        style=code,
        language=#1
    }%
}
{}

% ============================================================
% HEADER AND FOOTER
% ============================================================

% ============================================================
% PRE-CHAPTER PAGE STYLE
% ============================================================
% Used for:
%   Cover
%   Certificate
%   Declaration
%   Acknowledgement
%   Table of Contents
%   List of Tables
%   List of Figures
%
% No header and NO page number.
% ============================================================

\fancypagestyle{prechapter}{%
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}


% IMPORTANT:
% The report class uses "plain" for the first page of
% \chapter, \chapter*, \tableofcontents, \listoftables,
% and \listoffigures.
%
% Therefore, BEFORE Chapter 1, plain must also be empty.

\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
}


% Start the document with the empty style
\pagestyle{prechapter}


% ============================================================
% CHAPTER / MAIN REPORT PAGE STYLE
% ============================================================

\fancypagestyle{chapterstyle}{%
    \fancyhf{}

    % --------------------------------------------------------
    % Left: Enrollment Number
    % --------------------------------------------------------

    \fancyhead[L]{%
        \small
        \textbf{\EnrollmentNo}
    }

    % --------------------------------------------------------
    % Right: Internship Type (Code)
    % --------------------------------------------------------

    \fancyhead[R]{%
    \small
    \textbf{\SubjectName\ (\SubjectCode)}
}

    % --------------------------------------------------------
    % Actual Page Number
    % --------------------------------------------------------

    \fancyfoot[R]{%
        \small
        Page \thepage\ of \pageref{LastPage}
    }

    % No horizontal header line
    \renewcommand{\headrulewidth}{0pt}

    % No footer line
    \renewcommand{\footrulewidth}{0pt}
}


% ============================================================
% FIRST PAGE OF EVERY CHAPTER
% ============================================================

\fancypagestyle{chapterplain}{%
    \fancyhf{}

    % Left: Enrollment Number
    \fancyhead[L]{%
        \small
        \textbf{\EnrollmentNo}
    }

    % Right: Internship Type (Code)
    \fancyhead[R]{%
    \small
    \textbf{\SubjectName\ (\SubjectCode)}
}

    % Actual Page Number
    \fancyfoot[R]{%
        \small
        Page \thepage\ of \pageref{LastPage}
    }

    % No horizontal header line
    \renewcommand{\headrulewidth}{0pt}

    % No footer line
    \renewcommand{\footrulewidth}{0pt}
}


% ============================================================
% START HEADER FROM CHAPTER 1
% ============================================================
%
% IMPORTANT:
% - Does NOT reset page numbering.
% - Keeps the actual page number.
% - Changes "plain" to chapterplain from this point onward.
%
% Example:
% If Chapter 1 starts on physical page 7:
%             Page 7
%
% ============================================================

\newcommand{\startchapterheader}{%
    \clearpage
    \pagestyle{chapterstyle}%
    \makeatletter
    \let\ps@plain\ps@chapterplain
    \makeatother
}


% ============================================================
% HEADER POSITION
% ============================================================

\setlength{\headheight}{14pt}
\setlength{\headsep}{8mm}


% ------------------------------------------------------------
% No page number/header before Chapter 1
% ------------------------------------------------------------
% This is important because the standard "report" class uses
% a page-numbered style by default.

\pagestyle{empty}

% ============================================================
% HYPERLINKS
% ============================================================

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=black,
    urlcolor=blue,
    pdfauthor={\StudentName},
    pdftitle={\ReportTitle}
}

% ============================================================
% COVER PAGE
% ============================================================

\newcommand{\maketitlepage}{%

    \begin{titlepage}
        \thispagestyle{empty}
        \begin{center}

            \vspace*{2mm}
            \includegraphics[width=0.68\textwidth]{figures/upl-logo.png}

            \vspace{1mm}
            {\fontsize{15}{18}\selectfont\textbf{An}\par}

            \vspace{2mm}
            {\fontsize{16}{19}\selectfont\textbf{\SubjectName\ Report}\par}

            \vspace{1mm}
            {\fontsize{15}{18}\selectfont\textbf{on}\par}

            \vspace{1mm}
            {\fontsize{16}{19}\selectfont\bfseries\textcolor{UPLRed}{``\ReportTitle''}\par}

            \vspace{4mm}
            {\fontsize{13}{16}\selectfont Submitted as part of the curriculum of\par}

            \vspace{1mm}
            {\fontsize{14}{17}\selectfont \DegreeName\par}

            \vspace{1mm}
            {\fontsize{13}{16}\selectfont in\par}

            \vspace{1mm}
            {\fontsize{14}{17}\selectfont \BranchName\par}

            \vspace{8mm}
            {\fontsize{13}{16}\selectfont Submitted By\par}

            \vspace{3mm}
            \begin{tabular}{>{\centering\arraybackslash}p{0.38\textwidth} >{\centering\arraybackslash}p{0.38\textwidth}}
                \textbf{\StudentName} & \textbf{\EnrollmentNo}
            \end{tabular}

            \vspace{5mm}
            {\fontsize{13}{16}\selectfont Under the guidance of\par}

            \vspace{3mm}
            {\fontsize{14}{17}\selectfont\textbf{\MentorName}\par}

            \vspace{5mm}
            {\fontsize{13}{16}\selectfont Submitted To\par}

            \vspace{3mm}
            {\fontsize{13}{16}\selectfont\textbf{Department of \BranchName}\par}

            \vspace{1mm}
            {\fontsize{13}{16}\selectfont\textbf{\CollegeName}\par}

            \vspace{1mm}
            {\fontsize{13}{16}\selectfont\textbf{\ReportDate}\par}

        \end{center}
    \end{titlepage}
}

% ============================================================
% CERTIFICATE PAGE
% ============================================================

\newcommand{\makecertificate}{%

    \clearpage

    \thispagestyle{empty}

    \begin{center}

        % ----------------------------------------------------
        % COLLEGE NAME
        % ----------------------------------------------------

        {\fontsize{14}{17}\selectfont
        \textbf{\CollegeName}
        \par}

        \vspace{3mm}

        % ----------------------------------------------------
        % DEPARTMENT
        % ----------------------------------------------------

        {\fontsize{14}{17}\selectfont
        \textbf{Department of \BranchName}
        \par}

        \vspace{3mm}

        % ----------------------------------------------------
        % ACADEMIC YEAR
        % ----------------------------------------------------

        {\fontsize{13}{16}\selectfont
        \textbf{Academic Year \AcademicYear}
        \par}

        \vspace{12mm}

        % ----------------------------------------------------
        % CERTIFICATE
        % ----------------------------------------------------

        {\fontsize{16}{19}\selectfont
        \textbf{CERTIFICATE}
        \par}

    \end{center}

    % --------------------------------------------------------
    % CERTIFICATE TEXT
    % --------------------------------------------------------

    \vspace{12mm}

    \noindent
    This is to certify that
    \textbf{\StudentName, (\EnrollmentNo)}
    is a student of Semester \Semester\  of
    \DegreeShortName\ in \BranchName,
    \UniversityName,
    SRICT, Vataria, Ankleshwar, has successfully completed
    \SubjectName\ (\SubjectCode)
    at \textbf{\CompanyName, \CompanyPlace}
    and submitted report during academic year
    \AcademicYear.

    % --------------------------------------------------------
    % DATE
    % --------------------------------------------------------

    \vspace{18mm}

    \noindent
    Date:
    \hspace{5mm}
    \rule{8mm}{0.4pt}
    \hspace{2mm}/\hspace{2mm}
    \rule{8mm}{0.4pt}
    \hspace{2mm}/\hspace{2mm}
    \rule{15mm}{0.4pt}

    % --------------------------------------------------------
    % SIGNATURES
    % --------------------------------------------------------

    \vfill

    \begin{center}

        \begin{tabular*}{\textwidth}{
            @{\extracolsep{\fill}}
            >{\centering\arraybackslash}p{0.30\textwidth}
            >{\centering\arraybackslash}p{0.30\textwidth}
        }
            \rule{40mm}{0.4pt}
            &
            \rule{40mm}{0.4pt}
            \\[2mm]
        
            \textbf{Internship Mentor}
            &
            \textbf{Internship Coordinator}
            \\[2mm]
            \textbf{\MentorName}
            &
            \textbf{\InternshipCoordinator}
        
            
        \end{tabular*}

        \vspace{25mm}

        \rule{40mm}{0.4pt}

        \par

        \vspace{2mm}

        \textbf{Head of the Department}
        \par
        \vspace{2mm}
        \textbf{\HeadOfDepartment}

    \end{center}

}

% ============================================================
% DECLARATION PAGE
% ============================================================

\newcommand{\makedeclaration}{%

    \clearpage

    \thispagestyle{empty}

    % --------------------------------------------------------
    % Declaration Heading
    % --------------------------------------------------------

    \begin{center}

        {\fontsize{16}{19}\selectfont
        \textbf{DECLARATION}
        \par}

    \end{center}

    % --------------------------------------------------------
    % Declaration Text
    % --------------------------------------------------------

    \vspace{15mm}

    \noindent
    I, \textbf{\StudentName\ (\EnrollmentNo)}, am the student of
    Semester \Semester\ of  \DegreeShortName\ in
    \BranchName,
    \UniversityName,
    SRICT, Vataria, hereby declare that this report is prepared
    by me based on my information gathered during the
    \SubjectName\ done in June -- July 2026,
    at \textbf{\CompanyName}.

    % --------------------------------------------------------
    % Student Name / Signature
    % --------------------------------------------------------

     \vspace{30mm}

    \begin{flushright}

        \textbf{\StudentName}

        \vspace{3mm}

        \textbf{(\EnrollmentNo)}

    \end{flushright}

}


% ============================================================
% ACKNOWLEDGEMENT PAGE
% ============================================================

\newcommand{\makeacknowledgement}{%

    \clearpage

    \thispagestyle{empty}

    % --------------------------------------------------------
    % Acknowledgement Heading
    % --------------------------------------------------------

    \begin{center}

        {\fontsize{16}{19}\selectfont
        \textbf{ACKNOWLEDGEMENT}
        \par}

    \end{center}

    % --------------------------------------------------------
    % Acknowledgement Text
    % --------------------------------------------------------

    \vspace{12mm}

    \noindent
    I would like to express our sincere gratitude to all those
    who have supported and guided us throughout our
    \SubjectName.

    \vspace{6mm}

    \noindent
    \textbf{\MentorName}, our Internship Mentor, has helped us
    a lot with his expert advice, helpful feedback, and constant
    support. His/Her hard work, ideas, and support have been very
    helpful in getting us through tough times and finishing
    \SubjectName.

    \vspace{6mm}

    \noindent
    I also want to thank \textbf{\InternshipCoordinator}, the
    Coordinator of Internship, for always being there for us,
    keeping things on track, and making sure that our
    \SubjectName\ activities went well.

    \vspace{6mm}

    \noindent
    I also want to thank \textbf{\HeadOfDepartment}, the Head
    of Department, for constant support and leadership which
    have been very helpful in finishing our
    \SubjectName.

    \vspace{6mm}

    \noindent
    Finally, we want to thank everyone who helped us finish this
    \SubjectName, whether they were faculty, staff, or
    students.

    % --------------------------------------------------------
    % Student Name
    % --------------------------------------------------------
     \vspace{35mm}

    \begin{flushright}

        \textbf{\StudentName}

        \vspace{2mm}

        \textbf{(\EnrollmentNo)}

    \end{flushright}

}

% ============================================================
% BIBLIOGRAPHY / REFERENCES
% ============================================================

\def\thebibliography#1{%
    \clearpage
    \chapter*{\raggedleft REFERENCES}
    \addcontentsline{toc}{chapter}{REFERENCES}
    \list
        {[\arabic{enumi}]}%
        {%
            \settowidth\labelwidth{[#1]}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \usecounter{enumi}%
        }%
    \def\newblock{\hskip .11em plus .33em minus .07em}%
    \sloppy
    \clubpenalty4000
    \widowpenalty4000
    \sfcode`\.=1000\relax
}


% ============================================================
% END OF CLASS
% ============================================================

\endinput
