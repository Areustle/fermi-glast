/** 
 * @file RosenND.h
 * @brief Declaration for a N-dimesional Rosenbrock objective function
 * @author J. Chiang
 *
 * $Header: /nfs/slac/g/glast/ground/cvs/ScienceTools-scons/optimizers/src/RosenND.h,v 1.6 2015/03/21 05:36:46 jchiang Exp $
 */

#include "optimizers/Statistic.h"

namespace optimizers {
/** 
 * @class RosenND
 *
 * @brief A ND Rosenbrock test function
 *
 */
    
class RosenND : public Statistic {

public:

   RosenND(int ndim=3, double prefactor=100);

   virtual double value() const {
      Arg dummy;
      return value(dummy);
   }

   virtual void getFreeDerivs(std::vector<double> &derivs) const {
      Arg dummy;
      Function::getFreeDerivs(dummy, derivs);
   }

protected:

   virtual double value(const Arg &) const;

   virtual double derivByParamImp(const Arg &,
                                  const std::string &paramName) const;

   virtual Function * clone() const {
      return new RosenND(*this);
   }

private:

   int m_dim;

   double m_prefactor;


};

} // namespace optimizers

