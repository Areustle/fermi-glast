HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

HD_TEST_TASKS           = test_GRBobs

HD_TEST_CXXTASK         = ${HD_TEST_TASKS}

HD_TEST_CXXTASK_SRC_cxx	= testGRB.cxx

HD_CXXFLAGS             = ${HD_STD_CXXFLAGS}

HD_CXXLIBS              = ${HD_LFLAGS} \
                          -lGRBobs \
                          -lSpectObj \
                          -leblAtten \
                          ${GT_FLUX_LIBS} \
                          ${GT_XML_LIBS} \
                          ${GT_STD_CXXLIBS} \
			  -lwcs -lgsl -lgslcblas -lhealpix_cxx -lc_utils -lcxxsupport -lfftpack -lsharp -lgomp

include ${HD_STD_MAKEFILE}
