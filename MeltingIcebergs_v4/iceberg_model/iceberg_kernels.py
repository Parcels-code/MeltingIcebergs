import numpy as np
import parcels


#============================== General kernels ==============================#
def MinimumDistance(particles, fieldset):
    '''
    Calculate the minimum distance of the iceberg to ODP Site 696.
    '''
    
    lat_dist = np.fabs(particles.y - fieldset.ODP_lat) * (6371e3 * (np.pi/180.))   # vertical distance [m]
    lon_dist = np.fabs(particles.x - fieldset.ODP_lon) * ((6371e3 * np.cos(
        ((particles.y + fieldset.ODP_lat)/2.)*(np.pi/180.))) * (np.pi/180.)) # horizontal distance [m]
    
    dist = np.sqrt(lat_dist**2 + lon_dist**2)                              # total distance [m]

    particles.distance = np.minimum(dist, particles.prev_dist)
    particles.prev_dist = particles.distance 


def SetInitialPropertiesC1(particles, fieldset):
    '''
    Set the initial properties of the iceberg using:
        W = L/1.5
        M = L * W * T * rho_ice
        D = T * (rho_ice/rho_ocean)
    for size class C1.
    '''

    ptcls = particles[particles.check < 0.]
    ### Rackow (2017) sets the minimal iceberg volume to 1000m3 (10x10x10)
    ptcls.L = 17.                             # length [m]
    ptcls.W = ptcls.L/1.5                  # width [m]
    ptcls.T = 12.2                            # thickness [m]
        
    ptcls.M = ptcls.L * ptcls.W * ptcls.T * fieldset.rho_i # mass [kg]
    
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # draft [m]

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T
    
    ptcls.check = 1.
    
    particles.prev_check = particles.check


def SetInitialPropertiesC2(particles, fieldset):
    '''
    Set the initial properties of the iceberg using:
        W = L/1.5
        M = L * W * T * rho_ice
        D = T * (rho_ice/rho_ocean)
    for size class C2.
    '''
    

    ptcls = particles[particles.check < 0.]
    ptcls.L = 100.                            # length [m]
    ptcls.W = ptcls.L/1.5                  # width [m]
    ptcls.T = 20.                             # thickness [m]
    
    ptcls.M = ptcls.L * ptcls.W * ptcls.T * fieldset.rho_i # mass [kg]
    
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # draft [m]

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T
    
    ptcls.check = 1.
    
    particles.prev_check = particles.check
    

def SetInitialPropertiesC3(particles, fieldset):
    '''
    Set the initial properties of the iceberg using:
        W = L/1.5
        M = L * W * T * rho_ice
        D = T * (rho_ice/rho_ocean)
    for size class C3.
    '''
    
    ptcls = particles[particles.check < 0.]
    ptcls.L = 1000.                           # length [m]
    ptcls.W = ptcls.L/1.5                  # width [m]
    ptcls.T = 200.                            # thickness [m]
    
    ptcls.M = ptcls.L * ptcls.W * ptcls.T * fieldset.rho_i # mass [kg]
    
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # draft [m]

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T
    
    ptcls.check = 1.
    
    particles.prev_check = particles.check


def SetInitialPropertiesC4(particles, fieldset):
    '''
    Set the initial properties of the iceberg using:
        W = L/1.5
        M = L * W * T * rho_ice
        D = T * (rho_ice/rho_ocean)
    for size class C4.
    '''
    
    ptcls = particles[particles.check < 0.]
    ptcls.L = 10000.                          # length [m]
    ptcls.W = ptcls.L/1.5                      # width [m]
    ptcls.T = 500.                            # thickness [m]
    
    ptcls.M = ptcls.L * ptcls.W * ptcls.T * fieldset.rho_i # mass [kg]
    
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # draft [m]

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T
    
    ptcls.check = 1.
    
    particles.prev_check = particles.check



