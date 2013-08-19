import csv
import glob
import os
import pickle
import smtplib
import subprocess
import warnings
import matplotlib as plt
from pylab import *
from numpy import *
from scipy import signal
import matplotlib.animation as animation
from matplotlib.patches import Patch
from time import localtime, strftime


#--------------------------------------------------------------------
#				Configuration Data
#--------------------------------------------------------------------


class Config:
    def __init__(self):
        try:
            self.load('./e3d_default.pkl')
        except:
            self.default()
            self.save()

    def addmaterial(self, N):
        self.material.insert(N, Material())

    def addsource(self, N):
        self.source.insert(N, Source())
        #self.source = self.source + [Source()]

    def default(self):
        self.basic = Basic()
        self.boundary = Boundary()
        self.material = [Material()]
        self.model = Model()
        self.path = Path()
        self.source = [Source()]
        self.output = Output()

    def delmaterial(self, N):
        self.material.pop(N)

    def delsource(self, N):
        self.source.pop(N)

    def load(self, name):
        back = open(name, 'rb')
        tmp = pickle.load(back)
        back.close()
        self.__dict__.update(tmp)

    def save(self, name='./e3d_default.pkl'):
        back = open(name, 'wb')
        pickle.dump(self.__dict__, back, 2)
        back.close()

    def update(self, loop):
        self.path.log_msg = "Test %s" % loop


class Basic:
    def __init__(self):
        #Basic Configuration
        self.acoust = 1
        self.atten = 0
        self.degrees_free = 1
        self.loopnum = 1
        self.multicore = [1, 1, 1]
        self.multimodel = 0
        self.newmodel = 0
        self.run = 1
        self.units = 1


class Boundary:
    def __init__(self):
        #Boundary Configuration
        self.type = 3
        self.sponge = 0
        self.atten = 1
        self.atten_thick = 25
        self.atten_val = 5
        self.rand = 1


class Material():
    def __init__(self):
        self.mn = [3.0, 1.73, 2.7, 40.0, 40.0]
        self.sd = [0.01, 0.01, 0.0, 0.0, 0.0]
        self.dist = [0.0, 1.0, 1.0, 1.0]
        self.type = 7
        self.geo = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


class Model:
    def __init__(self):
        self.dims = 3
        self.size = [1.0, 1.0, 1.0]
        self.spacing = [0.005, 0.005, 0.005]
        self.number = [200, 200, 200]
        self.origin = [0.0, 0.0, 0.0]
        self.time = 1.0
        self.dt = 1e-3
        self.timesteps = 1e3
        self.max_dtct = 0.1
        self.v_avg = [0, 0, 0, 0, 0]
        self.v_min = [0, 0, 0, 0, 0]
        self.v_max = [0, 0, 0, 0, 0]


class Movies:
    def __init__(self):
        self.dir = 'z'
        self.loc = 0.5
        self.type = 13


class Output:
    def __init__(self):
        self.filt = 0
        self.bandpass = [0.0, 1.0e5]
        self.dec_space = 5
        self.dec_time = 10
        self.model = 1
        self.movie = 1
        self.trace = 1
        self.font = 'Helvetica'
        self.fontsize = '12'
        self.hres = 480               # Horizontal resolution
        self.hratio = 4.0 / 3.0       # Widescreen = 16.0/9.0
        self.sres = 50                # Screen resolution
        self.dpi = 150                # Print resolution
        self.fsize = (4, 3)           # Print size
        self.scale_sat = 1            # Colorbar saturation

        #Add one trace and movie by default
        self.movies = [Movies()]
        self.traces = [Traces()]

    def addmovie(self, N):
        self.movies.insert(N, Movies())

    def delmovie(self, N):
        self.movies.pop(N)

    def addtrace(self, N):
        self.traces.insert(N, Traces())

    def deltrace(self, N):
        self.traces.pop(N)


class Path:
    def __init__(self):
        self.usr = str(raw_input('Input Username:  '))
        self.bin = os.path.expanduser('/usr/local/SeismicTools/E3D/bin/')
        self.fin = 'E3D_in.txt'
        self.firstmodel = ''
        self.link = os.path.expanduser('~/SeismicTools/E3D/Link/')
        self.log = os.path.expanduser('~/Dropbox/Python/PyE3D/')
        self.log_msg = 'Test Model'
        self.oldmodel = os.path.expanduser('~/SeismicTools/E3D/')
        self.out = os.path.expanduser('~/SeismicTools/E3D/Results/')


