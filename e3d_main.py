from e3d_classes import *
from e3d_functions import *


def run_simulation():
    os.system('clear')
    config = Config()

    # Setup the linking and working directory
    if os.path.exists(config.path.link):
        tdir = sorted(glob.glob(config.path.link + '/1*'))
        if tdir:
            link_off = float(tdir[-1][-3:]) + 1
        else:
            link_off = 100
    else:
        os.mkdir(config.path.link)
        link_off = 100

    # Open the log file
    log = open(config.path.log + 'e3d_log.txt', 'a+')
    log.write("\n\n\nNew set of models for %s:\n\n" % (config.path.usr))

    for loop in range(0, config.basic.loopnum):
        #--------------------------------------------------------------------
        #				Workspace Configuration
        #--------------------------------------------------------------------
        # Update configuration and print to screen
        config = update_config(config, loop)
        print("\n\n\nModel #%i out of %i" % (loop + 1, config.basic.loopnum))
        print("----------------------------------------------\n")

        # Setup and link the working directory
        today = strftime('%d-%b-%Y', localtime())
        if os.path.exists(config.path.out + today):
            tdir = sorted(glob.glob(config.path.out + today + '/1*'))
            if tdir:
                work_off = float(tdir[-1][-3:]) + 1
            else:
                work_off = 100
        else:
            os.mkdir(config.path.out + today)
            work_off = 100

        workdir = config.path.out + today + '/' + str(int(work_off))
        linkdir = config.path.link + str(int(link_off + loop))
        os.mkdir(workdir)
        os.chdir(workdir)
        os.symlink(workdir, linkdir)
        log.write("Simulation #%s: %s\n" % (loop, workdir))
        log.write(config.path.log_msg + '\n')

        # Record the location of the first model, and link if requested
        if (loop == 0):
            config.path.firstmodel = workdir
        if (config.basic.multimodel == 1) & (loop > 0):
            config.path.oldmodel = config.path.firstmodel
            config.basic.newmodel = 1
            config.output.model = 0

        # Naming convention for files
        ft = ['pvel', 'svel', 'rden', 'patn', 'satn']
        ft2 = ['p', 's', 'r', 'Qp', 'Qs']
        ft3 = ['P-wave velocity file', 'S-wave velocity file', 'Density file', 'Qp file', 'Qs file']
        comp = {'x': 0, 'X': 0, 'y': 1, 'Y': 1, 'z': 2, 'Z': 2}
        mtype = ['Vx', 'Vy', 'Vz', 'Txx', 'Tyy', 'Tzz', 'Txy', 'Txz', 'Tyz', 'FP', 'FS']
        gridsize = []
        inputsize = []

        # Choose which material files to write
        if (config.basic.acoust == 2):
            config.basic.atten = 0
            config.basic.degrees_free = 1
            n_inputs = 1
        elif (config.basic.atten == 0):
            n_inputs = 3
        else:
            n_inputs = 5

        #--------------------------------------------------------------------
        #				Generate Material Files
        #--------------------------------------------------------------------
        if (config.basic.newmodel == 0) | (config.basic.newmodel == 2):
            # Determine the number of steps:
            n_regions = len(config.material)
            #wh_steps = (n_regions + 1) * (n_inputs + 1)

            # 2D/3D
            if (config.model.dims == 2):
                config.model.number[1] = 1

            # Locate materials and boundaries
            for ii in range(0, n_regions):
                e3d_locate(config.model, config.material[ii].type, config.material[ii].geo, ii)
            if (config.boundary.rand == 1):
                e3d_locate(config.model, 6, [4], 'rand')
            if (config.boundary.atten == 1) & (config.basic.atten):
                e3d_locate(config.model, 6, [config.boundary.atten_thick], 'atten')

            # Loop over material types
            region = Region(config.model)
            fractal = Mfile(config.model)
            velocity = Mfile(config.model)
            for ii in range(0, n_inputs):
                # Read an old material file
                if (config.basic.newmodel == 2):
                        fractal.read(config.model, config.path.oldmodel + ft[ii] + '.pv')

                # Generate fractal distribution if a degree of freedom is available
                if (ii < config.basic.degrees_free):
                    print("\nGenerating fractal distribution")
                    for jj in range(0, n_regions):
                        fractal_tmp = e3d_fractal(config.model, config.material[jj].dist)
                        region.load(jj)
                        fractal.v = region.copy(fractal_tmp, fractal.v)
                    if (config.boundary.rand == 1):
                        fractal_tmp = zeros(config.model.number)
                        region.load('rand')
                        fractal.v = region.copy(fractal_tmp, fractal.v)

                # Scale the fractal distribution appropriately
                print("Writing %s" % ft3[ii])
                velocity.v = fractal.v
                for jj in range(0, n_regions):
                    if (config.material[jj].type <= 7):
                        mn = config.material[jj].mn[ii]
                        sd = config.material[jj].sd[ii]
                        region.load(jj)
                        velocity.v = region.scale(fractal.v, velocity.v, mn, sd)
                    else:
                        velocity.readfromcsv(config.model, config.material[jj].geo[0], ii)

                if (ii >= 3) & (config.boundary.atten == 1):
                    region.load('atten')
                    velocity.v = region.scale(fractal.v, velocity.v, config.boundary.atten_val, 0) 

                # Record important information about the model, and write:
                config.model.v_avg[ii] = mean(velocity.v)
                config.model.v_max[ii] = amax(velocity.v)
                config.model.v_min[ii] = amin(velocity.v)
                velocity.write(config.model, "./%s.pv" % (ft[ii]))
        else:
            #Link to existing files
            velocity = Mfile(config.model)
            for ii in range(0, n_inputs):
                velocity.read(config.model, "%s%s.pv" % (config.path.oldmodel, ft[ii]))

        # Render any model files
        if (config.output.model == 1):
            print "\nRendering models"
            for ii in range(0, n_inputs):
                try:
                    velocity.read(config.model, "./%s.pv" % (ft[ii]))
                    velocity.plot(config.model, config.output)
                except:
                    print "Failed to render ./%s.pv" % (ft[ii])

        del fractal, region, velocity
        rm = glob.glob('./region*.pkl')
        for ii in rm:
            os.remove(ii)

        #--------------------------------------------------------------------
        #					Configure E3D Inputs
        #--------------------------------------------------------------------
        # Determine the appropriate time step size
        if (config.model.dims == 2):
            courant = 0.494
        else:
            courant = 0.606

        dt = (courant * config.model.max_dtct * config.model.spacing[0]) / config.model.v_max[0]
        config.model.dt = float("%2.1e" % dt)
        config.model.timesteps = int(config.model.time / config.model.dt)

        # Grid and input file sizes
        for ii in range(0, 3):
            gridsize.append(max(config.model.number[ii] - 1, 1)) 	# n, m, l
            inputsize.append(config.model.number[ii] - 1)			# n2, m2, l2

        # Check the seismic source frequency
        freqlim = min(1 / (2 * config.model.dt), config.model.v_min[0] / (10 * config.model.spacing[0]))
        sfreq = []
        for ii in range(0, len(config.source)):
            if (config.source[ii].freq > freqlim):
                config.source[ii].freq = freqlim
                print 'Warning: Desired source frequency too large...  reducing f to %f Hz' % (freqlim)
            sfreq.append(config.source[ii].freq)
        fmean = mean(sfreq)

        # Determine seismogram locations
        if config.output.traces:
            ntrace = 0
            for trace in config.output.traces:
                tmp = tile(trace.loc, (trace.N, 1))
                tmp[:, comp[trace.dir]] = tmp[:, comp[trace.dir]] + arange(0, trace.N) * trace.space
                # tmp[:, comp[trace.dir]] = tmp[:, comp[trace.dir]] + linspace(0, trace.N * trace.space, trace.N)
                if (ntrace == 0):
                    tracefile = tmp
                else:
                    append(tracefile, tmp, 0)
                ntrace += trace.N
            for ii in range(0, 2):
                tracefile[:, ii] = tracefile[:, ii] - config.model.origin[ii]
            with open('trace', 'wb') as f:
                writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(tracefile)

        #--------------------------------------------------------------------
        #					Write E3D Input File
        #--------------------------------------------------------------------
        print("\nWriting E3D input file")
        with open(config.path.fin, 'w') as fid:
            # Grid options
            fid.write("grid n=%i l=%i m=%i dh=%s" % (gridsize[0], gridsize[1], gridsize[2], config.model.spacing[0]))
            if (config.boundary.sponge == 1):
                fid.write(" damp=10 adamp=0.95")
            fid.write(" model=%i b=%i" % (config.basic.acoust, config.boundary.type))
            if (config.basic.atten == 1):
                fid.write(" q=1")
            fid.write('\n')

            # MPI options
            if (max(config.basic.multicore) > 1):
                fid.write("parallel nx=%i ny=%i nz=%i\n" % (config.basic.multicore[0], config.basic.multicore[1], config.basic.multicore[2]))

            # Time options
            fid.write("time t=%i dt=%2.1e\n" % (config.model.timesteps, config.model.dt))

            # Velocity, density, attenuation options
            fid.write("block p=%s s=%s r=%s" % (config.material[0].mn[0], config.material[0].mn[1], config.material[0].mn[2]))
            if (config.basic.atten):
                fid.write(" Qp=%s Qs=%s Qf=%s" % (config.material[0].mn[3], config.material[0].mn[4], fmean))
            fid.write("\n")
            for ii in range(0, n_inputs):
                fid.write("vfile type=%s file=\"%s.pv\" n1=0 n2=%i l1=0 l2=%i m1=0 m2=%i\n" % (ft2[ii], ft[ii], inputsize[0], inputsize[1], inputsize[2]))

            # Source options
            for ss in config.source:
                fid.write("source type=%i amp=%1.4e x=%s y=%s z=%s" % (ss.type, ss.amp, ss.loc[0], ss.loc[1], ss.loc[2]))
                if (ss.type == 4):
                    fid.write(" Mxx=%s Myy=%s Mzz=%s Mxy=%s Mxz=%s Myz=%s" % (ss.M[0], ss.M[1], ss.M[2], ss.M[3], ss.M[4], ss.M[5]))
                elif (ss.type == 5):
                    fid.write(" Fx=%s Fy=%s Fz=%s" % (ss.F[0], ss.F[1], ss.F[2]))
                elif (ss.type == 6):
                    fid.write(" strike=%s dip=%s rake=%s" % (ss.orient[0], ss.orient[1], ss.orient[2]))
                elif (ss.type == 7):
                    fid.write(" strike=%s dip=%s rake=%s length=%s width=%s depth=%s s0=%s d0=%s v=%s" % (ss.orient[0], ss.orient[1], ss.orient[2], ss.orient[3], ss.orient[4], ss.orient[5], ss.orient[6], ss.orient[7], ss.orient[8]))
                if (ss.wav == 0):
                    fid.write(" t0=%s freq=%s\n" % (ss.off, ss.freq))
                else:
                    e3d_wavelet(config.model, ss)
                    fid.write(" file=\"wav.sac\"\n")

            # Output options
            if config.output.traces:
                fid.write("traces file=\"out\" tfile=\"trace\" sample=%i mode=7\n" % (config.output.dec_time))
            for mov in config.output.movies:
                mloc = mov.loc - config.model.origin[comp[mov.dir]]
                fid.write("image movie=%i sample=%i %s=%s mode=%i file=\"%s_%s\"\n" % (config.output.dec_time, config.output.dec_space, mov.dir.lower(), mloc, mov.type, mov.dir.lower(), mov.loc))

        #--------------------------------------------------------------------
        #						Run E3D
        #--------------------------------------------------------------------
        config.save('./model.pkl')
        if (config.basic.run == 1):
            # Call E3D
            print("\nSending Model to E3D\nTimesteps = %i\n" % (config.model.timesteps))
            if (max(config.basic.multicore) > 1):
                ncores = config.basic.multicore[0] * config.basic.multicore[1] * config.basic.multicore[2]
                subprocess.call(['mpirun', '-np', str(ncores), '--cpus-per-proc', '1', "%se3d" % config.path.bin, config.path.fin])
            else:
                subprocess.call([config.path.bin + 'e3d', config.path.fin])

            # Render any outputs
            if (config.output.trace == 1):
                try:
                    print("Rendering traces")
                    tracefile = Tfile()

                    print("     ./out.0.TVx")
                    tracefile.read('out.0.TVx', config.output.traces)
                    tracefile.correct(config.source[0])
                    tracefile.plot(config.output)

                    if (config.model == 3):
                        print("     ./out.0.TVy")
                        tracefile.read('out.0.TVy', config.output.traces)
                        tracefile.correct(config.source[0])
                        tracefile.plot(config.output)

                    print("     ./out.0.TVz")
                    tracefile.read('out.0.TVz', config.output.traces)
                    tracefile.correct(config.source[0])
                    tracefile.plot(config.output)

                    del tracefile
                except:
                    print("     (No trace files rendered)")

            if (config.output.movie == 1):
                try:
                    print("Rendering movies")
                    movfile = Vfile()
                    for mov in config.output.movies:
                        print("     ./%s_%s.%s" % (mov.dir.lower(), mov.loc, mtype[mov.type - 11]))
                        movfile.load(config.model, config.basic.multicore, "%s_%s.%s" % (mov.dir.lower(), mov.loc, mtype[mov.type - 11]))
                        movfile.read()
                        movfile.plot(config.output)
                    del movfile
                except:
                    print("     (No movie files rendered)")

    # Cleanup
    log.close()
    print("\nFinished!\n")
    e3d_gmail('youremailhere', 'PyE3D', "%s Simulations completed successfuly!" % (loop + 1))


