HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

HD_CXXTASK              = gtpsf

HD_CXXTASK_SRC_cxx      = meanPsf.cxx

HD_CXXFLAGS             = ${HD_STD_CXXFLAGS} -fpermissive

HD_CXXLIBS              = ${HD_LFLAGS} \
                          ${GT_LIKELIHOOD_LIBS} \
			  -leblAtten \
                          ${GT_MAP_TOOLS_LIBS} \
                          ${GT_DATASUBSELECTOR_LIBS} \
                          ${GT_EVTBIN_LIBS} \
                          ${GT_OPT_LIBS} \
                          ${GT_HEALPIX_LIBS} \
                          -lirfLoader \
                          -lirfInterface \
                          -lirfUtil \
                          -llatResponse \
                          -ldc1aResponse \
                          -ltestResponse \
                          ${GT_XML_LIBS} \
                          ${GT_FFT_LIBS} \
                          ${GT_STD_CXXLIBS} \
			  -lwcs -lgsl -lgslcblas -lhealpix_cxx -lc_utils -lcxxsupport -lfftpack -lsharp -lgomp

HD_INSTALL_TASKS        = ${HD_CXXTASK}

HD_INSTALL_HELP         = gtpsf.txt

include ${HD_STD_MAKEFILE}
