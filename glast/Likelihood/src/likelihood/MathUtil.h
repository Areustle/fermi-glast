/**
 * @file MathUtil.h
 * @brief Declaration of MathUtil class.
 * @author Analia Cillis
 * $Header: /nfs/slac/g/glast/ground/cvs/ScienceTools-scons/Likelihood/src/likelihood/MathUtil.h,v 1.1 2006/09/14 20:39:40 peachey Exp $
 */
#ifndef MathUtil_h
#define MathUtil_h

/**
 * @class MathUtil
 * @brief Basic class containing poisson-related math (ln(gamma), gammaq etc.)
 */ 
class MathUtil {

public:
   static double gammln(double x);
   static void  gser(double *gamser, double a, double x, double *gln);
   static void  gcf(double *gammcf, double a, double x, double *gln);
   static double  gammq(double a, double x);
   static double poissonSig(double x, double mean);
};

#endif