def render():
    os.system('clear')
    config = Config()
    try:
        os.mkdir('./tmp')
    except:
        rm = glob.glob('./*.mp4')
        for ii in rm:
            os.remove(ii)
    os.chdir('./tmp')

    # Naming convention for files
    ft = ['pvel', 'svel', 'rden', 'patn', 'satn']
    ft3 = ['P-wave velocity file', 'S-wave velocity file', 'Density file', 'Qp file', 'Qs file']

    # Choose which material files to write
    if (config.basic.acoust == 2):
        config.basic.atten = 0
        config.basic.degrees_free = 1
        n_inputs = 1
    elif (config.basic.atten == 0):
        n_inputs = 3
    else:
        n_inputs = 5

    #--------------------------------------------------------------------
    #				Generate Material Files
    #--------------------------------------------------------------------
    if (config.basic.newmodel == 0) | (config.basic.newmodel == 2):
        # Determine the number of steps:
        n_regions = len(config.material)

        # Locate materials and boundaries
        for ii in range(0, n_regions):
            e3d_locate(config.model, config.material[ii].type, config.material[ii].geo, ii)
        if (config.boundary.rand == 1):
            e3d_locate(config.model, 6, [4], 'rand')
        if (config.boundary.atten == 1) & (config.basic.atten):
            e3d_locate(config.model, 6, [config.boundary.atten_thick], 'atten')

        # Loop over material types
        region = Region(config.model)
        fractal = Mfile(config.model)
        velocity = Mfile(config.model)
        for ii in range(0, n_inputs):
            # Read an old material file
            if (config.basic.newmodel == 2):
                    fractal.read(config.model, config.path.oldmodel + ft[ii] + '.pv')

            # Generate fractal distribution if a degree of freedom is available
            if (ii < config.basic.degrees_free):
                print("\nGenerating fractal distribution")
                for jj in range(0, n_regions):
                    fractal_tmp = e3d_fractal(config.model, config.material[jj].dist)
                    region.load(jj)
                    fractal.v = region.copy(fractal_tmp, fractal.v)
                if (config.boundary.rand == 1):
                    fractal_tmp = zeros(config.model.number)
                    region.load('rand')
                    fractal.v = region.copy(fractal_tmp, fractal.v)

            # Scale the fractal distribution appropriately
            print("Writing %s" % ft3[ii])
            velocity.v = fractal.v
            for jj in range(0, n_regions):
                if (config.material[jj].type <= 7):
                    mn = config.material[jj].mn[ii]
                    sd = config.material[jj].sd[ii]
                    region.load(jj)
                    velocity.v = region.scale(fractal.v, velocity.v, mn, sd)
                else:
                    velocity.readfromcsv(config.model, config.material[jj].geo[0], ii)

            if (ii >= 3) & (config.boundary.atten == 1):
                region.load('atten')
                velocity.v = region.scale(velocity.v, config.boundary.atten_val, 0)

            # Record important information about the model, and write:
            config.model.v_avg[ii] = mean(velocity.v)
            config.model.v_max[ii] = amax(velocity.v)
            config.model.v_min[ii] = amin(velocity.v)
            velocity.write(config.model, "./%s.pv" % (ft[ii]))
    else:
        #Link to existing files
        velocity = Mfile(config.model)
        for ii in range(0, n_inputs):
            velocity.read(config.model, "%s%s.pv" % (config.path.oldmodel, ft[ii]))

    # Render any model files
    if (config.output.model == 1):
        print "\nRendering models"
        for ii in range(0, n_inputs):
            try:
                velocity.read(config.model, "./%s.pv" % (ft[ii]))
                velocity.plot(config.model, config.output)
            except:
                print "Failed to render ./%s.pv" % (ft[ii])

    del fractal, region, velocity
    rm = glob.glob('./region*.pkl') + glob.glob('./*.pv')
    for ii in rm:
        os.remove(ii)

    # Cleanup
    os.chdir('..')
    print('\nDone...  Rendered models placed in ./tmp')


