import parcels
from operator import attrgetter
import numpy as np


Iceberg_FW = parcels.Particle.add_variable(
    [
    # Ocean - at surface
        parcels.Variable('tempS', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloS', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloS', initial=0, to_write=False), # v-velocity [m/s]

        # Wind - at surface
        parcels.Variable('uvela', initial=0, to_write=False),   # u-velocity [m/s]
        parcels.Variable('vvela', initial=0, to_write=False),   # v-velocity [m/s]

        # Ocean - at iceberg base
        parcels.Variable('tempB', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloB', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloB', initial=0, to_write=False), # v-velocity [m/s]
        
        # Ocean - depth-integrated along iceberg draft
        parcels.Variable('tempD', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloD', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloD', initial=0, to_write=False), # v-velocity [m/s]
        
        # Iceberg properties
        parcels.Variable('L', initial=0, to_write=False),          # Iceberg length [m]
        parcels.Variable('W', initial=0, to_write=False),          # Iceberg width [m]
        parcels.Variable('T', initial=0, to_write=False),          # Iceberg thickness [m]
        parcels.Variable('M', initial=0),                          # Iceberg mass [kg]
        
        parcels.Variable('prev_L', to_write=False, initial=attrgetter('L')),
        parcels.Variable('prev_W', to_write=False, initial=attrgetter('W')),
        parcels.Variable('prev_T', to_write=False, initial=attrgetter('T')),
        
        # Melt terms
        parcels.Variable('Mvr', initial=0),                      # buoyant convection [m/s]
        parcels.Variable('Mbr', initial=0),                      # basal melt [m/s]
        parcels.Variable('Mer', initial=0),                      # wave erosion [m/s]
        
        parcels.Variable('prev_Mvr', to_write=False, initial=attrgetter('Mvr')),
        parcels.Variable('prev_Mbr', to_write=False, initial=attrgetter('Mbr')),
        parcels.Variable('prev_Mer', to_write=False, initial=attrgetter('Mer')),
        
        # Others
        parcels.Variable('bath', initial=0, to_write=False),    # bathymetry [m]
        
        parcels.Variable('distance', initial=1000000),      # distance to ODP Site U1475  
        parcels.Variable('prev_dist', to_write=False, initial=attrgetter('distance')),
        
        parcels.Variable('check', to_write=False, initial=-1), # check iceberg existance
        parcels.Variable('prev_check', to_write=False, initial=attrgetter('check')),
    ]
)    
    
### Backward
Iceberg_BW = parcels.Particle.add_variable(
    [
    # Ocean - at surface
        parcels.Variable('tempS', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloS', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloS', initial=0, to_write=False), # v-velocity [m/s]

        # Wind - at surface
        parcels.Variable('uvela', initial=0, to_write=False),   # u-velocity [m/s]
        parcels.Variable('vvela', initial=0, to_write=False),   # v-velocity [m/s]

        # Ocean - at iceberg base
        parcels.Variable('tempB', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloB', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloB', initial=0, to_write=False), # v-velocity [m/s]
        
        # Ocean - depth-integrated along iceberg draft
        parcels.Variable('tempD', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloD', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloD', initial=0, to_write=False), # v-velocity [m/s]
        
        # Iceberg properties
        parcels.Variable('L', initial=0, to_write=False),          # Iceberg length [m]
        parcels.Variable('W', initial=0, to_write=False),          # Iceberg width [m]
        parcels.Variable('T', initial=0, to_write=False),          # Iceberg thickness [m]
        parcels.Variable('M', initial=0),                          # Iceberg mass [kg]
        
        parcels.Variable('prev_L', to_write=False, initial=attrgetter('L')),
        parcels.Variable('prev_W', to_write=False, initial=attrgetter('W')),
        parcels.Variable('prev_T', to_write=False, initial=attrgetter('T')),
        
        # Melt terms
        parcels.Variable('Mvr', initial=0),                      # buoyant convection [m/s]
        parcels.Variable('Mbr', initial=0),                      # basal melt [m/s]
        parcels.Variable('Mer', initial=0),                      # wave erosion [m/s]
        
        parcels.Variable('prev_Mvr', to_write=False, initial=attrgetter('Mvr')),
        parcels.Variable('prev_Mbr', to_write=False, initial=attrgetter('Mbr')),
        parcels.Variable('prev_Mer', to_write=False, initial=attrgetter('Mer')),
        
        # Others
        parcels.Variable('bath', initial=0, to_write=False),    # bathymetry [m]
        parcels.Variable('reg', initial=0, dtype=np.int32),      # region Carter
    
        parcels.Variable('check', to_write=False, initial=-1), # check iceberg existance
        parcels.Variable('prev_check', to_write=False, initial=attrgetter('check')),
    ]
) 