class Region:
    def __init__(self, model):
        self.r = zeros(model.number)

    def load(self, rnumber):
        fid = open('region_' + str(rnumber) + '.pkl', 'rb')
        self.r = pickle.load(fid)
        fid.close()

    def copy(self, source, target):
        target = (1 - self.r) * target + self.r * source
        return target

    def scale(self, target, mn, sd):
        target = (1 - self.r) * target + self.r * (sd * target + 1) * mn
        return target


class Source:
    def __init__(self):
        self.type = 5
        self.amp = 1e20
        self.freq = 10.0
        self.off = 0.2
        self.loc = [0.5, 0.5, 0.0]
        self.wav = 1
        self.F = [0.0, 0.0, 1.0]
        self.M = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        self.orient = [56.0, 41.0, 106.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0]


class Traces:
    def __init__(self):
        self.dir = 'z'
        self.loc = [0.5, 0.5, 0.0]
        self.N = 200
        self.space = 0.005
        self.corr = 1


#--------------------------------------------------------------------
#				Output/Input Files
#--------------------------------------------------------------------
# Model files (velocity, density, attenuation)
class Mfile:
    def __init__(self, model):
        self.v = zeros(model.number)
        self.name = ''

    def read(self, model, target):
        ft = {'pvel': 'P-wave Velocity', 'svel': 'S-wave Velocity', 'rden': 'Density', 'patn': 'P-wave Attenuation',
              'satn': 'S-wave Attenuation'}
        self.type = target[-7:-3]
        self.name = ft[self.type]
        nelements = model.number[0] * model.number[1] * model.number[2]
        mshape = (model.number[0], model.number[2], model.number[1])
        with open(target, 'rb') as fid:
            tmp = fromfile(fid, dtype='float32', count=nelements)
        self.v = swapaxes(reshape(tmp, mshape, order='F'), 1, 2).astype('float')

    def write(self, model, target):
        nelements = model.number[0] * model.number[1] * model.number[2]
        tmp = reshape(swapaxes(self.v, 1, 2), nelements, order='F')
        with open(target, 'wb') as fid:
            tmp.astype('float32').tofile(fid)

    def plot(self, model, output):
        Z = linspace(0, model.number[2] * model.spacing[2], model.number[2]) + model.spacing[2]
        imsize = [model.origin[0], model.size[0] + model.origin[0], model.origin[1], model.size[1] + model.origin[1]]
        fig = plt.figure(figsize=(output.hres / output.sres, output.hres / (output.sres * output.hratio)),
                         dpi=output.sres)
        vimg = plt.imshow(self.v[:, :, 0], extent=imsize, vmin=round(amin(self.v), 1) - 0.05, vmax=round(amax(self.v) + 0.05, 1),
                          cmap=cm.jet)
        vtitle = plt.title('')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.colorbar()

        def animate(ii):
            vimg.set_array(self.v[:, :, ii])
            vtitle.set_text("%s Plot (Z = %1.2fkm)" % (self.name, Z[ii]))
            return vimg, vtitle

        ani = animation.FuncAnimation(fig, animate, frames=len(Z), interval=20, blit=False, repeat=False)
        ani.save("./%s.mp4" % self.type, fps=30, codec='libx264')
        #plt.ion()
        #plt.show()		# Showing plot prevents other files from rendering
        #plt.close()