def SetInitialPropertiesC5(particles, fieldset):
    '''
    Set the initial properties of the iceberg using:
        W = L/1.5
        M = L * W * T * rho_ice
        D = T * (rho_ice/rho_ocean)
    for size class C5.
    '''
    
    ptcls = particles[particles.check < 0.]
    ptcls.L = 100000.                         # length [m]
    ptcls.W = ptcls.L/1.5                  # width [m]
    ptcls.T = 500.                            # thickness [m]
    
    ptcls.M = ptcls.L * ptcls.W * ptcls.T * fieldset.rho_i # mass [kg]
    
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # draft [m]

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T
    
    ptcls.check = 1.

    particles.prev_check = particles.check


def SampleRegion(particles, fieldset):
    '''
    At the iceberg's location, sample the region (see Carter et al., 2017)
    '''
    
    particles.reg = fieldset.R[particles.t+(particles.dt/2.), 0., particles.y, particles.x]

def NewProperties(particles, fieldset):
    '''
    Calculates the new properties of the iceberg from the melt terms.
    '''
    ptcls = particles[particles.check > 0.]
    # Calculate old thickness of iceberg draft
    draft = ptcls.prev_T * (fieldset.rho_i/fieldset.rho_o)

    # Calculate working areas for ...
    Ab = ptcls.prev_L * ptcls.prev_W                          # ... basal melt [m3]
    Av = 2. * draft * (ptcls.prev_L + ptcls.prev_W)           # ... buoyant convection on all sides below SL [m3]
    Ae = ptcls.prev_T * (ptcls.prev_L + ptcls.prev_W)      # ... wave erosion on two sides [m3]

    # Volume changes
    dV = (ptcls.prev_Mbr*Ab + ptcls.prev_Mvr*Av + ptcls.prev_Mer*Ae) * ptcls.dt   # total volume loss [m3]
    Vol = (ptcls.prev_L * ptcls.prev_W * ptcls.prev_T) - dV                          # new volume [m3]

    ptcls_del = ptcls[Vol < 0.]
    ptcls_del.state = parcels.StatusCode.Delete

    # New dimensions
    ptcls.T = ptcls.prev_T - ptcls.prev_Mbr*ptcls.dt    # calculate new thickness directly [m]
    A = Vol/ptcls.T                                              # horizontal area iceberg [m2]
    ptcls.W = np.sqrt(A/1.5)                                   # new width follows from ratio L = 1.5W [m]
    ptcls.L = 1.5 * ptcls.W                                   # new length follows from width as L = 1.5W [m]
    ptcls.z = ptcls.T * (fieldset.rho_i/fieldset.rho_o)   # new draft [m]

    #inds = ptcls.L >=0, ptcls.W >= 0, ptcls.T >=0
    inds = (ptcls.L >= 0) & (ptcls.W >= 0) & (ptcls.T >= 0)
    ptcls_new = ptcls[inds] # New mass
    ptcls_new.M = ptcls_new.T * ptcls_new.W * ptcls_new.L * fieldset.rho_i   # iceberg mass [kg]

    ep_crit = np.sqrt(6. * (fieldset.rho_i/fieldset.rho_o) * (1. - (fieldset.rho_i/fieldset.rho_o)))
    ep = ptcls_new.W/ptcls_new.T

    ptcls_tip = ptcls_new[ep < ep_crit] # iceberg tipping (WDE17)
    Vol_tip = ptcls_tip.L * ptcls_tip.W * ptcls_tip.T

    ptcls_tip.T = ptcls_tip.W         # calculate new thickness [m]
    A = Vol_tip/ptcls_tip.T          # keep volume and ratios correct
    ptcls_tip.W = np.sqrt(A/1.5)   # calculate new width [m]
    ptcls_tip.L = 1.5 * ptcls_tip.W   # calculate new length [m]
    ptcls_tip.z = ptcls_tip.T * (fieldset.rho_i/fieldset.rho_o)   # new draft [m]

    ptcls[~inds].state = parcels.StatusCode.Delete

    ptcls.prev_L = ptcls.L
    ptcls.prev_W = ptcls.W
    ptcls.prev_T = ptcls.T


