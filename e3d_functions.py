from e3d_classes import *


def e3d_fractal(model, dist):
    # Setup a random-normal fractal model
    if dist[0] == -0.5 * model.dims:
        fractal = random.normal(0, 1, model.number)
    else:
        # Build the spectral filter:
        f = 1 / (2 * model.spacing[1])
        X, Y, Z = mgrid[0:model.number[0], 0:model.number[1], 0:model.number[2]]
        X = array(2 * f * X / model.number[0] - f)
        Y = array(2 * f * Y / model.number[1] - f)
        Z = array(2 * f * Z / model.number[2] - f)
        K = ((dist[1] * X) ** 2 + (dist[2] * Y) ** 2 + (dist[3] * Z) ** 2)
        del X, Y, Z

        #Fix to avoid divide by zero error
        mid = (array(model.number) * 0.5).astype('int')
        K[tuple(mid)] = K[tuple(mid + 1)]
        F = K ** (-0.25 * model.dims - 0.5 * dist[0])

        # Generate a random matrix and do an fft
        V = random.normal(0, 1, model.number)
        fV = fft.fftn(V)
        del V

        # Apply the spectral filter and do an ifft
        V = real(fft.ifftn(fV * fft.fftshift(F)))
        del fV, K

        # Make sure the distribution is normalized
        fractal = (V - V.mean()) / V.std()

    return (fractal)


def e3d_locate(model, rtype, geometry, rnumber):
    # Create the material grids
    region = array(zeros(model.number), dtype=bool)
    X, Y, Z = mgrid[0:model.number[0], 0:model.number[1], 0:model.number[2]]
    X = array(X * model.spacing[0] + model.origin[0])
    Y = array(Y * model.spacing[1] + model.origin[1])
    Z = array(Z * model.spacing[2] + model.origin[2])

    # Switch for region type
    if (rtype == 1):
        print 'Region #' + str(rnumber) + ' - Rectangle'
        region = (X >= geometry[0]) & (X <= geometry[1]) & (Y >= geometry[2]) & (Y <= geometry[3]) & (
            Z >= geometry[4]) & (Z <= geometry[5])

    elif (rtype == 2):
        print 'Region #' + str(rnumber) + ' - Sphere'
        X = X - geometry[0]
        Y = Y - geometry[1]
        Z = Z - geometry[2]
        test = X ** 2 + Y ** 2 + Z ** 2
        region = (test <= geometry[3] ** 2)

    elif (rtype == 3):
        print 'Region #' + str(rnumber) + ' - Cylinder'
        dx = geometry[3] - geometry[0]
        dy = geometry[4] - geometry[1]
        dz = geometry[5] - geometry[2]
        thz = arctan2(dy, dx)
        thy = arctan2(dz, sqrt(dx ** 2 + dy ** 2))
        X, Y, Z = e3d_transform(X - geometry[0], Y - geometry[1], Z - geometry[2], thz, thy, 0, 0, 0)
        test = sqrt(
            (geometry[3] - geometry[0]) ** 2 + (geometry[4] - geometry[1]) ** 2 + (geometry[5] - geometry[2]) ** 2)
        region = ((Y ** 2 + Z ** 2) <= (geometry[6] ** 2)) & (X >= 0) & (X <= test)

    elif (rtype == 4):
        print 'Region #' + str(rnumber) + ' - Polynomial'

        X = polyval(geometry[0, :], X)
        Y = polyval(geometry[1, :], Y)
        test = X * Y
        region = (Z <= test)

    elif (rtype == 5):
        print 'Region #' + str(rnumber) + ' - Plane'
        thz = geometry[3] * pi / 180 - pi / 2
        thy = geometry[4] * pi / 180
        X, Y, Z = e3d_transform(X - geometry[0], Y - geometry[1], Z - geometry[2], thz, thy, 0, 0, 0)
        test = geometry[6] * sin(2 * pi * absolute(X) / geometry[5])
        region = (Z + test >= 0) & (Z + test <= geometry[8])

    elif (rtype == 6):
        if isinstance(rnumber, (int, long)):
            print 'Region #' + str(rnumber) + ' - Open Box'
        region[:geometry[0], :, :] = 1
        region[-1 * geometry[0]:, :, :] = 1
        region[:, :geometry[0], :] = 1
        region[:, -1 * geometry[0]:, :] = 1
        region[:, :, -1 * geometry[0]:] = 1

    elif (rtype == 7):
        print 'Region #' + str(rnumber) + ' - Entire Domain'
        region[:] = 1

    elif (rtype == 8):
        print 'Region #' + str(rnumber) + ' - Interpolation from File'
        region[:] = 1

    # elif (rtype == 8):
    #     print 'Region #' + str(rnumber) + ' - Piecewise Surface'
    #     segments = int((len(geometry) - 4) / 2)
    #     thz = geometry[3] * pi / 180
    #     thy = 0
    #     X, Y, Z = e3d_transform(X - geometry[0], Y - geometry[1], Z - geometry[2], thz, thy, 0, 0, 0)
    #
    #     for ii in range(0, segments):
    #         xstart = geometry[2 * ii + 4]
    #         zstart = geometry[2 * ii + 5]
    #         xend = geometry[2 * ii + 6]
    #         zend = geometry[2 * ii + 7]
    #         slope = (zend - zstart) / (xend - xstart)
    #         test = Z - slope * (X - xstart) - zstart
    #         region = region + ((X >= xstart) & (X <= xend) & (test <= 0))
    #
    # elif (rtype == 9):
    #     print 'Region #' + str(rnumber) + ' - Tunnel'
    #     segments = int((len(geometry) - 5) / 3)
    #     width = geometry[0]
    #     height = geometry[1]
    #     X = X - geometry[2]
    #     Y = Y - geometry[3]
    #     Z = Z - geometry[4]
    #     thz_old = 0
    #     thy_old = 0
    #
    #     for ii in range(0, segments):
    #         thz = geometry[5 + ii * 3] * pi / 180
    #         thy = geometry[6 + ii * 3] * pi / 180
    #         L = geometry[7 + ii * 3]
    #         X, Y, Z = e3d_transform(X, Y, Z, thz, thy, thz_old, thy_old, 1)
    #
    #         #Determine distance required to close tunnel
    #         if (ii > 0):
    #             thz_old = geometry[5 + (ii - 1) * 3] * pi / 180
    #             thy_old = geometry[6 + (ii - 1) * 3] * pi / 180
    #             Lback1 = min((width * tan(0.5 * (thz - thz_old))) ** 2, width ** 2)
    #             Lback2 = min((height * tan(0.5 * (thy - thy_old))) ** 2, height ** 2)
    #             Lback = -0.5 * sqrt(Lback1 ** 2 + Lback2 ** 2)
    #         else:
    #             Lback = 0
    #
    #         if (ii < segments - 1):
    #             thz_new = geometry[5 + (ii + 1) * 3] * pi / 180
    #             thy_new = geometry[6 + (ii + 1) * 3] * pi / 180
    #             Lfor1 = min((width * tan(0.5 * (thz_new - thz))) ** 2, width ** 2)
    #             Lfor2 = min((height * tan(0.5 * (thy_new - thy))) ** 2, height ** 2)
    #             Lfor = -0.5 * sqrt(Lfor1 ** 2 + Lfor2 ** 2)
    #         else:
    #             Lfor = 0
    #
    #         # Logicals
    #         region = region + (
    #             (X >= Lback) & (X <= L + Lfor) & (absolute(Y) <= 0.5 * width) & (absolute(Z) <= 0.5 * height))
    #         X = X - L
    #         thz_old = thz
    #         thy_old = thy

    fid = open('region_' + str(rnumber) + '.pkl', 'wb')
    pickle.dump(region, fid, 2)
    fid.close()