# Trace files
class Tfile:
    def __init__(self):
        self.comp = ''
        self.x = []
        self.v = []
        self.t = []

    def all(self, target, traces, source, output):
        self.read(target, traces)
        self.correct(source)
        self.output(output)

    def read(self, target, traces):
        self.comp = target[-1]
        self.x = []
        self.v = []
        self.dir = []
        self.loc = []
        self.corr = []

        with open(target, 'rb') as fid:
            # File information
            self.N = fromfile(fid, dtype='int32', count=1)
            self.timesteps = fromfile(fid, dtype='int32', count=1)
            self.dt = fromfile(fid, dtype='float32', count=1)
            self.t = linspace(0, self.timesteps * self.dt, self.timesteps)

            # Read traces
            multiplex = []
            while (1):
                multiplex.append(fromfile(fid, dtype='int32', count=1))
                if (multiplex[-1] == -1):
                    break
            ntraces = len(multiplex) - 1
            tmp = array(fromfile(fid, dtype='float32', count=self.timesteps * ntraces))
            tmp = reshape(tmp, (ntraces, self.timesteps), order='F')
            tmp2 = zeros((self.N, self.timesteps))

        # Sort traces (if missing pad with zeros)
        for ii in range(0, self.N):
            try:
                loc = multiplex.index(ii)
                tmp2[ii, :] = tmp[loc, :]
            except:
                tmp2[ii, :] = zeros((1, self.timesteps))

        # Separate traces
        off = 0
        for trace in traces:
            self.v.append(tmp2[off:off + trace.N])
            self.x.append(array(linspace(0, trace.N * trace.space, trace.N)))
            self.loc.append(trace.loc)
            self.dir.append(trace.dir.lower())
            self.corr.append(trace.corr)

    def correct(self, source):
        comp = {'x': [0, 1, 2], 'y': [1, 0, 2], 'z': [2, 0, 1]}
        for ii in range(0, len(self.v)):
            r = sqrt((self.x[ii] - source.loc[comp[self.dir[ii]][0]]) ** 2
                     + (self.loc[ii][comp[self.dir[ii]][1]] - source.loc[comp[self.dir[ii]][0]]) ** 2
                     + (self.loc[ii][comp[self.dir[ii]][2]] - source.loc[comp[self.dir[ii]][0]]) ** 2)
            if (self.corr[ii] > 0):
                if (self.corr[ii] == 2):
                    r = sqrt(r)
                for jj in range(0, size(self.v[ii], 0)):
                    self.v[ii][jj][:] = self.v[ii][jj][:] * r[jj]

    def plot(self, output):
        plt.figure(figsize=output.fsize, dpi=output.dpi)
        for ii in range(0, len(self.v)):
            imsize = [self.t[0], self.t[-1], self.x[ii][-1], self.x[ii][0]]
            lim = amax(absolute(self.v[ii])) / output.scale_sat
            plt.imshow(self.v[ii], extent=imsize, vmin=-lim, vmax=lim, cmap=cm.gray, origin='upper')
            plt.title("%s-Velocity for Trace #%i" % (self.comp.upper(), ii))
            plt.xlabel('Time (s)')
            plt.ylabel('Offset (km)')
            plt.colorbar()
            plt.savefig("Trace_%i_v%s.pdf" % (ii, self.comp))
            plt.clf()


