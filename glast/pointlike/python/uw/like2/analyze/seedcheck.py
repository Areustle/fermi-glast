"""
Analyze seeds

$Header: /glast/ScienceTools/glast/pointlike/python/uw/like2/analyze/Attic/seedcheck.py,v 1.1.2.1 2015/08/13 18:03:04 jasercio Exp $

"""
import os
import numpy as np
import pylab as plt
import pandas as pd
import skymaps
from .. import associate
from . import sourceinfo, diagnostics, _html
from .analysis_base import FloatFormat

b12index = skymaps.Band(12).index

class SeedCheck(sourceinfo.SourceInfo):
    """Analysis of a set of seeds
    <br>
    <p>This is a second stage after a run that produced a residual TS map. The first pipeline run, "tables", generates nside=512 HEALPix 
    tables of the residual TS and kde plots. The plot analysis "hptables" that follows it does a cluster analysis, generating a list of
    seed positions in the file "seeds.txt". A second pipeline run, "seedcheck", for each ROI, adds seeds falling in the central pixel to the model, 
    performing an inital fit to the flux only, then a localization, and finally a full fit. The fit and localization information are 
    written to a set of pickle files in the folder "seedcheck" or the zip file "seedcheck.zip".
    A selection is applied with there cuts: 
    %(cut_summary)s
    <br>and the remaining sources are analyzed here.
    """
    require='seedcheck.zip'
    def setup(self, **kw):
        self.plotfolder = self.seedname='seedcheck'
        self.spectral_type='power law'
        self.load()
        
    def load(self):
        files, sources = self.load_pickles(self.seedname)
        sdict={}
        assoc={}
        for source in sources:
            name = source.name
            model = source.model
            pars = np.empty(4); pars.fill(np.nan)
            errs = np.empty(4); errs.fill(-2)
            free = np.zeros(4, bool)
            n = model.len()
            pars[:n] = model.parameters
            free[:n] = model.free
            try:
                diag = np.diag(model.get_cov_matrix())
                errs[:n] = [np.sqrt(x) if x>0 else -1 for x in diag[:n]]
                badfit = np.any(errs[model.free]<=0)
            except Exception, msg:
                print 'fail errors for %s:%s' % (name, msg)
                badfit = True
            has_adict = hasattr(source,'adict') and source.adict is not None
            has_ellipse = hasattr(source, 'ellipse') and source.ellipse is not None
            sdict[name] = dict(
                ra =source.skydir.ra(), dec=source.skydir.dec(),
                ts=source.ts,
                delta_ts=source.ellipse[6] if has_ellipse else np.nan,
                r95 = 2.6*source.ellipse[2] if has_ellipse else np.nan,
                locqual=source.ellipse[5] if has_ellipse else np.nan,
                glat=source.skydir.b(), glon=source.skydir.l(),
                eflux=pars[0] * model.e0**2 *1e6,
                eflux_unc=errs[0] * model.e0**2 *1e6 if errs[0]>0 else np.nan,
                pindex = pars[1],
                pindex_unc = errs[1] if errs[1]>0 else np.nan,
                par2 = pars[2],
                par2_unc = errs[2] if errs[2]>0 else np.nan,
                e0 = model.e0,
                aprob = source.adict['prob'][0] if has_adict else 0,
                index = b12index(source.skydir),
                #gflux  = model.i_flux(), ## photon flux
                )
            assoc[name] = dict(
                acat = source.adict['cat'][0] if has_adict else None,
                aname= source.adict['name'][0] if has_adict else None,
                adelta_ts = source.adict['deltats'][0] if has_adict else None,
                aprob = source.adict['prob'][0] if has_adict else 0.,
                adict = source.adict if has_adict else None,
                )
        self.df = pd.DataFrame(pd.DataFrame(sdict).transpose(), 
            columns="""ra dec glat glon ts ellipse delta_ts eflux eflux_unc 
                    pindex pindex_unc par2 par2_unc e0 r95 locqual aprob index""".split() 
            )
        self.df.index.name='name'
        
        # analyze associations, make summary
        self.assoc = pd.DataFrame(assoc).transpose()
        self.assoc.index.name = 'name'
        if all(self.assoc.aprob==0):
            print "No associations found: running the standard logic"
            try:
                self.make_associations()
            except Exception, msg:
                print 'Association attempt failed: %s' % msg
                raise
        else:
            print "Using associations from uwpipeline run"
        
        # define good subset
        self.good = (self.df.ts>6)&(self.df.r95<0.6)&(self.df.locqual<8)
        self.df_good= self.df[self.good]
        
