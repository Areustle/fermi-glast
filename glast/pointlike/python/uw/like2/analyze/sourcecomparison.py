"""
Comparison with the 3FGL catalog

$Header: /glast/ScienceTools/glast/pointlike/python/uw/like2/analyze/Attic/sourcecomparison.py,v 1.1.2.1 2015/08/13 18:03:04 jasercio Exp $

"""

import os
from astro.io import fits as pyfits
import numpy as np
import pylab as plt
import pandas as pd

from skymaps import SkyDir
from . import sourceinfo

class SourceComparison(sourceinfo.SourceInfo):
    """Comparison with a FITS catalog, 2FGL or beyond
    """

    def setup(self, cat='3FGL-v13r3_v6r9p1_3lacv12p1_v7.fits', #'gll_psc4yearsource_v9_assoc_v6r3p0.fit', #gll_psc_v06.fit',
            catname='3FGL', **kw):
        super(SourceComparison, self).setup(**kw)
        self.catname=catname
        self.plotfolder='comparison_%s' % catname
        if not os.path.exists('plots/'+self.plotfolder):
            os.mkdir('plots/'+self.plotfolder)
        if cat[0]!='/':
            cat = os.path.expandvars('$FERMI/catalog/'+cat)
        assert os.path.exists(cat), 'Did not find file %s' %cat
        ft = pyfits.open(cat)[1].data
        self.ft=ft # temp
        print 'loaded FITS catalog file %s with %d entries' % (cat, len(ft))
        id_prob = [np.nan]*len(ft)
        try:
            id_prob = ft.ID_Probability_v6r9p1[:,0] ## should find that suffix
        except:
            print 'warning: id_prob not set'
        cat_skydirs = map (lambda x,y: SkyDir(float(x),float(y)), ft.RAJ2000, ft.DEJ2000)

        glat = [s.b() for s in cat_skydirs]
        glon = [s.l() for s in cat_skydirs]
        def nickfix(n):
            return n if n[:3]!='PSR' else 'PSR '+n[3:]
        index = map(nickfix, [x.strip() for x in ft.NickName_3FGL]) #Source_Name
        self.cat = pd.DataFrame(dict(name3=ft.Source_Name_3FGL_1,
                nickname=map(nickfix, ft.NickName_3FGL),
                ra=ft.RAJ2000,dec= ft.DEJ2000,
                ts=ft.Test_Statistic,
                skydir=cat_skydirs,
                glat=glat, glon=glon,
                #pivot=ft.Pivot_Energy, flux=ft.Flux_Density,
                #modelname=ft.SpectrumType,
                id_prob=id_prob,
                a95=ft.Conf_95_SemiMajor, b95=ft.Conf_95_SemiMinor, ang95=ft.Conf_95_PosAng,
                flags=np.asarray(ft.Flags_3FGL, int),
                ),
            columns = 'name3 nickname ra dec glat glon skydir ts a95 b95 ang95 id_prob flags'.split(), # this to order them
            index=index, )
        self.cat.index.name='name'
        self.cat['pt_flags'] = self.df.flags
        self.cat['pt_ts'] = self.df.ts
        self.cat['pt_ra'] = self.df.ra
        self.cat['pt_dec'] = self.df.dec

        def find_close(A,B):
            """ helper function: make a DataFrame with A index containg columns of the
            name of the closest entry in B, and its distance
            A, B : DataFrame objects each with a skydir column
            """
            def mindist(a):
                d = map(a.difference, B.skydir.values)
                n = np.argmin(d)
                return (B.index[n], np.degrees(d[n]))
            return pd.DataFrame( map(mindist,  A.skydir.values),
                index=A.index, columns=('otherid','distance'))

        if catname=='2FGL' or catname=='3FGL':
            print 'generating closest distance to catalog "%s"' % cat
            closedf= find_close(self.df, self.cat)
            self.df['closest']= closedf['distance']
            self.df['close_name']=closedf.otherid
            #closest = np.degrees(np.array([min(map(sdir.difference, cat_skydirs))for sdir in self.df.skydir.values]))
            #self.df['closest'] = closest
            closedf.to_csv(os.path.join('plots', self.plotfolder, 'comparison_%s.csv'%catname))
            closest2 = np.degrees(np.array([min(map(sdir.difference, self.df.skydir.values)) for sdir in cat_skydirs]))
            self.cat['closest']= closest2


    def distance_to_cat(self, maxdist=0.5, tscuts=[10,50,500], nbins=26):
        """Associations of sources with 2FGL

        """
        fig,ax = plt.subplots( figsize=(4,4))
        for tscut in tscuts:
            ax.hist(self.df.closest[self.df.ts>tscut].clip(0,maxdist), np.linspace(0,maxdist,nbins), log=True,
             label='TS>%d'%tscut)
        ax.grid()
        ax.legend(prop=dict(size=10))
        plt.setp(ax, xlabel='closest distance to %s source'%self.catname)
        return fig

    def lost_plots(self, close_cut=0.25, minassocprob=0.8, maxts=250):
        """3FGL sources not present in new list
        Histogram of the 3FGL catalog TS and Galactic latitude for those sources more than %(close_cut).2f deg from a skymodel source.
        The subset of sources with associations (prob>%(minassocprob)s) is shown. <br>
        Left: Distribution vs. TS.<br>
        Right: Distribution vs sine of Galactic latitude.
        """
        self.minassocprob=minassocprob
        self.close_cut = close_cut
        fig,axx = plt.subplots(1,2, figsize=(8,4))
        self.lost = self.cat.closest>close_cut
        print '%d sources from %s further than %.2f deg: consider lost' % (sum(self.lost) , self.catname, close_cut )
        self.cat.ix[self.lost].to_csv(os.path.join(self.plotfolder,'3fgl_lost.csv'))
        print '\twrite to file "%s"' % os.path.join(self.plotfolder,'3fgl_lost.csv')
        lost_assoc = self.lost & (self.cat.id_prob>0.8)

        def left(ax):
            space = np.linspace(0,maxts,21)
            ax.hist(self.cat.ts[self.lost].clip(0,maxts), space, label='all (%d)'%sum(self.lost))
            ax.hist(self.cat.ts[lost_assoc].clip(0,maxts), space, color='orange', label='associated(%d)' %sum(lost_assoc) )
            ax.legend(prop=dict(size=10))
            ax.grid()
            plt.setp(ax, xlabel='TS of %s source' %self.catname)

        def right(ax):
            space = np.linspace(-1,1,51)
            singlat = np.sin(np.radians(self.cat.glat))
            ax.hist(singlat[self.lost], space, label='all (%d)'%sum(self.lost))
            #lost_assoc = self.lost & (self.cat.id_prob>0.8)
            ax.hist(singlat[lost_assoc], space, color='orange', label='associated(%d)' %sum(lost_assoc) )
            ax.legend(prop=dict(size=10))
            ax.grid()
            plt.setp(ax, xlabel='sin(glat) of %s source' %self.catname, xlim=(-1,1))
            return fig
        for f, ax in zip((left,right), axx.flatten()):
            f(ax)
        return fig

    def poorly_localized(self):
        pass

    def all_plots(self):
        """Results of comparison with 3FGL catalog
        """
        self.runfigures([ self.distance_to_cat, self.lost_plots])

    def lookup_3fgl(self, name3):
        if name3[-1]!=' ' and name3[-1]!='c': name3=name3+' '
        fglnames = list(self.cat.name3)
        try:
            i = fglnames.index(name3)
            nick = self.cat.ix[i].name
            j=  list(self.df.close_name).index(nick)
            return self.df.ix[j]
        except Exception, msg:
            print 'Source %s not found (%s)' % (name3, msg)
            return None