# Movie files
class Vfile:
    def __init__(self):
        self.dir = ''
        self.x = []
        self.y = []
        self.v = []
        self.t = []

    def load(self, model, multicore, target):
        # File information
        ftype = {'.Vx': ['Vx', -3], '.Vy': ['Vy', -3], '.Vz': ['Vz', -3], 'Txx': ['Txx', -4],
                 'Tyy': ['Tyy', -4], 'Tzz': ['Tzz', -4], 'Txy': ['Txy', -4], 'Txz': ['Txz', -4],
                 'Tyz': ['Tyz', -4], '.FP': ['PP', -3], '.FS': ['SP', -3]}
        comp = {'x': [1, 2], 'y': [0, 2], 'z': [0, 1]}
        self.type = ftype[target[-3:]][0]
        off = ftype[target[-3:]][1]
        self.dir = target[0]
        self.loc = target[2:off]
        self.ngrids = multicore[comp[self.dir][0]] * multicore[comp[self.dir][1]]

        # Global Grid information
        self.fid = open(target, 'rb')
        gx = fromfile(self.fid, dtype='int32', count=1)
        gy = fromfile(self.fid, dtype='int32', count=1)
        self.timesteps = fromfile(self.fid, dtype='int32', count=1)
        self.dt = fromfile(self.fid, dtype='float32', count=1)
        self.fid.seek(8 * 4)
        f = fromfile(self.fid, dtype='int32', count=1)
        self.fid.seek(4 * 4)

        # Vectors for plotting, etc.
        self.col = round((gx - 1) / f + 1)
        self.row = round((gy - 1) / f + 1)
        self.x = linspace(0, self.col, self.col) * model.spacing[comp[self.dir][0]] * f + model.origin[
            comp[self.dir][0]]
        self.y = linspace(0, self.row, self.row) * model.spacing[comp[self.dir][1]] * f + model.origin[
            comp[self.dir][1]]
        self.t2 = 0
        self.writestep = 0

    def read(self, nframes=-1):
        if (nframes == -1):
            nframes = self.timesteps - self.t2  # Read all remaining frames
        self.v = zeros((self.col, self.row, nframes), dtype=float32)
        self.t = linspace(self.t2 * self.dt, (self.t2 + nframes) * self.dt, nframes)
        self.t2 += nframes

        # Read frames by subgrid:
        for ii in range(0, nframes):
            for jj in range(0, self.ngrids):
                sx = fromfile(self.fid, dtype='int32', count=1)
                sy = fromfile(self.fid, dtype='int32', count=1)
                sxo = fromfile(self.fid, dtype='int32', count=1)
                syo = fromfile(self.fid, dtype='int32', count=1)
                f = fromfile(self.fid, dtype='int32', count=1)
                nx = int(floor((sx - 1) / f + 1))
                ny = int(floor((sy - 1) / f + 1))
                nxo = int(floor(sxo / f))
                nyo = int(floor(syo / f))
                tmp = fromfile(self.fid, dtype='float32', count=nx * ny)
                self.v[nxo:(nxo + nx), nyo:(nyo + ny), ii] = reshape(tmp, (nx, ny), order='F')

    def plot(self, output):
        # Create adaptive scale
        scale_len = 100
        scale_fix = 250
        nframes = self.v.shape[2]
        scale = zeros((nframes, 1))
        win = ones((scale_len, 1))
        for ii in range(0, nframes):
            scale[ii] = amax(absolute(self.v[:, :, ii]))
        scale = convolve(squeeze(scale), squeeze(win), mode='same') / output.scale_sat
        if (self.writestep == 0):
            scale[:scale_fix] = scale[scale_fix]

        # Initialize figure
        comp = {'x': ['Y', 'Z'], 'y': ['X', 'Z'], 'z': ['X', 'Y']}
        fig = plt.figure(figsize=(output.hres / output.sres, output.hres / (output.sres * output.hratio)),
                         dpi=output.sres)
        imsize = [self.x[0], self.x[-1], self.y[-1], self.y[0]]
        vimg = plt.imshow(self.v[:, :, 0], extent=imsize, vmin=-scale[0], vmax=scale[0], cmap=cm.RdBu)
        vtitle = plt.title('')
        plt.xlabel(comp[self.dir][0])
        plt.ylabel(comp[self.dir][1])
        plt.colorbar()

        def animate(ii):
            vimg.set_array(self.v[:, :, ii])
            vimg.set_clim(-scale[ii], scale[ii])
            vtitle.set_text("%s for %s=%s km (t=%1.2e s)" % (self.type, self.dir, self.loc, self.t[ii]))
            return vimg, vtitle

        ani = animation.FuncAnimation(fig, animate, frames=self.v.shape[2], interval=20, blit=False, repeat=False)
        if (self.writestep == 0):
            ani.save("./%s_%s_%s.mp4" % (self.dir, self.loc, self.type), fps=30, codec='libx264')
        else:
            ani.save("./%s_%s_%s_%i.mp4" % (self.dir, self.loc, self.type, self.writestep), fps=30,
                     extra_args=['-vcodec', 'libx264'])
        self.writestep += 1


# SAC File
class Sacfile:
    def __init__(self):
        self.hd = -12345 * ones(158)
        self.V = []
        self.dt = 1

    def create_header(self):
        self.hd[0] = self.dt
        self.hd[5] = 0
        self.hd[6] = (len(self.V) - 1) * self.dt
        self.hd[7] = 0
        self.hd[76] = 6
        self.hd[79] = len(self.V)
        self.hd[85] = 1
        self.hd[87] = 11
        self.hd[105] = 1

    def write(self, fname):
        with open(fname, 'wb') as fid:
            self.hd[:70].astype('float32').tofile(fid)
            self.hd[70:].astype('int32').tofile(fid)
            self.V.astype('float32').tofile(fid)

    def read(self, fname):
        with open(fname, 'wb') as fid:
            self.hd[:70] = fromfile(fid, dtype='float32', count=70)
            self.hd[70:] = fromfile(fid, dtype='int32', count=88)
            self.dt = self.hd[0]
            self.V = fromfile(fid, dtype='float32', count=self.hd[79])