#========================= Kernels depth-integration =========================#
def AdvectionEE(particles, fieldset):
    '''
    Advection of icebergs using Explicit Euler (aka Euler Forward) integration
    using the depth-integrated ocean velocity components.
    '''
    
    particles.dx += particles.uveloD/(1852*60*np.cos(particles.y*np.pi/180.)) * particles.dt
    particles.dy += particles.vveloD/(1852*60) * np.dt

    
def Grounding(particles, fieldset):
    '''
    Set the depth-integrated velocity to zero when an iceberg has run aground.
    '''
    ptcls = particles[particles.z >= np.fabs(particles.bath)]

    ptcls.uveloD = 0.
    ptcls.vveloD = 0.


def SampleFields(particles, fieldset):
    '''
    At the iceberg's location, sample:
     1) the surface wind field,
     2) the ocean bathymetry,
     3) the surface ocean temperature and velocity,
     4) the ocean temperature and velocity at the iceberg base, and
     5) the depth-integrated ocean temperature and velocity along the iceberg's draft.
    '''

### Wind: surface wind stress components and surface wind speed
    wind_time = particles.t + (particles.dt / 2.)
    surface_depth = np.zeros_like(particles.x)
    wind_depth = surface_depth
    taux, tauy = fieldset.XY[wind_time, wind_depth, particles.y, particles.x]  # [g/(s2 cm)]
    # tauy = fieldset.Y[wind_time, wind_depth, particles.y, particles.x]  # [g/(s2 cm)]
    vela = np.sqrt((np.sqrt(taux**2+tauy**2)*0.1)/(fieldset.rho_a*0.0015))            # [m/s]
    wind_drag = fieldset.rho_a * 0.0015 * np.maximum(np.fabs(vela), 1e-12)
    particles.uvela = (taux*0.1)/wind_drag                   # [m/s]
    particles.vvela = (tauy*0.1)/wind_drag                   # [m/s]
    
    ### Bathymetry
    particles.bath = fieldset.deptho[particles.t+(particles.dt/2.), particles.z, particles.y, particles.x] # [m] #either deptho or B for bathymetry.
    
    ## Determine the deepest point between the iceberg's base and the bathymetry
    z = np.minimum(particles.z, np.fabs(particles.bath))
    
    ### Surface (ocean): ocean temperature and velocity components at the surface
    particles.tempS = fieldset.thetao[wind_time, surface_depth, particles.y, particles.x]    # [°C]
    uvel, vvel = fieldset.UV[wind_time, surface_depth, particles.y, particles.x]       # [°/s]
    particles.uveloS = uvel*1852*60*np.cos(particles.y*np.pi/180.)                    # [m/s]
    particles.vveloS = vvel*1852*60                                                        # [m/s]
    
    ### Basal (ocean): ocean temperature and velocity components at the iceberg base
    particles.tempB = fieldset.thetao[particles.t+(particles.dt/2.), z, particles.y, particles.x]     # [°C]
    uvel, vvel = fieldset.UV[particles.t+(particles.dt/2.), z, particles.y, particles.x]        # [°/s]
    particles.uveloB = uvel*1852*60*np.cos(particles.y*np.pi/180.)                    # [m/s]
    particles.vveloB = vvel*1852*60                                                        # [m/s]
    
    ### Integrated (ocean): depth-integrated ocean temperature and velocity components along the iceberg's draft

    center_depth = fieldset.UV.grid.depth # is this .depth or should this be .z?
    face_depth = np.empty(len(center_depth) + 1)
    face_depth[1:-1] = (center_depth[:-1] + center_depth[1:]) /2
    face_depth[0] = 0.
    face_depth[-1] = center_depth[-1] + (center_depth[-1] - face_depth[-2])
    thickness = np.gradient(face_depth)

    t = np.zeros_like(particles.x)
    u = np.zeros_like(particles.x)
    v = np.zeros_like(particles.x)

