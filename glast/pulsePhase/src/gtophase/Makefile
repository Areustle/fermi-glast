HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

HD_CXXTASK              = gtophase

HD_CXXTASK_SRC_cxx      = gtophase.cxx

HD_CXXFLAGS             = ${HD_STD_CXXFLAGS}

HD_CXXLIBS              = ${HD_LFLAGS} \
                          ${GT_PULSEPHASE_LIBS} \
                          ${GT_PULSARDB_LIBS} \
                          ${GT_TIMESYSTEM_LIBS} \
                          ${GT_STD_CXXLIBS} \
			  -lwcs -lgsl -lgslcblas -lhealpix_cxx -lc_utils -lcxxsupport -lfftpack -lsharp -lgomp

HD_INSTALL_TASKS        = ${HD_CXXTASK}

HD_INSTALL_HELP         = gtophase.txt

include ${HD_STD_MAKEFILE}
