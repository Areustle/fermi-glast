/**
 * @file TF1Map.h
 * @brief A source class that uses ROOT TF1 object to define a spectrum symbolically
 * id est with a formula. Besides, the spatial localization of the source is based on a FITS map image, encapsulated in 
 * the MapSource base class. 
 * The TF1Map class is instantiated based on the information parsed from
 * the params string, passed to the object vi the constructor. Here is an example of
 * such params string :
 * params="flux=17.,tf1name=FT1Map_TEST,formula=-0.0001*(100.-x)*(1100.-x),fitsFile=$(FLUXROOT)/sources/gas_gal.fits,emin=100.,emax=1100,tf1precision=100,gamma=2,lonMin=-180,lonMax=180,latMin=-90,latMax=90"/>
 * tf1name is needed to let the user make sure that the ROOT object has a unique name identifier in ROOT internal memory.
 * tf1precision defines the granularity with which TF1 will approximate the formula.
 * @author Johann Cohen-Tanugi
 *
 * $Header: /nfs/slac/g/glast/ground/cvs/ScienceTools-scons/celestialSources/genericSources/genericSources/TF1Map.h,v 1.4 2006/05/30 17:53:42 cohen Exp $
 */
 

#ifndef TF1MAP_H
#define TF1MAP_H

#include "TF1.h"
#include "genericSources/MapSource.h"
#include<map>

class TF1Map : public MapSource
{
 public:
  TF1Map(const std::string& /*params*/);
  ~TF1Map() {;}//{delete p_tf1;}
  

  ///The TF1 object manages the random draw, so that the float argument, normally a
  /// random draw from a [0,1[ distribution, is unused.
  float operator()(float )const 
    {
      return p_tf1.GetRandom();
    }

  std::string title() const 
    {
      return "TF1Map";
    }

  const char * particleName() const    {      return m_particle_name.c_str();    }

  
  ///Return an energy sampled from the TF1 distribution. 
  double energy(double time)    {      return (*this)(time);    }


  /// Overload of flux method to ensure proper call to m_flux
  /// @return Total flux (photons/m^2).
  /// @param time Simulation time in seconds.
  virtual double flux(double ) const  { return m_flux; } 


 private:
  ///pointer to the TF1 object that reads the symbolic formula and does all the job
  mutable TF1  p_tf1;
  std::map<std::string,std::string> m_parmap;
};

#endif