# added n_layers to ensure that only the levels that contain at least one particle are visited. 
    n_layers = np.searchsorted(face_depth, np.max(particles.z), side="left")
    for di, D in enumerate(center_depth[:n_layers]):
        # NOTE this can be made faster by ignoring shallow particles
        inds = np.where(particles.z > face_depth[di])[0]
        ptcls = particles[inds]
        layer_depth = np.full_like(ptcls.x, D)
        temp = fieldset.thetao[ptcls.t+(particles.dt/2.), layer_depth, ptcls.y, ptcls.x]
        #changed fieldset.T to fieldset.thetao
        uu, uv = fieldset.UV[ptcls.t+(particles.dt/2.), layer_depth, ptcls.y, ptcls.x]
        #NOTE changed np.min to np.minimum, is this still correct?
        dz = np.minimum(ptcls.z - face_depth[di], thickness[di])
        t[inds] += temp * dz
        u[inds] += uu * dz
        v[inds] += uv * dz
    
    
    safe_depth = np.maximum(z, 1e-12)
    particles.tempD = t / safe_depth                                     # [°C]
    uvel = u / safe_depth                                                # [°/s]
    vvel = v / safe_depth                                                # [°/s]
    
    particles.uveloD = uvel*1852*60*np.cos(particles.y*np.pi/180.)   # [m/s]
    particles.vveloD = vvel*1852*60                                       # [m/s]


