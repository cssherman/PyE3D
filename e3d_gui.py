#!/usr/bin/python
from e3d_classes import *
from Tkinter import *
import e3d_main
import ttk
import tkFont
from tkFileDialog import askopenfilename, asksaveasfilename


class GUIFramework(Frame):
    def __init__(self, master=None):
        self.config = Config()
        Frame.__init__(self, master)
        os.system('clear')
        self.master.geometry("%dx%d+%d+%d" % (710, 700, 0, 0))
        self.grid(padx=15, pady=15, sticky=N + S + E + W)

        # Theme configuration
        ttkstyle = ttk.Style()
        try:
            # OS X Default Theme
            ttkstyle.theme_use('aqua')
            self.master.configure(background='gray91')
            ttkstyle.configure('TFrame', background='gray91')
            ttkstyle.configure('TNotebook', background='gray91')
            self.BasicFont = tkFont.Font(family='Lucida Grande', size=12, weight='normal', slant='roman')
            self.HighlightFont = tkFont.Font(family='Helvetica', size=12, weight='bold', slant='italic')
            self.HighlightFont2 = tkFont.Font(family='Helvetica', size=12, weight='normal', slant='italic')

        except:
            # Modified Ubuntu Theme
            ttkstyle.theme_use('clam')
            self.master.configure(background='gray85')
            ttkstyle.configure('TButton', padding=1, background='gray80')
            ttkstyle.configure('TCombobox', padding=2)
            ttkstyle.map('TCombobox', fieldbackground=[('readonly', 'focus', 'gray90'), ('readonly', 'gray90')])
            ttkstyle.map('TEntry', selectbackground=[('!disabled', 'gray90')], selectforeground=[('!disabled', 'black')])
            ttkstyle.configure('TFrame', background='gray85')
            ttkstyle.configure('TLabel', background='gray85', padding=4)
            ttkstyle.configure('TNotebook', background='gray85')
            self.BasicFont = tkFont.Font(family='DejaVu Sans', size=10, weight='normal', slant='roman')
            self.HighlightFont = tkFont.Font(family='DejaVu Sans', size=10, weight='bold', slant='italic')
            self.HighlightFont2 = tkFont.Font(family='DejaVu Sans', size=10, weight='normal', slant='italic')
        ttkstyle.configure('.', font=self.BasicFont)

        self.master.title("PyE3D Gui")
        self.master.protocol('WM_DELETE_WINDOW', quit)
        self.Create_Main()

    def quit(self):
        self.master.destroy()

    def Create_Main(self):
        # Create notebook and subframes
        self.nb = ttk.Notebook(self.master)
        self.nb.grid(padx=10, pady=10)
        #self.f1 = ttk.Frame(width=700, height=300)
        self.f1 = ttk.Frame()
        self.f2 = ttk.Frame()
        self.f3 = ttk.Frame()
        self.f4 = ttk.Frame()
        self.f5 = ttk.Frame()
        self.f6 = ttk.Frame()
        self.f7 = ttk.Frame()
        self.nb.add(self.f1, text='Main')
        self.nb.add(self.f2, text='Advanced')
        self.nb.add(self.f3, text='Materials')
        self.nb.add(self.f4, text='Sources')
        self.nb.add(self.f5, text='Traces')
        self.nb.add(self.f6, text='Movies')
        self.nb.add(self.f7, text='Rendering')

        # Control buttons
        bwidth = 10
        self.btn_run = ttk.Button(self.master, text='Run PyE3D', width=bwidth, command=self.GUI_Run)
        self.btn_post = ttk.Button(self.master, text='Run Post', width=bwidth, command=self.GUI_Post)
        self.btn_save = ttk.Button(self.master, text='Save', width=bwidth, command=self.GUI_Save)
        self.btn_export = ttk.Button(self.master, text='Export', width=bwidth, command=self.GUI_Export)
        self.btn_load = ttk.Button(self.master, text='Load', width=bwidth, command=self.GUI_Load)
        self.btn_restore = ttk.Button(self.master, text='Restore', width=bwidth, command=self.GUI_Restore)

        # Grid main window
        self.nb.grid(row=0, column=0, columnspan=5, sticky=N + W + E + S)
        self.btn_run.grid(row=1, column=0, pady=5)
        self.btn_post.grid(row=2, column=0, pady=5)
        self.btn_save.grid(row=1, column=1, pady=5)
        self.btn_export.grid(row=2, column=1, pady=5)
        self.btn_load.grid(row=1, column=2, pady=5)
        self.btn_restore.grid(row=2, column=2, pady=5)

        #-----------------------------------------------------------------------------------
        # Basic Options (Frame 1)
        #-----------------------------------------------------------------------------------
        seprow = [6, 12]
        txt = ['Basic Setup', 'Model Size:', '   X', '   Y', '   Z', 'Model Origin:', '   X', '   Y', '   Z',
               'Model Spacing:', '   X', '   Y', '   Z', 'Model Time:', '   T', '', 'Boundary Conditions',
               'Type of Boundary:', 'Sponge Boundary:', 'Attenuating Boundary:', '', 'Analysis Options',
               'Run Model:', 'Type of Model:', 'Attenuation:', 'Number of Dimensions:']
        txtrow = [0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        txtcol = [0, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        txtbold = [0, 16, 21]
        enrow = [2, 2, 2, 3, 3, 3, 4, 4, 4, 5]
        encol = [2, 4, 6, 2, 4, 6, 2, 4, 6, 2]
        drrow = [9, 10, 11, 14, 15, 16, 17]
        drval = [('Reflecting', 'Quiet', 'Surface', 'Surface (acousitc)'), ('No', 'Yes'), ('No', 'Yes'), ('No', 'Yes'), ('Elastic', 'Acoustic'), ('No', 'Yes'), ('2', '3'), ('No', 'Yes')]

        # Store Handles
        self.lbText, self.enText, self.drBox = self.Create_BasicFrame(self.f1, seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)

        #-----------------------------------------------------------------------------------
        # Advanced Options (Frame 2)
        #-----------------------------------------------------------------------------------
        seprow = [4, 9]
        txt = ['Model Setup', 'Timestep Size:', 'ct/dt', 'Number of Runs:', 'N', 'MPI Nodes:', 'nX', '   nY',
               '   nZ', '', 'Material Control', 'Independant Parameters:', 'Model Generation:', 'Multiple Runs:',
               '', 'Input/Output Paths', 'Output Location:', 'Logfile Location:', 'Linking Directory:', 'E3D Path:',
               'Input Name:','Alert address:']
        txtrow = [0, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        txtcol = [0, 0, 1, 0, 1, 0, 1, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        txtbold = [0, 10, 15]
        enrow = [1, 2, 3, 3, 3, 11, 12, 13, 14, 15, 16]
        encol = [2, 2, 2, 4, 6, 1, 1, 1, 1, 1, 1]
        drrow = [6, 7, 8]
        drval = [('pvel', 'pvel, svel', 'pvel, svel, dens'), ('Create New', 'Copy Existing', 'Modify Existing'),
                 ('Independent', 'Create Initial')]

        # Store Handles
        self.adv_lbText, self.adv_enText, self.adv_drBox = self.Create_BasicFrame(self.f2, seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
        for ii in range(5, 11):
            self.adv_enText[ii].configure(width=40)
            self.adv_enText[ii].grid(columnspan=5)

        #-----------------------------------------------------------------------------------
        # Material Options (Frame 3)
        #-----------------------------------------------------------------------------------
        self.materialframes = ttk.Notebook(self.f3)
        self.materialframes.grid(row=0, column=0, columnspan=5, sticky=N + W + E + S, padx=5, pady=5)
        self.Create_MaterialFrames(len(self.config.material))

        # Basic Information
        self.lbText.append(ttk.Label(self.f3, text='Number of Regions:', font=self.HighlightFont2))
        self.nmat = ttk.Label(self.f3, text='1')
        self.btn_addmat = ttk.Button(self.f3, text='Add Region', width=15, command=self.GUI_AddMat)
        self.btn_delmat = ttk.Button(self.f3, text='Remove Region', width=15, command=self.GUI_DelMat)
        self.btn_render = ttk.Button(self.f3, text='Render Model', width=15, command=self.GUI_Render)

        self.lbText[-1].grid(row=1, column=0)
        self.nmat.grid(row=1, column=1, padx=15)
        self.btn_addmat.grid(row=1, column=2, padx=10, pady=5)
        self.btn_delmat.grid(row=1, column=3, padx=10, pady=5)
        self.btn_render.grid(row=2, column=2, padx=10, pady=5)

        #-----------------------------------------------------------------------------------
        # Source Options (Frame 4)
        #-----------------------------------------------------------------------------------
        self.sourceframes = ttk.Notebook(self.f4)
        self.sourceframes.grid(row=0, column=0, columnspan=5, sticky=N + W + E + S, padx=5, pady=5)
        self.Create_SourceFrames(len(self.config.source))

        # Basic Information
        self.lbText.append(ttk.Label(self.f4, text='Number of Sources:', font=self.HighlightFont2))
        self.nsource = ttk.Label(self.f4, text='1')
        self.btn_addsource = ttk.Button(self.f4, text='Add Source', width=15, command=self.GUI_AddSource)
        self.btn_delsource = ttk.Button(self.f4, text='Remove Source', width=15, command=self.GUI_DelSource)

        self.lbText[-1].grid(row=1, column=0)
        self.nsource.grid(row=1, column=1, padx=15)
        self.btn_addsource.grid(row=1, column=2, padx=10, pady=5)
        self.btn_delsource.grid(row=1, column=3, padx=10, pady=5)

        #-----------------------------------------------------------------------------------
        # Traces (Frame 5)
        #-----------------------------------------------------------------------------------
        self.traceframes = ttk.Notebook(self.f5)
        self.traceframes.grid(row=0, column=0, columnspan=5, sticky=N + W + E + S, padx=5, pady=5)
        self.Create_TraceFrames(len(self.config.output.traces))

        # Basic Information
        self.lbText.append(ttk.Label(self.f5, text='Number of Traces:', font=self.HighlightFont2))
        self.ntrace = ttk.Label(self.f5, text='1')
        self.btn_addtrace = ttk.Button(self.f5, text='Add Trace', width=15, command=self.GUI_AddTrace)
        self.btn_deltrace = ttk.Button(self.f5, text='Remove Trace', width=15, command=self.GUI_DelTrace)

        self.lbText[-1].grid(row=1, column=0)
        self.ntrace.grid(row=1, column=1, padx=15)
        self.btn_addtrace.grid(row=1, column=2, padx=10, pady=5)
        self.btn_deltrace.grid(row=1, column=3, padx=10, pady=5)

        #-----------------------------------------------------------------------------------
        # Movies (Frame 6)
        #-----------------------------------------------------------------------------------
        self.movieframes = ttk.Notebook(self.f6)
        self.movieframes.grid(row=0, column=0, columnspan=5, sticky=N + W + E + S, padx=5, pady=5)
        self.Create_MovieFrames(len(self.config.output.movies))

        # Basic Information
        self.lbText.append(ttk.Label(self.f6, text='Number of Movies:', font=self.HighlightFont2))
        self.nmovie = ttk.Label(self.f6, text='1')
        self.btn_addmovie = ttk.Button(self.f6, text='Add Movie', width=15, command=self.GUI_AddMovie)
        self.btn_delmovie = ttk.Button(self.f6, text='Remove Movie', width=15, command=self.GUI_DelMovie)

        self.lbText[-1].grid(row=1, column=0)
        self.nmovie.grid(row=1, column=1, padx=15)
        self.btn_addmovie.grid(row=1, column=2, padx=10, pady=5)
        self.btn_delmovie.grid(row=1, column=3, padx=10, pady=5)

        #-----------------------------------------------------------------------------------
        # Rendering Options (Frame 7)
        #-----------------------------------------------------------------------------------
        seprow = [4, 8, 12]
        txt = ['Render Outputs', 'Models:', 'Traces:', 'Movies:', '', 'Output Decimation', 'Time:', 'nt', 'Space:',
               'nx', '', 'Filtering (not enabled in this version)', 'Type:', 'Range:', '   f1', '   f2', '', 'Etc.',
               'Saturation']
        txtrow = [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 9, 10, 11, 11, 11, 12, 13, 14]
        txtcol = [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 3, 0, 0, 0]
        txtbold = [0, 5, 11, 17]
        enrow = [6, 7, 11, 11, 14]
        encol = [2, 2, 2, 4, 2]
        drrow = [1, 2, 3, 10]
        drval = [('No', 'Yes'), ('No', 'Yes'), ('No', 'Yes'), ('None', 'Lowpass', 'Highpass', 'Bandpass')]

        # Store Handles
        self.rend_lbText, self.rend_enText, self.rend_drBox = self.Create_BasicFrame(self.f7, seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
        self.rend_drBox[3].bind('<<ComboboxSelected>>', self.GUI_BtnUpdate)
        self.Update_Screen()

    def Create_MaterialFrames(self, N):
        frames = self.materialframes.tabs()
        for ii in frames:
            self.materialframes.forget(ii)
        self.mf = []
        self.material_enText = []
        self.material_drBox = []
        self.material_lbText = []
        for jj in range(0, N):
            self.mf.append(ttk.Frame())
            self.materialframes.add(self.mf[jj], text="Region %i" % (jj + 1))

            # Configuration
            seprow = [5, 10]
            txt = ['Material Properties', 'P-Velocity (km/s):', '   Avg', '   SD (%)', 'S-Velocity (km/s):',
                   '   Avg', '   SD (%)', 'Density (g/cc):', '   Avg', '   SD (%)', 'Attenuation:', '   Qp',
                   '   Qs', '', 'Statistical Distribution', 'Type:', 'Fractal Dimension:', '   fdim',
                   'Fractal Scaling:', '   fX', '   fY', '   fZ', '', 'Geometry', 'Type:', 'A', '  A0', '  A1',
                   '  A2', 'B', '  B0', '  B1', '  B2', 'C', '  C0', '  C1', '  C2']
            txtrow = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 8, 9, 9, 9, 9, 10, 11, 12, 13, 13, 13, 13,
                      14, 14, 14, 14, 15, 15, 15, 15]
            txtcol = [0, 0, 1, 3, 0, 1, 3, 0, 1, 3, 0, 1, 3, 0, 0, 0, 0, 1, 0, 1, 3, 5, 0, 0, 0, 0, 1, 3, 5, 0, 1,
                      3, 5, 0, 1, 3, 5]
            txtbold = [0, 14, 23]
            enrow = [1, 1, 2, 2, 3, 3, 4, 4, 8, 9, 9, 9, 13, 13, 13, 14, 14, 14, 15, 15, 15]
            encol = [2, 4, 2, 4, 2, 4, 2, 4, 2, 2, 4, 6, 2, 4, 6, 2, 4, 6, 2, 4, 6]
            drrow = [7, 12]
            drval = [('Homogeneous', 'Random', 'Fractal'), ('Rectangle', 'Sphere', 'Cylinder', 'Polynomial Surface',
                                                            'Planar Surface', 'Open Box', 'Entire Domain',
                                                            'Interp from File')]

            # Store Handles
            lbText, enText, drBox = self.Create_BasicFrame(self.mf[jj], seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
            self.material_lbText.append(lbText)
            self.material_enText.append(enText)
            self.material_drBox.append(drBox)
            self.material_drBox[jj][0].bind('<<ComboboxSelected>>', self.GUI_SetMaterialType)
            self.material_drBox[jj][1].bind('<<ComboboxSelected>>', self.GUI_BtnUpdate)

    def Create_MovieFrames(self, N):
        frames = self.movieframes.tabs()
        for ii in frames:
            self.movieframes.forget(ii)
        self.mvf = []
        self.movie_enText = []
        self.movie_drBox = []
        self.movie_lbText = []
        for jj in range(0, N):
            self.mvf.append(ttk.Frame())
            self.movieframes.add(self.mvf[jj], text="Movie %i" % (jj + 1))

            # Configuration
            seprow = []
            txt = ['Type:', '', 'Direction:', 'Position:', '   X=']
            txtrow = [0, 1, 2, 3, 3]
            txtcol = [0, 0, 0, 0, 1]
            txtbold = []
            enrow = [3]
            encol = [2]
            drrow = [0, 2]
            drval = [('Vx', 'Vy', 'Vz', 'Txx', 'Tyy', 'Tzz', 'Txy', 'Txz', 'Tyz', 'P Potential', 'S Potential'),
                     ('X', 'Y', 'Z')]

            # Store Handles
            lbText, enText, drBox = self.Create_BasicFrame(self.mvf[jj], seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
            self.movie_lbText.append(lbText)
            self.movie_enText.append(enText)
            self.movie_drBox.append(drBox)
            self.movie_drBox[jj][1].bind('<<ComboboxSelected>>', self.GUI_BtnUpdate)

    def Create_SourceFrames(self, N):
        frames = self.sourceframes.tabs()
        for ii in frames:
            self.sourceframes.forget(ii)
        self.sf = []
        self.source_enText = []
        self.source_drBox = []
        self.source_lbText = []
        for jj in range(0, N):
            self.sf.append(ttk.Frame())
            self.sourceframes.add(self.sf[jj], text="Source %i" % (jj + 1))

            # Configuration
            seprow = [6]
            txt = ['Characteristics', 'Source Type:', 'Wavelet Type:', 'Amplitude:', '   A', 'Frequency:', '   F',
                   'Offset:', '   O', '', 'Orientation', 'Position:', '   X', '   Y', '   Z', 'A', '   A0',
                   '   A1', '   A2', 'B', '   B0', '   B1', '   B2', '   B3', '   B4', '   B5']
            txtrow = [0, 1, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11]
            txtcol = [0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 3, 5, 0, 1, 3, 5, 0, 1, 3, 5, 1, 3, 5]
            txtbold = [0, 10]
            enrow = [3, 4, 5, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11]
            encol = [2, 2, 2, 2, 4, 6, 2, 4, 6, 2, 4, 6, 2, 4, 6]
            drrow = [1, 2]
            drval = [('P', 'S', 'None', 'Moment Tensor', 'Force', 'Point Fault', 'Finite Fault'),
                     ('Ricker', 'd/dt Gaussian', 'Gaussian')]

            # Generate Frames and Store Handles
            lbText, enText, drBox = self.Create_BasicFrame(self.sf[jj], seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
            self.source_lbText.append(lbText)
            self.source_enText.append(enText)
            self.source_drBox.append(drBox)
            self.source_drBox[jj][0].bind('<<ComboboxSelected>>', self.GUI_BtnUpdate)

    def Create_TraceFrames(self, N):
        frames = self.traceframes.tabs()
        for ii in frames:
            self.traceframes.forget(ii)
        self.tf = []
        self.trace_enText = []
        self.trace_drBox = []
        self.trace_lbText = []
        for jj in range(0, N):
            self.tf.append(ttk.Frame())
            self.traceframes.add(self.tf[jj], text="Trace %i" % (jj + 1))

            # Configuration
            seprow = []
            txt = ['Trace Direction:', '', 'Origin:', '   X', '   Y', '   Z', 'Number:', '   N', 'Spacing:', '   S', '',
                   'Corrections:']
            txtrow = [0, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 6]
            txtcol = [0, 0, 0, 1, 3, 5, 0, 1, 0, 1, 0, 0]
            txtbold = []
            enrow = [2, 2, 2, 3, 4]
            encol = [2, 4, 6, 2, 2]
            drrow = [0, 6]
            drval = [('X', 'Y', 'Z'), ('None', 'Spreading (Spherical)', 'Spreading (Surface)')]

            # Generate Frames and Store Handles
            lbText, enText, drBox = self.Create_BasicFrame(self.tf[jj], seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow)
            self.trace_lbText.append(lbText)
            self.trace_enText.append(enText)
            self.trace_drBox.append(drBox)

    def Create_BasicFrame(self, frame, seprow, txt, txtrow, txtcol, txtbold, enrow, encol, drval, drrow):
        # Separators
        sepr = []
        for ii in range(0, len(seprow)):
            sepr.append(ttk.Separator(frame, orient=HORIZONTAL))
            sepr[ii].grid(row=seprow[ii], column=0, columnspan=7, sticky=E + W, padx=10)

        # Labels
        lbText = []
        for ii in range(0, len(txt)):
            lbText.append(ttk.Label(frame, text=txt[ii]))
            lbText[ii].grid(row=txtrow[ii], column=txtcol[ii], sticky=W)
        for ii in txtbold:
            #lbText[ii].config(font='TkDefaultFont %i bold italic' % (self.txtsize))
            lbText[ii].config(font=self.HighlightFont)

        # Entries
        enText = []
        for ii in range(0, len(enrow)):
            enText.append(ttk.Entry(frame, width=12))
            enText[ii].grid(row=enrow[ii], column=encol[ii], padx=2)

        # Dropdown Boxes
        drBox = []
        for ii in range(0, len(drrow)):
            drBox.append(ttk.Combobox(frame, values=drval[ii], state='readonly'))
            drBox[ii].current(0)
            drBox[ii].grid(row=drrow[ii], column=1, columnspan=3, padx=10)

        # Return Handles
        return lbText, enText, drBox

    def Update_Screen(self):
        # Main Page
        for ii in range(0, 10):
            self.enText[ii].delete(0, END)
        self.enText[0].insert(0, self.config.model.size[0])
        self.enText[1].insert(0, self.config.model.size[1])
        self.enText[2].insert(0, self.config.model.size[2])
        self.enText[3].insert(0, self.config.model.origin[0])
        self.enText[4].insert(0, self.config.model.origin[1])
        self.enText[5].insert(0, self.config.model.origin[2])
        self.enText[6].insert(0, self.config.model.spacing[0])
        self.enText[7].insert(0, self.config.model.spacing[1])
        self.enText[8].insert(0, self.config.model.spacing[2])
        self.enText[9].insert(0, self.config.model.time)
        self.drBox[0].current(self.config.boundary.type - 1)
        self.drBox[1].current(self.config.boundary.sponge)
        self.drBox[2].current(self.config.boundary.atten)
        self.drBox[3].current(self.config.basic.run)
        self.drBox[4].current(self.config.basic.acoust - 1)
        self.drBox[5].current(self.config.basic.atten)
        self.drBox[6].current(self.config.model.dims - 2)

        # Advanced Page
        for ii in range(0, 11):
            self.adv_enText[ii].delete(0, END)
        self.adv_enText[0].insert(0, self.config.model.max_dtct)
        self.adv_enText[1].insert(0, self.config.basic.loopnum)
        self.adv_enText[2].insert(0, self.config.basic.multicore[0])
        self.adv_enText[3].insert(0, self.config.basic.multicore[1])
        self.adv_enText[4].insert(0, self.config.basic.multicore[2])
        self.adv_enText[5].insert(0, self.config.path.out)
        self.adv_enText[6].insert(0, self.config.path.log)
        self.adv_enText[7].insert(0, self.config.path.link)
        self.adv_enText[8].insert(0, self.config.path.bin)
        self.adv_enText[9].insert(0, self.config.path.fin)
        self.adv_enText[10].insert(0, self.config.path.email)
        self.adv_drBox[0].current(self.config.basic.degrees_free - 1)
        self.adv_drBox[1].current(self.config.basic.newmodel)
        self.adv_drBox[2].current(self.config.basic.multimodel)

        # Materials Page
        self.nmat.config(text=len(self.config.material))
        enrow = [13, 13, 13, 14, 14, 14, 15, 15, 15]
        encol = [2, 4, 6, 2, 4, 6, 2, 4, 6]
        mdic = {'Rectangle': [['First Corner:', '    X', '   Y', '   Z', 'Second Corner:', '   X', '   Y', '   Z', '', '', '', ''],
                              [1, 1, 1, 1, 1, 1, 0, 0, 0]],
                'Sphere': [['Center:', '   X', '   Y', '   Z', 'Radius:', '   R', '', '', '', '', '', ''],
                           [1, 1, 1, 1, 0, 0, 0, 0, 0]],
                'Cylinder': [['Point 1:', '   X', '   Y', '   Z', 'Point 2:', '   X', '   Y', '   Z', 'Radius:', '   R', '', ''],
                             [1, 1, 1, 1, 1, 1, 1, 0, 0]],
                'Polynomial Surface': [['f(X):', '   a0', '   a1', '   a2', 'f(Y):', '   a0', '   a1', '   a2', '', '', '', ''],
                                       [1, 1, 1, 1, 1, 1, 0, 0, 0]],
                'Planar Surface': [['Point:', '   X', '   Y', '   Z', 'Orient:', '   S', '   D', '', 'Rough/Thick:', '   L', '   A', '   T'],
                                   [1, 1, 1, 1, 1, 0, 1, 1, 1]],
                'Open Box': [['Width:', '   N', '', '', '', '', '', '', '', '', '', ''],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0]],
                'Entire Domain': [['', '', '', '', '', '', '', '', '', '', '', ''],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                'Interp from File': [['CSV File (X, Y, Z, Vp, Vs, Dens):', 'Path:', '', '', '', '', '', '', '', '', '', ''],
                                    [1, 0, 0, 0, 0, 0, 0, 0, 0]]}

        for ii in range(0, len(self.config.material)):
            for jj in range(0, 21):
                self.material_enText[ii][jj].delete(0, END)
            self.material_enText[ii][0].insert(0, self.config.material[ii].mn[0])
            self.material_enText[ii][1].insert(0, self.config.material[ii].sd[0] * 100)
            self.material_enText[ii][2].insert(0, self.config.material[ii].mn[1])
            self.material_enText[ii][3].insert(0, self.config.material[ii].sd[1] * 100)
            self.material_enText[ii][4].insert(0, self.config.material[ii].mn[2])
            self.material_enText[ii][5].insert(0, self.config.material[ii].sd[2] * 100)
            self.material_enText[ii][6].insert(0, self.config.material[ii].mn[3])
            self.material_enText[ii][7].insert(0, self.config.material[ii].mn[4])
            self.material_enText[ii][8].insert(0, self.config.material[ii].dist[0])
            self.material_enText[ii][9].insert(0, self.config.material[ii].dist[1])
            self.material_enText[ii][10].insert(0, self.config.material[ii].dist[2])
            self.material_enText[ii][11].insert(0, self.config.material[ii].dist[3])
            self.material_drBox[ii][1].current(self.config.material[ii].type - 1)
            mtype = self.material_drBox[ii][1].get()
            for jj in range(0, 9):
                self.material_enText[ii][jj + 12].insert(0, self.config.material[ii].geo[jj])

            if (amax(self.config.material[ii].sd) == 0):
                self.material_drBox[ii][0].current(0)
            elif (self.config.material[ii].dist[0] == -1.5):
                self.material_drBox[ii][0].current(1)
            else:
                self.material_drBox[ii][0].current(2)

            for jj in range(25, 37):
                self.material_lbText[ii][jj].configure(text=mdic[mtype][0][jj - 25])

            for jj in range(12, 21):
                if mdic[mtype][1][jj - 12]:
                    self.material_enText[ii][jj].grid(row=enrow[jj - 12], column=encol[jj - 12])
                else:
                    self.material_enText[ii][jj].grid_forget()

        # Source Page
        self.nsource.config(text=len(self.config.source))
        enrow = [9, 9, 9, 10, 10, 10, 11, 11, 11]
        encol = [2, 4, 6, 2, 4, 6, 2, 4, 6]
        sdic = {'P': [['', '', '', '', '', '', '', '', '', '', ''],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                'S': [['', '', '', '', '', '', '', '', '', '', ''],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                'None': [['', '', '', '', '', '', '', '', '', '', ''],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                'Moment Tensor': [['Tensor:', '   Mxx', '   Myy', '   Mzz', '','   Mxy', '   Mxz', '   Myz', '', '', '', ''],
                                  [1, 1, 1, 1, 1, 1, 0, 0, 0]],
                'Force': [['Direction:', '   Fx', '   Fy', '   Fz', '', '', '', '', '', '', ''],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0]],
                'Point Fault': [['Orientation:', 'Strike', 'Dip', 'Rake', '', '', '', '', '', '', ''],
                                [1, 1, 1, 0, 0, 0, 0, 0, 0]],
                'Finite Fault': [['Orientation:', 'Strike', 'Dip', 'Rake', 'Size:', 'L', 'W', 'D', 's0', 'd0', 'v'],
                                 [1, 1, 1, 1, 1, 1, 1, 1, 1]]}

        for ii in range(0, len(self.config.source)):
            for jj in range(0, 15):
                self.source_enText[ii][jj].delete(0, END)
            self.source_enText[ii][0].insert(0, self.config.source[ii].amp)
            self.source_enText[ii][1].insert(0, self.config.source[ii].freq)
            self.source_enText[ii][2].insert(0, self.config.source[ii].off)
            self.source_drBox[ii][0].current(self.config.source[ii].type - 1)
            self.source_drBox[ii][1].current(self.config.source[ii].wav)
            stype = self.source_drBox[ii][0].get()
            for jj in range(3, 6):
                self.source_enText[ii][jj].insert(0, self.config.source[ii].loc[jj - 3])

            if (self.config.source[ii].type == 4):
                for jj in range(6, 12):
                    self.source_enText[ii][jj].insert(0, self.config.source[ii].M[jj - 6])
            elif (self.config.source[ii].type == 5):
                for jj in range(6, 9):
                    self.source_enText[ii][jj].insert(0, self.config.source[ii].F[jj - 6])
            elif (self.config.source[ii].type >= 6):
                for jj in range(6, 14):
                    self.source_enText[ii][jj].insert(0, self.config.source[ii].orient[jj - 6])

            for jj in range(15, 26):
                self.source_lbText[ii][jj].configure(text=sdic[stype][0][jj - 15])

            for jj in range(6, 15):
                if sdic[stype][1][jj - 6]:
                    self.source_enText[ii][jj].grid(row=enrow[jj - 6], column=encol[jj - 6])
                else:
                    self.source_enText[ii][jj].grid_forget()

        # Trace Page
        self.ntrace.config(text=len(self.config.output.traces))
        tdic = {'x': 0, 'X': 0, 'y': 1, 'Y': 1, 'z': 2, 'Z': 2}
        for ii in range(0, len(self.config.output.traces)):
            for jj in range(0, 5):
                self.trace_enText[ii][jj].delete(0, END)
            self.trace_enText[ii][0].insert(0, self.config.output.traces[ii].loc[0])
            self.trace_enText[ii][1].insert(0, self.config.output.traces[ii].loc[1])
            self.trace_enText[ii][2].insert(0, self.config.output.traces[ii].loc[2])
            self.trace_enText[ii][3].insert(0, self.config.output.traces[ii].N)
            self.trace_enText[ii][4].insert(0, self.config.output.traces[ii].space)
            self.trace_drBox[ii][0].current(tdic[self.config.output.traces[ii].dir])
            self.trace_drBox[ii][1].current(self.config.output.traces[ii].corr)

        # Movie Page
        self.nmovie.config(text=len(self.config.output.movies))
        tdic = {'x': [0, '   X = '], 'X': [0, '   X = '], 'y': [1, '   Y = '], 'Y': [1, '   Y = '], 'z': [2, '   Z = '], 'Z': [2, '   Z = ']}
        for ii in range(0, len(self.config.output.movies)):
            self.movie_enText[ii][0].delete(0, END)
            self.movie_enText[ii][0].insert(0, self.config.output.movies[ii].loc)
            self.movie_drBox[ii][0].current(self.config.output.movies[ii].type - 11)
            self.movie_drBox[ii][1].current(tdic[self.config.output.movies[ii].dir][0])
            self.movie_lbText[ii][4].config(text=tdic[self.config.output.movies[ii].dir][1])

        # Rendering Page
        enrow = [11, 11]
        encol = [2, 4]
        mdic = {'None': [['', '', ''], [0, 0]],
                'Lowpass': [['Corner Frequency:', '   f1', ''], [1, 0]],
                'Highpass': [['Corner Frequency:', '', '   f2'], [0, 1]],
                'Bandpass': [['Corner Frequencies:', '   f1', '   f2'], [1, 1]]}

        for ii in range(0, 5):
                self.rend_enText[ii].delete(0, END)
        self.rend_enText[0].insert(0, self.config.output.dec_time)
        self.rend_enText[1].insert(0, self.config.output.dec_space)
        self.rend_enText[2].insert(0, self.config.output.bandpass[0])
        self.rend_enText[3].insert(0, self.config.output.bandpass[1])
        self.rend_enText[4].insert(0, self.config.output.scale_sat)
        self.rend_drBox[0].current(self.config.output.model)
        self.rend_drBox[1].current(self.config.output.trace)
        self.rend_drBox[2].current(self.config.output.movie)
        self.rend_drBox[3].current(self.config.output.filt)

        ftype = self.rend_drBox[3].get()
        for ii in range(13, 16):
            self.rend_lbText[ii].configure(text=mdic[ftype][0][ii - 13])
        for ii in range(2, 4):
            if mdic[ftype][1][ii - 2]:
                self.rend_enText[ii].grid(row=enrow[ii - 2], column=encol[ii - 2])
            else:
                self.rend_enText[ii].grid_forget()

    def Update_Config(self):
        # Main Page
        self.config.model.size[0] = float(self.enText[0].get())
        self.config.model.size[1] = float(self.enText[1].get())
        self.config.model.size[2] = float(self.enText[2].get())
        self.config.model.origin[0] = float(self.enText[3].get())
        self.config.model.origin[1] = float(self.enText[4].get())
        self.config.model.origin[2] = float(self.enText[5].get())
        self.config.model.spacing[0] = float(self.enText[6].get())
        self.config.model.spacing[1] = float(self.enText[7].get())
        self.config.model.spacing[2] = float(self.enText[8].get())
        self.config.model.number[0] = int(self.config.model.size[0] / self.config.model.spacing[0])
        self.config.model.number[1] = int(self.config.model.size[1] / self.config.model.spacing[1])
        self.config.model.number[2] = int(self.config.model.size[2] / self.config.model.spacing[2])
        self.config.model.time = float(self.enText[9].get())
        self.config.boundary.type = self.drBox[0].current() + 1
        self.config.boundary.sponge = self.drBox[1].current()
        self.config.boundary.atten = self.drBox[2].current()
        self.config.basic.run = self.drBox[3].current()
        self.config.basic.acoust = self.drBox[4].current() + 1
        self.config.basic.atten = self.drBox[5].current()
        self.config.model.dims = self.drBox[6].current() + 2

        # Advanced Page
        self.config.model.max_dtct = float(self.adv_enText[0].get())
        self.config.basic.loopnum = int(self.adv_enText[1].get())
        self.config.basic.multicore[0] = int(self.adv_enText[2].get())
        self.config.basic.multicore[1] = int(self.adv_enText[3].get())
        self.config.basic.multicore[2] = int(self.adv_enText[4].get())
        self.config.path.out = self.adv_enText[5].get()
        self.config.path.log = self.adv_enText[6].get()
        self.config.path.link = self.adv_enText[7].get()
        self.config.path.bin = self.adv_enText[8].get()
        self.config.path.fin = self.adv_enText[9].get()
        self.config.path.email = self.adv_enText[10].get()
        self.config.basic.degrees_free = self.adv_drBox[0].current() + 1
        self.config.basic.newmodel = self.adv_drBox[1].current()
        self.config.basic.multimodel = self.adv_drBox[2].current()

        # Materials Page
        for ii in range(0, len(self.config.material)):
            self.config.material[ii].mn[0] = float(self.material_enText[ii][0].get())
            self.config.material[ii].sd[0] = float(self.material_enText[ii][1].get()) * 0.01
            self.config.material[ii].mn[1] = float(self.material_enText[ii][2].get())
            self.config.material[ii].sd[1] = float(self.material_enText[ii][3].get()) * 0.01
            self.config.material[ii].mn[2] = float(self.material_enText[ii][4].get())
            self.config.material[ii].sd[2] = float(self.material_enText[ii][5].get()) * 0.01
            self.config.material[ii].mn[3] = float(self.material_enText[ii][6].get())
            self.config.material[ii].mn[4] = float(self.material_enText[ii][7].get())
            self.config.material[ii].dist[0] = float(self.material_enText[ii][8].get())
            self.config.material[ii].dist[1] = float(self.material_enText[ii][9].get())
            self.config.material[ii].dist[2] = float(self.material_enText[ii][10].get())
            self.config.material[ii].dist[3] = float(self.material_enText[ii][11].get())
            self.config.material[ii].type = self.material_drBox[ii][1].current() + 1
            if (self.config.material[ii].type <= 7):
                # Geometric Regions
                for jj in range(0, 9):
                    try:
                        self.config.material[ii].geo[jj] = float(self.material_enText[ii][jj + 12].get())
                    except ValueError:
                        self.config.material[ii].geo[jj] = 0.0
            else:
                # Interpolation Option
                tmp_path = self.material_enText[ii][12].get()
                if os.path.exists(tmp_path):
                    self.config.material[ii].geo[0] = tmp_path
                else:
                    self.config.material[ii].geo[0] = self.config.path.link + 'file.csv'  # Default path if not set


        # Source Page
        for ii in range(0, len(self.config.source)):
            self.config.source[ii].amp = float(self.source_enText[ii][0].get())
            self.config.source[ii].freq = float(self.source_enText[ii][1].get())
            self.config.source[ii].off = float(self.source_enText[ii][2].get())
            self.config.source[ii].type = self.source_drBox[ii][0].current() + 1
            self.config.source[ii].wav = self.source_drBox[ii][1].current()
            for jj in range(3, 6):
                    self.config.source[ii].loc[jj - 3] = float(self.source_enText[ii][jj].get())
            try:
                if (self.config.source[ii].type == 4):
                    for jj in range(6, 12):
                        self.config.source[ii].M[jj - 6] = float(self.source_enText[ii][jj].get())
                elif (self.config.source[ii].type == 5):
                    for jj in range(6, 9):
                        self.config.source[ii].F[jj - 6] = float(self.source_enText[ii][jj].get())
                elif (self.config.source[ii].type >= 6):
                    for jj in range(6, 14):
                        self.config.source[ii].orient[jj - 6] = float(self.source_enText[ii][jj].get())
            except:
                pass

        # Trace Page
        for ii in range(0, len(self.config.output.traces)):
            self.config.output.traces[ii].loc[0] = float(self.trace_enText[ii][0].get())
            self.config.output.traces[ii].loc[1] = float(self.trace_enText[ii][1].get())
            self.config.output.traces[ii].loc[2] = float(self.trace_enText[ii][2].get())
            self.config.output.traces[ii].N = int(self.trace_enText[ii][3].get())
            self.config.output.traces[ii].space = float(self.trace_enText[ii][4].get())
            self.config.output.traces[ii].dir = self.trace_drBox[ii][0].get()
            self.config.output.traces[ii].corr = self.trace_drBox[ii][1].current()

        # Movie Page
        for ii in range(0, len(self.config.output.movies)):
            self.config.output.movies[ii].loc = float(self.movie_enText[ii][0].get())
            self.config.output.movies[ii].type = self.movie_drBox[ii][0].current() + 11
            self.config.output.movies[ii].dir = self.movie_drBox[ii][1].get()

        # Rendering Page
        self.config.output.dec_time = int(self.rend_enText[0].get())
        self.config.output.dec_space = int(self.rend_enText[1].get())
        self.config.output.bandpass[0] = float(self.rend_enText[2].get())
        self.config.output.bandpass[1] = float(self.rend_enText[3].get())
        self.config.output.scale_sat = float(self.rend_enText[4].get())
        self.config.output.model = self.rend_drBox[0].current()
        self.config.output.trace = self.rend_drBox[1].current()
        self.config.output.movie = self.rend_drBox[2].current()
        self.config.output.filt = self.rend_drBox[3].current()

    def GUI_Render(self):
        self.Update_Config()
        self.config.save()
        self.master.withdraw()
        e3d_main.render()
        self.master.update()
        self.master.deiconify()

    def GUI_Run(self):
        self.Update_Config()
        self.config.save()
        self.master.withdraw()
        e3d_main.run_simulation()
        self.master.update()
        self.master.deiconify()

    def GUI_Post(self):
        self.Update_Config()
        self.config.save()
        self.master.withdraw()
        e3d_main.run_post()
        self.master.update()
        self.master.deiconify()

    def GUI_Save(self):
        self.Update_Config()
        self.config.save()

    def GUI_Export(self):
        self.Update_Config()
        filename = asksaveasfilename()
        self.config.save(filename)

    def GUI_Load(self):
        filename = askopenfilename()
        self.config.load(filename)
        self.Create_MaterialFrames(len(self.config.material))
        self.Create_SourceFrames(len(self.config.source))
        self.Create_TraceFrames(len(self.config.output.traces))
        self.Create_MovieFrames(len(self.config.output.movies))
        self.Update_Screen()

    def GUI_Restore(self):
        self.config.default()
        self.Create_MaterialFrames(len(self.config.material))
        self.Create_SourceFrames(len(self.config.source))
        self.Create_TraceFrames(len(self.config.output.traces))
        self.Create_MovieFrames(len(self.config.output.movies))
        self.Update_Screen()

    def GUI_AddMat(self):
        self.Update_Config()
        try:
            frame = self.materialframes.index(self.materialframes.select()) + 1
        except:
            frame = 0
        self.config.addmaterial(frame)
        self.Create_MaterialFrames(len(self.config.material))
        self.Update_Screen()

    def GUI_DelMat(self):
        self.Update_Config()
        frame = self.materialframes.index(self.materialframes.select())
        self.config.delmaterial(frame)
        self.Create_MaterialFrames(len(self.config.material))
        self.Update_Screen()

    def GUI_AddSource(self):
        self.Update_Config()
        try:
            frame = self.sourceframes.index(self.sourceframes.select()) + 1
        except:
            frame = 0
        self.config.addsource(frame)
        self.Create_SourceFrames(len(self.config.source))
        self.Update_Screen()

    def GUI_DelSource(self):
        self.Update_Config()
        frame = self.sourceframes.index(self.sourceframes.select())
        self.config.delsource(frame)
        self.Create_SourceFrames(len(self.config.source))
        self.Update_Screen()

    def GUI_AddTrace(self):
        self.Update_Config()
        try:
            frame = self.traceframes.index(self.traceframes.select()) + 1
        except:
            frame = 0
        self.config.output.addtrace(frame)
        self.Create_TraceFrames(len(self.config.output.traces))
        self.Update_Screen()

    def GUI_DelTrace(self):
        self.Update_Config()
        frame = self.traceframes.index(self.traceframes.select())
        self.config.output.deltrace(frame)
        self.Create_TraceFrames(len(self.config.output.traces))
        self.Update_Screen()

    def GUI_AddMovie(self):
        self.Update_Config()
        try:
            frame = self.movieframes.index(self.movieframes.select()) + 1
        except:
            frame = 0
        self.config.output.addmovie(frame)
        self.Create_MovieFrames(len(self.config.output.movies))
        self.Update_Screen()

    def GUI_DelMovie(self):
        self.Update_Config()
        frame = self.movieframes.index(self.movieframes.select())
        self.config.output.delmovie(frame)
        self.Create_MovieFrames(len(self.config.output.movies))
        self.Update_Screen()

    def GUI_BtnUpdate(self, *_):
        self.Update_Config()
        self.Update_Screen()

    def GUI_SetMaterialType(self, *_):
        self.Update_Config()
        frame = self.materialframes.index(self.materialframes.select())
        mtype = self.material_drBox[frame][0].current()

        if (mtype == 0):
            mset = [0, 0, 0, -1.5]
        elif (mtype == 1):
            mset = [0.01, 0.01, 0.01, -1.5]
        else:
            mset = [0.01, 0.01, 0.01, 0]

        self.config.material[frame].sd[0] = mset[0]
        self.config.material[frame].sd[1] = mset[1]
        self.config.material[frame].sd[2] = mset[2]
        self.config.material[frame].dist[0] = mset[3]

        self.Update_Screen()

if __name__ == "__main__":
    guiFrame = GUIFramework()
    guiFrame.mainloop()
