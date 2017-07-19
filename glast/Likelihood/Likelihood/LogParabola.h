/** 
 * @file LogParabola.h
 * @brief Declaration for the LogParabola class
 * @author J. Chiang
 *
 * $Header: /nfs/slac/g/glast/ground/cvs/ScienceTools-scons/Likelihood/Likelihood/LogParabola.h,v 1.4 2015/03/21 05:38:02 jchiang Exp $
 */

#ifndef Likelihood_LogParabola_h
#define Likelihood_LogParabola_h

#include "optimizers/Function.h"
#include "optimizers/Arg.h"

namespace Likelihood {

/** 
 * @class LogParabola
 *
 * @brief A log-parabolic function for modeling Blazar SED components.
 *
 */
    
class LogParabola : public optimizers::Function {

public:

   /// @brief The log-parabolic form is given by
   /// \f$K (E/E_1)^{-(\alpha + \beta*\log(E/E_1))}\f$
   /// @param norm \f$k\f$ in the formula
   /// @param alpha 
   /// @param beta 
   /// @param Eb \f$E_1\f$ in the formula
   LogParabola(double norm=1., double alpha=1., double beta=2., double Eb=100.);

   virtual Function * clone() const {
      return new LogParabola(*this);
   }

protected:

   double value(const optimizers::Arg &) const;

   double derivByParamImp(const optimizers::Arg & x,
                          const std::string & paramName) const;

};

} // namespace Likelihood

#endif // Likelihood_LogParabola_h