### Forward daily
Iceberg_FW_day = parcels.Particle.add_variable(
    [
    # Ocean - at surface
        parcels.Variable('tempS', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloS', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloS', initial=0, to_write=False), # v-velocity [m/s]

        # Wind - at surface
        parcels.Variable('uvela', initial=0, to_write=False),   # u-velocity [m/s]
        parcels.Variable('vvela', initial=0, to_write=False),   # v-velocity [m/s]

        # Ocean - at iceberg base
        parcels.Variable('tempB', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloB', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloB', initial=0, to_write=False), # v-velocity [m/s]
        
        # Ocean - depth-integrated along iceberg draft
        parcels.Variable('tempD', initial=0, to_write=False),   # temperature [°C]
        parcels.Variable('uveloD', initial=0, to_write=False), # u-velocity [m/s]
        parcels.Variable('vveloD', initial=0, to_write=False), # v-velocity [m/s]
        
        # Iceberg properties
        parcels.Variable('L', initial=0, to_write=False),          # Iceberg length [m]
        parcels.Variable('W', initial=0, to_write=False),          # Iceberg width [m]
        parcels.Variable('T', initial=0, to_write=False),          # Iceberg thickness [m]
        parcels.Variable('M', initial=0),                          # Iceberg mass [kg]
        
        parcels.Variable('prev_L', to_write=False, initial=attrgetter('L')),
        parcels.Variable('prev_W', to_write=False, initial=attrgetter('W')),
        parcels.Variable('prev_T', to_write=False, initial=attrgetter('T')),
        
        # Melt terms
        parcels.Variable('Mvr', initial=0),                      # buoyant convection [m/s]
        parcels.Variable('Mbr', initial=0),                      # basal melt [m/s]
        parcels.Variable('Mer', initial=0),                      # wave erosion [m/s]
        
        parcels.Variable('prev_Mvr', to_write=False, initial=attrgetter('Mvr')),
        parcels.Variable('prev_Mbr', to_write=False, initial=attrgetter('Mbr')),
        parcels.Variable('prev_Mer', to_write=False, initial=attrgetter('Mer')),
        
        # Others
        parcels.Variable('bath', initial=0, to_write=False),    # bathymetry [m]
        
        parcels.Variable('distance', initial=1000000),      # distance to ODP Site U1475  
        parcels.Variable('prev_dist', to_write=False, initial=attrgetter('distance')),
        
        parcels.Variable('check', to_write=False, initial=-1), # check iceberg existance
        parcels.Variable('prev_check', to_write=False, initial=attrgetter('check')),
    ]
)