def BuoyantConvection(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through buoyant convection at the icebergs sides following:
        Mv = b1 * T + b2 * T^2
    with
        b1 = 7.62E-3 [m/(d °C)]
        b2 = 1.29E-3 [m/(d °C)]
        T: depth-integrated temperature [°C]
    See also Merino et al. (2016).
    '''

    mask = particles.z < np.fabs(particles.bath) # if not grounded

    # meltrate till seafloor
    particles[mask].Mvr = (7.62e-3 * particles[mask].tempD + 1.29e-3 * (particles[mask].tempD)**2)/fieldset.sec_to_day

    Mv1 = 7.62e-3 * particles[~mask].tempD + 1.29e-3 * (particles[~mask].tempD)**2
    Mvr1 = Mv1 * np.fabs(particles[~mask].bath)
    # meltrate 'below' seafloor
    Mv2 = 7.62e-3 * particles[~mask].tempB + 1.29e-3 * (particles[~mask].tempB)**2
    Mvr2 = Mv2 * (particles[~mask].z-np.fabs(particles[~mask].bath))
    # total meltrate
    Mvr = (Mvr1+Mvr2)/particles[~mask].z                                 # [m/d]
    particles[~mask].Mvr = Mvr/fieldset.sec_to_day

    particles.prev_Mvr = particles.Mvr


def BasalMelt(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through basal melt at the iceberg base following:
        Mb = C * |v_ice - v_ocean|^0.8 * (T_ocean - T_ice) / (L^0.2) 
    with
        C = 0.58 [°C^-1 m^0.4 d^-1 s^0.8]
        v_ice: iceberg velocity (depth-integrated) [m/s]
        v_ocean: ocean velocity at the iceberg base [m/s]
        T_ocean: ocean temperature at the iceberg base [°C]
        T_ice = -1.92 [°C]; freezing temperature
        L: iceberg length [m]
    See FitzMaurice & Stern (2018) and references therein.
    '''
    
    dvelabs = np.sqrt((particles.uveloD-particles.uveloB)**2 + (particles.vveloD-particles.vveloB)**2)
    
    Mbr = 0.58 * (dvelabs**0.8) * ((particles.tempB-fieldset.Ti)/(particles.L**0.2))   # [m/d]
    particles.Mbr = Mbr/fieldset.sec_to_day                                           # [m/s]
    particles.prev_Mbr = particles.Mbr


def BasalMeltAlt(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through basal melt at the iceberg base following the bulk
    equation when its length is smaller than 1E2 m and the adapted equation when larger.
    '''

    mask = particles.L <= 15000.
 
    dvelabs = np.sqrt((particles[mask].uveloD-particles[mask].uveloB)**2 + (particles[mask].vveloD-particles[mask].vveloB)**2)

    Mbr = 0.58 * (dvelabs**0.8) * ((particles[mask].tempB-fieldset.Ti)/(particles[mask].L**0.2))   # [m/d]
    particles[mask].Mbr = Mbr/fieldset.sec_to_day                                           # [m/s]

   
    f = np.fabs(2 * fieldset.Om * np.sin(particles[~mask].lat*np.pi/180.))
    u_st = np.sqrt(fieldset.cd) * np.sqrt(particles[~mask].uveloD**2 + particles[~mask].vveloD**2)
    eta_st = 1./np.sqrt(1 + fieldset.xiN*u_st/(f*fieldset.Lo*fieldset.Rc))
    h_nu = 5*fieldset.nu/u_st

    GammaT = fieldset.k_r*np.log(
        u_st*fieldset.xiN*eta_st**2/(f*h_nu)) + 1./(
        2*fieldset.xiN*eta_st) - fieldset.k_r                                                   # [-]
    GammaM = 12.5 * fieldset.Pr**(2./3.) - 6                                                    # [-]
    gamma_T3EM = (fieldset.rho_o*fieldset.cpo*np.sqrt(fieldset.cd)*(
        0.004*particles[~mask].tempS+0.02)) / (GammaT + GammaM)                                         # [W/(m2 K)]

    particles[~mask].Mbr = gamma_T3EM * (0.7*particles[~mask].tempS-1.2-fieldset.Ti) / (fieldset.rho_i * fieldset.Lf)   # [m/s]
    
    particles.prev_Mbr = particles.Mbr


def WaveErosion(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through wave erosion at the icebergs sides:
        Me = 1/12 Ss * (1+cos(pi*A_ice^3)) * (T_ocean + 2)
    with sea state:
        Ss = 3/2 (|v_atm - v_ocean|)^0.5 + 1/10 |v_atm - v_ocean|
    and
        A_ice: fractional sea-ice area [m2]; negligible in the Eocene
        T_ocean: ocean surface temperature [°C]
        v_atm: surface wind velocity [m/s]
        v_ocean: ocean surface velocity [m/s]
    '''
    
    dvelabs = np.sqrt((particles.uvela-particles.uveloS)**2 + (particles.vvela-particles.vveloS)**2)
    Ss = (3./2.) * np.sqrt(dvelabs) + (1./10.) * dvelabs
    
    Ai = 0.
    damping = 0.5 * (1 + np.cos(np.pi * Ai**3))
    
    Mer = (1./6.) * Ss * damping * (particles.tempS - - 2.)   # [m/d]
    particles.Mer = Mer/fieldset.sec_to_day                   # [m/s]
    particles.prev_Mer = particles.Mer


#============================== Kernels surface ==============================#
  
def SampleFieldsSurf(particles, fieldset):
    '''
    At the iceberg's location, sample:
     1) the surface wind field,
     2) the surface ocean temperature and velocity.
    '''
    
    ### Wind: surface wind stress components and surface wind speed
    wind_time = particles.t + (particles.dt / 2.)
    surface_depth = np.zeros_like(particles.x)
    taux, tauy = fieldset.XY[wind_time, surface_depth, particles.y, particles.x]  # [g/(s2 cm)]
    # tauy = fieldset.Y[wind_time, surface_depth, particles.y, particles.x]  # [g/(s2 cm)]
    vela = np.sqrt((np.sqrt(taux**2+tauy**2)*0.1)/(fieldset.rho_a*0.0015))            # [m/s]
    wind_drag = fieldset.rho_a * 0.0015 * np.maximum(np.fabs(vela), 1e-12)
    particles.uvela = (taux*0.1)/wind_drag                   # [m/s]
    particles.vvela = (tauy*0.1)/wind_drag                   # [m/s]
    
    ### Surface (ocean): ocean temperature and velocity components at the surface
    particles.temp = fieldset.thetao[wind_time, surface_depth, particles.y, particles.x]     # [°C]
    uvel, vvel = fieldset.UV[wind_time, surface_depth, particles.y, particles.x]       # [°/s]
    particles.uvelo = uvel*1852*60*np.cos(particles.y*np.pi/180.)                     # [m/s]
    particles.vvelo = vvel*1852*60     

def AdvectionEESurf(particles, fieldset):
    '''
    Advection of icebergs using Explicit Euler (aka Euler Forward) integration
    using the surface ocean velocity components.
    '''
    
    particles.dx += particles.uvelo/(1852*60*np.cos(particles.dy*np.pi/180.)) * particles.dt
    particles.dy += particles.vvelo/(1852*60) * particles.dt


def BuoyantConvectionSurf(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through buoyant convection at the icebergs sides following:
        Mv = b1 * T + b2 * T^2
    with
        b1 = 7.62E-3 [m/(d °C)]
        b2 = 1.29E-3 [m/(d °C)]
        T: ocean temperature [°C]
    See also Merino et al. (2016).
    '''
    
    Mvr = 7.62e-3 * particles.temp + 1.29e-3 * (particles.temp)**2   # [m/d]
    
    particles.Mvr = Mvr/fieldset.sec_to_day                         # [m/s]
    particles.prev_Mvr = particles.Mvr


def BasalMeltSurf(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through basal melt at the iceberg base following:
        Mb = C * |v_ice - v_ocean|^0.8 * (T_ocean - T_ice) / (L^0.2) 
    with
        C = 0.58 [°C^-1 m^0.4 d^-1 s^0.8]
        v_ice: iceberg velocity [m/s]
        v_ocean: ocean velocity [m/s]
        T_ocean: ocean temperature [°C]
        T_ice = -1.92 [°C]; freezing temperature
        L: iceberg length [m]
    See FitzMaurice & Stern (2018) and references therein.
    '''
    
    # Let's sample the second ocean layer so we can calculate some basal melt
    # Nnormally, vIB =/= vS. Now, let's calculate uB as mean of u0 and u1.
    basal_depth = np.zeros_like(particles.x) + 10.1
    uvel, vvel = fieldset.UV[particles.t+(particles.dt/2.), basal_depth, particles.y, particles.x, particles]     # [°/s]
    uvel = (uvel*1852*60*np.cos(particles.y*np.pi/180.)+particles.uvelo)/2.           # [m/s]
    vvel = (vvel*1852*60+particles.vvelo)/2.                                               # [m/s]
    
    dvelabs = np.sqrt((uvel-particles.uvelo)**2 + (vvel-particles.vvelo)**2) # actually 0 as IB moves with surface flow
    
    Mbr = 0.58 * (dvelabs**0.8) * ((particles.temp-fieldset.Ti)/(particles.L**0.2))   # [m/d]
    particles.Mbr = Mbr/fieldset.sec_to_day                                          # [m/s]
    particles.prev_Mbr = particles.Mbr


def WaveErosionSurf(particles, fieldset):
    '''
    Calculates the mass loss rate [m/s] through wave erosion at the icebergs sides:
        Me = 1/12 Ss * (1+cos(pi*A_ice^3)) * (T_ocean + 2)
    with sea state:
        Ss = 3/2 (|v_atm - v_ocean|)^0.5 + 1/10 |v_atm - v_ocean|
    and
        A_ice: fractional sea-ice area [m2]; negligible in the Eocene
        T_ocean: ocean surface temperature [°C]
        v_atm: surface wind velocity [m/s]
        v_ocean: ocean surface velocity [m/s]
    '''
    
    dvelabs = np.sqrt((particles.uvela-particles.uvelo)**2 + (particles.vvela-particles.vvelo)**2)
    Ss = (3./2.) * np.sqrt(dvelabs) + (1./10.) * dvelabs
    
    Ai = 0.
    damping = 0.5 * (1 + np.cos(np.pi * Ai**3))
    
    Mer = (1./6.) * Ss * damping * (particles.temp - - 2.)    # [m/d]
    particles.Mer = Mer/fieldset.sec_to_day                   # [m/s]
    particles.prev_Mer = particles.Mer