def e3d_transform(x, y, z, thz, thy, thz_old, thy_old, back):
    R1 = array([[cos(thz), sin(thz), 0], [-1 * sin(thz), cos(thz), 0], [0, 0, 1]])
    R2 = array([[cos(thy), 0, sin(thy)], [0, 1, 0], [-1 * sin(thy), 0, cos(thy)]])
    R = dot(R2, R1)

    if (back == 1):
        R1 = array([[cos(thz_old), sin(thz_old), 0], [-1 * sin(thz_old), cos(thz_old), 0], [0, 0, 1]])
        R2 = array([[cos(thy_old), 0, sin(thy_old)], [0, 1, 0], [-1 * sin(thy_old), 0, cos(thy_old)]])
        R_back = linalg.inv(R2 * R1)
        R = dot(R, R_back)

    x2 = R[0, 0] * x + R[0, 1] * y + R[0, 2] * z
    y2 = R[1, 0] * x + R[1, 1] * y + R[1, 2] * z
    z2 = R[2, 0] * x + R[2, 1] * y + R[2, 2] * z
    return (x2, y2, z2)


def e3d_gmail(toaddr, subject, body):
    fromaddr = 'cssherman.matlab@gmail.com'
    passwd = '1adam123'
    msg = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (fromaddr, toaddr, subject, body)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(fromaddr, passwd)
    server.sendmail(fromaddr, toaddr, msg)


def e3d_wavelet(model, source):

    #from e3d_classes import Sacfile
    # Setup
    wc = source.freq * 2 * pi
    gd = 0.05
    slength = 200

    # Find length and std of gaussian window
    time_off = source.off / (2 * model.dt)
    time_off = min(model.timesteps, max(0, round(time_off)))
    time_buf = 2 * model.timesteps + 4 * time_off
    sd = sqrt(-2 * log(gd) / wc ** 2) / (2 * model.dt)

    # Generate and trim the window
    W = signal.gaussian(time_buf, sd)
    if (source.type == 1):
        W = diff(W)
    W2 = W[int(0.5 * time_buf - time_off):int(0.5 * time_buf - time_off + model.timesteps)]
    W2[:slength] = W2[:slength] * linspace(0, 1, slength)

    # Create the sac file
    sac = Sacfile()
    sac.V = W2 / max(abs(W2))
    sac.dt = model.dt
    sac.create_header()
    sac.write('./wav.sac')