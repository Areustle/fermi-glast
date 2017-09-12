HD_COMPONENT_NAME       = glast

HD_COMPONENT_VERS       =

# NOTE: These package subdirectories are in dependency order. That is,
# packages later in the list depend upon successful builds of packages
# earlier in the list. As new packages are added, this ordering should
# be maintained.

HD_SUBDIRS              = embed_python \
                          facilities \
                          tip \
                          astro \
                          BayesianBlocks \
                          st_facilities \
                          st_stream \
                          st_graph \
                          st_app \
                          xmlBase \
                          irfs \
                          healpix \
                          flux \
                          optimizers \
                          celestialSources \
                          catalogAccess \
                          evtbin \
                          burstFit \
                          dataSubselector \
                          map_tools \
                          Likelihood \
                          evtUtils \
                          fitsGen \
                          observationSim \
			  observationSim/pfiles \
                          orbitSim \
                          rspgen \
                          sourceIdentify \
                          timeSystem \
                          pulsarDb \
                          periodSearch \
                          pulsePhase \
                          bin.perl \
                          pyBurstAnalysisGUI \
                          pyExposure \
                          pyLikelihood \
                          gtobspsf \
                          PyPsf \
                          sane \
                          SolarSystemTools

HD_TEST_SUBDIRS         = embed_python \
                          facilities \
                          tip \
                          astro \
                          st_facilities \
                          st_stream \
                          st_graph \
                          st_app \
                          xmlBase \
                          irfs \
                          healpix \
                          flux \
                          optimizers \
                          celestialSources \
                          catalogAccess \
                          evtbin \
                          burstFit \
                          dataSubselector \
                          map_tools \
                          Likelihood \
                          orbitSim \
                          fitsGen \
                          observationSim \
                          rspgen \
                          timeSystem \
                          pulsarDb \
                          periodSearch \
                          pulsePhase \
                          test-scripts

ROOT_DEPENDANT			= evtUtils \
				  fitsGen \
				  observationSim

HD_CLEAN                = ${HD_BLD_EXEC_PFX} ${HD_BLD_PFX}

HD_DISTCLEAN            = config.cache \
                          config.log \
                          config.status \
                          configure.lineno \
                          cxxtest.out \
                          fortest.out \
                          hd_install \
                          headas-setup \
                          hmakerc

HD_CTASK                = hd_install

HD_CTASK_SRC_c          = hd_install.c

HD_CFLAGS		= ${CFLAGS}

HD_INSTALL_TASKS        = hd_install

HD_INSTALL_SHELL_SCRIPTS = hd_scanenv hmake

HD_INSTALL_EXTRA        = install-BUILD_DIR

include ${HD_STD_MAKEFILE}

# Custom target to prevent recursion to Root-specific packages as apppropriate.
subdir:
	exclude=`echo ${HD_SUBDIR} | sed -e 's:/.*::'`; \
	if [ "x${BUILD_WITHOUT_ROOT}" != "xyes" -o `echo ${ROOT_DEPENDANT} | grep -c $$exclude` -eq 0 -o `echo "observationSim/pfiles" | grep -xc ${HD_SUBDIR}` -eq 1 ]; then \
	  ${HD_MAKE} ${HD_TARG_PFX}subdir; \
	fi

# Install BUILD_DIR; tap dance needed because the built tools live in BUILD_DIR
#------------------------------------------------------------------------------
install-BUILD_DIR:
	@${HD_INSTALL} ${HD_BUILD_DIR} ${HD_EXEC_PFX}/BUILD_DIR ${HD_CP_P}