### Surface
Iceberg_FW_Surf = parcels.Particle.add_variable(
    [
    # Ocean - at surface
        parcels.Variable('temp', initial=0, to_write=False),    # Surface-kernel temperature [°C]
        parcels.Variable('uvelo', initial=0, to_write=False),   # Surface-kernel u-velocity [m/s]
        parcels.Variable('vvelo', initial=0, to_write=False),   # Surface-kernel v-velocity [m/s]
    
        # Wind - at surface
        parcels.Variable('uvela', initial=0, to_write=False),   # u-velocity [m/s]
        parcels.Variable('vvela', initial=0, to_write=False),   # v-velocity [m/s]

        # Iceberg properties
        parcels.Variable('L', initial=0, to_write=False),          # Iceberg length [m]
        parcels.Variable('W', initial=0, to_write=False),          # Iceberg width [m]
        parcels.Variable('T', initial=0, to_write=False),          # Iceberg thickness [m]
        parcels.Variable('M', initial=0),                          # Iceberg mass [kg]
        
        parcels.Variable('prev_L', to_write=False, initial=attrgetter('L')),
        parcels.Variable('prev_W', to_write=False, initial=attrgetter('W')),
        parcels.Variable('prev_T', to_write=False, initial=attrgetter('T')),
        
        # Melt terms
        parcels.Variable('Mvr', initial=0),                      # buoyant convection [m/s]
        parcels.Variable('Mbr', initial=0),                      # basal melt [m/s]
        parcels.Variable('Mer', initial=0),                      # wave erosion [m/s]
        
        parcels.Variable('prev_Mvr', to_write=False, initial=attrgetter('Mvr')),
        parcels.Variable('prev_Mbr', to_write=False, initial=attrgetter('Mbr')),
        parcels.Variable('prev_Mer', to_write=False, initial=attrgetter('Mer')),
        
        # Others
        parcels.Variable('bath', initial=0, to_write=False),    # bathymetry [m]
        
        parcels.Variable('distance', initial=1000000),      # distance to ODP Site U1475  
        parcels.Variable('prev_dist', to_write=False, initial=attrgetter('distance')),
        
        parcels.Variable('check', to_write=False, initial=-1), # check iceberg existance
        parcels.Variable('prev_check', to_write=False, initial=attrgetter('check')),
    ]
)    

### Backward
Iceberg_BW_Surf = parcels.Particle.add_variable(
    [
    # Ocean - at surface
        parcels.Variable('temp', initial=0, to_write=False),    # Surface-kernel temperature [°C]
        parcels.Variable('uvelo', initial=0, to_write=False),   # Surface-kernel u-velocity [m/s]
        parcels.Variable('vvelo', initial=0, to_write=False),   # Surface-kernel v-velocity [m/s]
    
        # Wind - at surface
        parcels.Variable('uvela', initial=0, to_write=False),   # u-velocity [m/s]
        parcels.Variable('vvela', initial=0, to_write=False),   # v-velocity [m/s]

        # Iceberg properties
        parcels.Variable('L', initial=0, to_write=False),          # Iceberg length [m]
        parcels.Variable('W', initial=0, to_write=False),          # Iceberg width [m]
        parcels.Variable('T', initial=0, to_write=False),          # Iceberg thickness [m]
        parcels.Variable('M', initial=0),                          # Iceberg mass [kg]
        
        parcels.Variable('prev_L', to_write=False, initial=attrgetter('L')),
        parcels.Variable('prev_W', to_write=False, initial=attrgetter('W')),
        parcels.Variable('prev_T', to_write=False, initial=attrgetter('T')),
        
        # Melt terms
        parcels.Variable('Mvr', initial=0),                      # buoyant convection [m/s]
        parcels.Variable('Mbr', initial=0),                      # basal melt [m/s]
        parcels.Variable('Mer', initial=0),                      # wave erosion [m/s]
        
        parcels.Variable('prev_Mvr', to_write=False, initial=attrgetter('Mvr')),
        parcels.Variable('prev_Mbr', to_write=False, initial=attrgetter('Mbr')),
        parcels.Variable('prev_Mer', to_write=False, initial=attrgetter('Mer')),
        
        # Others
        parcels.Variable('bath', initial=0, to_write=False),    # bathymetry [m]
        parcels.Variable('reg', initial=0, dtype=np.int32),      # region Carter

        parcels.Variable('check', to_write=False, initial=-1), # check iceberg existance
        parcels.Variable('prev_check', to_write=False, initial=attrgetter('check')),
    ]
) 