#        self.test = self.df_good.ix[self.df_good.aprob>0.8]
        
        acat=list(self.df_good.ix[self.df_good.aprob>0.8]['acat'].values)
        sa = list(set(acat))
        t = np.zeros(len(sa),int)
        for x in acat:
            t[sa.index(x)]+=1
        self.assoc_sum = zip(sa, t)
        self.cut_summary= """<p>Read in %d sources from file %s: <br>selection cut:
                    (self.df.ts>6)*(self.df.r95<0.6)*(self.df.locqual<8) : %d remain"""\
            % (len(sources), self.require, sum(self.good))
        print self.cut_summary
    
    def make_associations(self):
        """ run the standard association logic 
            Only apply to "good" sources
        """
        srcid = associate.SrcId()
        assoc={}
        print 'Note: making bzcat first if second'
        for name, s in self.df.iterrows():
            has_ellipse=  not np.isnan(s['r95'])
            if has_ellipse: 
                try:
                    adict = srcid(name, skymaps.SkyDir(s['ra'],s['dec']), s['r95']/2.6)
                except Exception, msg:
                    print 'Failed association for source %s: %s' % (name, msg)
                    adict=None
                has_ellipse = adict is not None
                if has_ellipse:
                    cats = adict['cat']; probs = adict['prob']
                    i=1 if len(cats)>1 and \
                        cats[1]=='bzcat' and probs[1]>0.8\
                        or cats[0]=='cgrabs' else 0
            assoc[name] = ad = dict(
                    acat =  adict['cat'][i] if has_ellipse else None,
                    aname=  adict['name'][i] if has_ellipse else None,
                    adelta_ts = adict['deltats'][i] if has_ellipse else None,
                    aprob = adict['prob'][i] if has_ellipse else 0.,
                    adict = adict if has_ellipse else None,
                    )
        
        self.assoc = pd.DataFrame(assoc).transpose()
        self.assoc.index.name = 'name'
        for col in 'acat aname adelta_ts aprob adict'.split():
            self.df[col] = self.assoc[col]
    
    def seed_cumulative_ts(self, cut=None, label='all seeds'):
        """ Cumulative TS distribution for seeds 
        """
        v = self.df_good.ts
        if cut is not None: v=v[cut]
        fig = self.cumulative_ts(v, check_localized=False, label=label)
        ax = plt.gca()
        plt.setp(ax, ylim=(9,1000), xlim=(9,100))
        leg =ax.legend()
        pbox = leg.get_patches()[0]; pbox._height=0; pbox._y=5
        return fig
        
    def unassoc_seed_cumulative_ts(self):
        """ Cumulative TS distribution for seed sources that are not associated
        """
        return self.seed_cumulative_ts(cut=self.assoc.aprob<0.8, label='unassociated')
        
    def histo(self, ax, v, bins):
        ax.hist(v, bins)
        ts = np.array(self.df_good.ts)
        ax.hist(v[ts>10], bins, label='TS>10')
        ax.hist(v[ts>25], bins, label='TS>25')
        ax.legend(prop=dict(size=10))
        ax.grid()
    
    def localization(self):
        """ Localization results
        <br>Left: r95; right; delta TS
        """
        fig, ax = plt.subplots(1,3, figsize=(12,5))
        plt.subplots_adjust(left=0.1)
        df = self.df_good
        def r95(ax):
            v = 60.*df.r95; bins = np.linspace(0, 25,26)
            self.histo(ax, v[~pd.isnull(v)], bins)
            plt.setp(ax, xlabel='r95 (arcmin)')
        def delta_ts(ax):
            v = np.sqrt(list(df.delta_ts)); bins = np.linspace(0,10,26)
            self.histo(ax, v, bins)
            plt.setp(ax, xlabel='sqrt(delta_ts)', xlim=(0,3))
        def locqual(ax):
            self.histo(ax, df.locqual.clip(0,8), np.linspace(0,8,26))
            plt.setp(ax, xlabel='localization quality', xlim=(0,8))
        for f, a in zip((r95, delta_ts,locqual), ax.flatten()):
            f(a)
        return fig

    def spectral_parameters(self, ax=None, index_lim=(1.5,3.0), flux_lim=(0.05,5)):
        """ Spectral fit parameters
        Flux vs. spectral index for %(spectral_type)s fit
        <br>histograms of sin(glat) and sqrt(delta_ts) for all, TS>10, and TS>25
        """
        fig, ax = plt.subplots(1,2, figsize=(10,5))
        df = self.df_good
        good = df.ts>10
        super = df.ts>25
        def flux_index(ax, ylim=index_lim, xlim=flux_lim):
            for cut, c,label in zip((good, super), ('.b', 'or'), ('TS>10', 'TS>25')):
                ax.plot(df.eflux[cut].clip(*xlim), df.pindex[cut].clip(*ylim), c, label=label)
            ax.grid()
            ax.legend(loc='lower right', prop=dict(size=10))
            plt.setp(ax, ylim=ylim, xlim=xlim, xscale='log', ylabel='spectral index', xlabel='Energy flux [eV]')
        def singlat(ax):
            v = np.sin(np.radians(list(df.glat))); bins=np.linspace(-1,1,26)
            self.histo(ax, v, bins)
            plt.setp(ax, xlabel='sin(glat)')
        def skyplot(ax):
            glon = df.glon
            glon[glon>180]-=360
            ax.plot(glon, np.sin(np.radians(list(df.glat))), 'o')
            plt.setp(ax, xlim=(180,-180), xlabel='glon', ylabel='sin(glat)')
        def index_vs_cutoff(ax):
            cutoff = df.par2
            for tsmin, marker in zip((10,25), ('.b', 'or')):
                cut = df.ts>tsmin
                ax.plot(cutoff[cut], df.pindex[cut],  marker, label='TS>%d'%tsmin)
            plt.setp(ax, ylabel='spectral index', xlabel='cutoff', ylim=(0.5,3.0), xlim=(0, 3000))
            ax.grid(); ax.legend( prop=dict(size=10))
        for f, a in zip((flux_index,  singlat,), ax.flatten()):
            f(a)
            
        return fig

    def locations(self, vmin=10, vmax=50):
        """ Positions
        Locations of the good candidates. Colors show TS value.
        """
        fig, ax = plt.subplots(figsize=(10,8))
        return self.skyplot(self.df_good.ts, ax=ax, vmin=vmin, vmax=vmax, cbtext='TS', s=50)
    
    def seed_list(self):
        """ Results of analysis of seeds
        %(info)s
        <p>A <a href="../../%(csv_file)s?download=true">csv file</a> is also available.
        """
        cols="""ra	dec	glon glat		ts		eflux	pindex r95	
            delta_ts locqual aprob acat aname index""".split()
        t = self.df_good[cols].sort_index(by='index')
        good_seeds = 'good_seeds.csv'
        self.csv_file = os.path.join(self.plotfolder,good_seeds)
        t.to_csv(self.csv_file)
        print 'wrote list that succeeded to %s' % self.csv_file
        filename = 'good_seeds.html'
        html_file = self.plotfolder+'/%s' % filename
        htmldoc = diagnostics.html_table(t, float_format=diagnostics.FloatFormat(2))
        open(html_file,'w').write('<head>\n'+ _html.style + '</head>\n<body>'+ htmldoc+'\n</body>')

        self.info = self.df_good['ts eflux pindex r95 locqual aprob'.split()].describe().to_html(float_format=FloatFormat(2)).replace('%', '%%')
        self.info += '<p><a href="%s?skipDecoration">Table of %d seeds</a> '% (filename, len(t))
        if len(self.assoc_sum)>0:
            self.info += '<p>Association summary for good seeds' 
            t = pd.DataFrame(self.assoc_sum, columns='catalog associations'.split()).sort_index(by='catalog')
            self.info += t.to_html(index=False)
            # Make a summary of the AGN types 
            ta=self.assoc[self.assoc.aprob>0.8]
            bznames = np.array(ta.aname[ta.acat=='bzcat'])
            if len(bznames!=0):
                self.info+='<p>BZCAT AGN type summary'
                bztypes = set([name[3] for name in bznames])
                td = dict()       
                for t in bztypes:
                    td[t]= 0
                for n in bznames:
                    t = n[3]
                    td[t] +=1
                self.info += pd.DataFrame(td.items(), columns='type count'.split()).to_html(index=False)
        else:
            self.info += '<p>No associations found'

    def all_plots(self):
        self.runfigures([self.seed_list, self.seed_cumulative_ts, self.locations, self.spectral_parameters, self.localization,])
