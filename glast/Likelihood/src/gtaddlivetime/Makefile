HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

HD_CXXTASK              = gtltsum

HD_CXXTASK_SRC_cxx      = gtaddlivetime.cxx

HD_CXXFLAGS             = ${HD_STD_CXXFLAGS}

HD_CXXLIBS              = ${HD_LFLAGS} \
                          ${GT_DATASUBSELECTOR_LIBS} \
                          ${GT_EVTBIN_LIBS} \
                          -lirfUtil \
                          ${GT_STD_CXXLIBS} \
			  -lgsl -lgslcblas -lhealpix_cxx -lc_utils -lcxxsupport -lfftpack -lsharp -lgomp -lwcs

HD_INSTALL_TASKS        = ${HD_CXXTASK}

HD_INSTALL_HELP         = gtltsum.txt

include ${HD_STD_MAKEFILE}
