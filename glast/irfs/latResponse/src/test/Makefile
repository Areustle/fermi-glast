HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

HD_TEST_TASKS           = test_latResponse

HD_TEST_CXXTASK         = ${HD_TEST_TASKS}

HD_TEST_CXXTASK_SRC_cxx	= test.cxx

HD_CXXFLAGS             = ${HD_STD_CXXFLAGS}

HD_CXXLIBS              = ${HD_LFLAGS} \
                          -llatResponse \
                          -lirfUtil \
                          -lirfInterface \
                          ${GT_CPPUNIT_LIBS} \
                          ${GT_STD_CXXLIBS} \
			  -lwcs -lgsl -lgslcblas -lhealpix_cxx -lc_utils -lcxxsupport -lfftpack -lsharp -lgomp

include ${HD_STD_MAKEFILE}

#Do not change this.  It is needed to work around the behavior
#of make when using the test target and a file named test.cxx
test:
	${HD_MAKE} ${HD_TEST_CXXTASK}