def run_post():
    os.system('clear')
    config = Config()
    tmp_config = Config()
    tdir = glob.glob(config.path.link + '/1*')
    ft = ['pvel', 'svel', 'rden', 'patn', 'satn']
    mtype = ['Vx', 'Vy', 'Vz', 'Txx', 'Tyy', 'Tzz', 'Txy', 'Txz', 'Tyz', 'FP', 'FS']

    for subdir in tdir:
        print("\n%s" % (subdir))
        os.chdir(subdir)
        tmp_config.load('./model.pkl')

        if (config.output.model == 1):
            try:
                print("Rendering models")

                if (tmp_config.basic.acoust == 2):
                    n_inputs = 1
                elif (tmp_config.basic.atten == 0):
                    n_inputs = 3
                else:
                    n_inputs = 5

                velocity = Mfile(tmp_config.model)
                for ii in range(0, n_inputs):
                    print("     ./%s.pv" % (ft[ii]))
                    velocity.read(tmp_config.model, "./%s.pv" % (ft[ii]))
                    velocity.plot(tmp_config.model, config.output)
                del velocity
            except:
                print("     (No model files rendered)")

        if (config.output.trace == 1):
            try:
                print("Rendering traces")
                tracefile = Tfile()

                print("     ./out.0.TVx")
                tracefile.read('out.0.TVx', tmp_config.output.traces)
                tracefile.correct(tmp_config.source[0])
                tracefile.plot(config.output)

                if (config.model == 3):
                    print("     ./out.0.TVy")
                    tracefile.read('out.0.TVy', tmp_config.output.traces)
                    tracefile.correct(tmp_config.source[0])
                    tracefile.plot(config.output)

                print("     ./out.0.TVz")
                tracefile.read('out.0.TVz', tmp_config.output.traces)
                tracefile.correct(tmp_config.source[0])
                tracefile.plot(config.output)

                del tracefile
            except:
                print("     (No trace files rendered)")

        if (config.output.movie == 1):
            try:
                print("Rendering movies")
                movfile = Vfile()
                for mov in tmp_config.output.movies:
                    print("     ./%s_%s.%s" % (mov.dir.lower(), mov.loc, mtype[mov.type - 11]))
                    movfile.load(tmp_config.model, tmp_config.basic.multicore, "%s_%s.%s" % (mov.dir.lower(), mov.loc, mtype[mov.type - 11]))
                    movfile.read()
                    movfile.plot(config.output)
                del movfile
            except:
                print("     (No movie files rendered)")

        print "Finished"
