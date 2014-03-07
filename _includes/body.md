In current biomedical research, fluorescence correlation spectroscopy (FCS) is  applied
to characterize molecular dynamic processes in vitro and in living cells.  Commercial
FCS setups only permit data analysis that is limited to  a specific instrument by
the use of in-house file formats or a  finite number of implemented correlation
model functions. PyCorrFit is a general-purpose FCS evaluation software that,
amongst other formats, supports the established Zeiss ConfoCor3 ~.fcs  file format.
PyCorrFit comes with several built-in model functions, covering a wide range of
applications in standard confocal FCS. In addition, it contains equations dealing
with different excitation geometries like total internal reflection (TIR).

#### Supported Operating Systems
- Any operating system with a Python 2.7 installation
- Binary support for:
  - Windows XP or higher
  - MacOSx 10.6 or higher
  - Ubuntu Linux [LTS](https://wiki.ubuntu.com/LTS)

#### Supported Filetypes
- [ALV-6000](http://www.alvgmbh.de/) correlator files (~.ALV) (single and multiple runs / tested in autocorrelation mode) 
- [Zeiss](http://microscopy.zeiss.com/microscopy/en_us/products/confocal-microscopes.html) Confocor3 files (~.fcs)
- [Correlator.com](http://correlator.com/) Flex correlators (~.SIN) 
- PyCorrFit (~.csv)  

#### Fitting
- Pre-defined model functions (confocal FCS, TIR-FCS, Triplet blinking, multiple components)
- Import of user-defined model functions 
- Global fitting across multiple model functions or data sets
- Least squares fit using the Levenberg-Marquard algorithm
- Weighted fitting with standard deviation
- Parameter error estimation 


#### Tools and Features
- Averaging of curves
- Background correction
- Batch processing
- Overlay tool to identify outliers
- Fast simulation of model parameter behavior
- Session management
- User-defined model functions
- High quality plot export using LaTeX (bitmap or vector graphics)


#### Verbosity
- Detailed [documentation](https://github.com/paulmueller/PyCorrFit/raw/master/PyCorrFit_doc.pdf)
- Included Python shell access
- Documented and structured [source](https://github.com/paulmueller/PyCorrFit/tree/master/src) code
- Access to all internal parameters of a measurement
- Update helper to for new program version
- Open source software; anyone can contribute


#### Screenshots
[ ![scrot](./images/Screenshot_Desktop_Win.png) ](./images/Screenshot_Desktop_Win.png "Desktop (Windows)")

[ ![scrot](./images/Screenshot_Desktop_Mac.png) ](./images/Screenshot_Desktop_Mac.png "Desktop (Mac OSx)")

[ ![scrot](./images/Screenshot_Desktop.png) ](./images/Screenshot_Desktop.png "Desktop (Ubuntu)")

[ ![scrot](./images/Screenshot_Desktop_Raspbian_Jessie.png) ](./images/Screenshot_Desktop_Raspbian_Jessie.png "PyCorrFit on the Raspberry Pi!")

[ ![scrot](./images/Screenshot_Main.png) ](./images/Screenshot_Main.png "Main Window")

[ ![scrot](./images/Screenshot_Graphics_output.png) ](./images/Screenshot_Graphics_output.png "Graphics  output  (matplotlib)")

[ ![scrot](./images/Screenshot_Select_curves.png) ](./images/Screenshot_Select_curves.png "Curve  selection")

[ ![scrot](./images/Screenshot_Trace_view.png) ](./images/Screenshot_Trace_view.png "Trace  view")
