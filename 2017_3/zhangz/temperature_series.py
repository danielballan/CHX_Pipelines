def goto_newspot(xstep=.025,ystep=-.025):
	RE(mvr(diff.xh,xstep))
	if diff.xh.user_readback.value > -0.78:
		RE(mv(diff.xh,-1.1))
		RE(mvr(diff.yh,ystep))

def XPCS_slowseries(T=-100,repeat=1):
	att2.set_T(1E-3)
	series(expt=5,imnum=300,acqp='auto',comment='5s + 300 @ '+str(T)+'C repeat: '+str(repeat)+' transmission: '+str(att2.calc_T(1E-3)[1])  + RE.md['sample'],feedback_on=True)
	

#for PEO4K at lower temperature <=44, transmission=0.2, 1000 frames, exp=0.01

def XPCS_fastseries(T=-100,repeat=1, transmission= 0.036 ): 
	att2.set_T(transmission)
	RE.md['transmission']=att2.calc_T(transmission)[1]
	series(expt=.01,imnum=5000,acqp='auto',comment='.01s + 5.0k @ '+str(T)+'C repeat: '+str(repeat)+' transmission: '+str(att2.calc_T(transmission)[1])  + RE.md['sample'],feedback_on=True)

def XPCS_flyseries(T=-100,repeat=1, transmission= 0.036 ):
	att2.set_T(transmission)
	RE.md['transmission']=att2.calc_T(transmission)[1]
	series(expt=.00134,imnum=10000,acqp='auto',comment='.00134s + 10.0k @ '+str(T)+'C repeat: '+str(repeat)+' transmission: '+str(att2.calc_T(transmission)[1])  + RE.md['sample'],feedback_on=True)


def XPCS_shutterseries(T=-100,repeat=1):
	RE(mv(foil_x,-18.5))  #Sets a transmission of 0.036 at 9.65 keV
	series(shutter_mode='multi',expt=.2,imnum=200,acqp=5.,comment='0.2s 5s period + 200fr @ '+str(T)+'C repeat: '+str(repeat)+'  ' + RE.md['sample'],feedback_on=False)    
	

def XPCS_slowseries(T=-100,repeat=1,expt=1, imnum=100, transmission= 0.00024): #0.0013 ): 
	att2.set_T(transmission)
	RE.md['transmission']=att2.calc_T(transmission)[1]
	#imnum = 100
	#expt= 7.04 #1.3
	series(expt=expt,imnum=imnum,acqp='auto',comment=str(expt) +'s %s k @'%(imnum/1000) +str(T)+'C repeat: '+str(repeat)+' transmission: '+str(att2.calc_T(transmission)[1])  + RE.md['sample'],feedback_on=True)


def sample_temp_dose_series(Temperatures=[ 95, 105, 115, 125, 135, 145, 155, 165, 175, 185],
                  transmission= [ 0.19, 0.036, 0.0068,   0.0068, 1.3e-3, 1.3e-3 ][::-1],
                        imnum = [ 100,  100,    600,     1250,    3000,  6500][::-1],
                            repeats=2, wait_time=600):
	for temp in Temperatures:
		set_temperature(temp)
		check_bl()  # this will result in the feedback ON + diodqe IN
		wait_temperature(wait_time=wait_time)
		sample_dose_series( transmission= transmission, imnum=imnum,
                                repeats=repeats,dose=0.25*100*0.0068,  temp= temp )
		
def sample_dose_series( transmission= [ 0.19, 0.036, 0.0068, 1.3e-3, 2.4e-4][::-1],
repeats=1,dose=0.25*100*0.0068, temp= 75,   imnum=100 ):
        """Use the same dose, dose in unit of sec.frame.transmission,
                 For +Li PEO4K@36K, no beam damage dose is: 0.25 sec * 100 frame * 0.0068 trans

                 available transmission= [ 0.19, 0.036, 0.0068, 1.3e-3, 2.4e-4, 4.7e-5]
        """
        i = 0
        for t in transmission:
                #set_CHAB()
                check_bl()  # this will result in the feedback ON + diodqe IN
                bring_bpm_back()
                t_ = att2.calc_T(t)[1]
                if isinstance(imnum, int):
                        expt = dose/( t_ * imnum )
                        imnum_ = imnum
                else:
                        imnum_ = imnum[i]
                        expt = dose/(t_*imnum_)
                i += 1
                        
                for rep in range(repeats):
                        check_recover()
                        fast_sh.close() # get ready for measurements
                        goto_newspot()
                        XPCS_slowseries(T=temp,repeat=rep,  imnum=imnum_, expt=expt, transmission=t_)
        check_bl()
        bring_bpm_back()
 
                

def set_CHAB():
        for i in range(2):                
                caput( 'XF:11IDB-BI{XBPM:02}CtrlDAC:ALevel-SP', 4.2)
                caput( 'XF:11IDB-BI{XBPM:02}CtrlDAC:BLevel-SP', 5.2)
                time.sleep(3)
        
        print("Set CHA/CHB!!!")
        
def bring_bpm_back():
        if not caget('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP'):
                print('Bring BPM back here!!!')
                set_CHAB()
                caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',1)  #put HDM feedback on
                time.sleep(60)
                caput('XF:11IDA-OP{Mir:HDM-Ax:P}Sts:FB-Sel',0)        
                time.sleep(5)
                for i in range(20):
                        caput('XF:11IDB-BI{XBPM:02}Fdbk:AEn-SP',1)
                        caput('XF:11IDB-BI{XBPM:02}Fdbk:BEn-SP',1)
                        time.sleep(20)
        

def sample_one_dose( transmission=  0.036, repeats=2, dose=0.25*100*0.0068, imnum= 250, temp= 65 ):
        """
        available transmission= [ 0.19, 0.036, 0.0068, 1.3e-3, 2.4e-4, 4.7e-5]
        """
        t = transmission
        #set_CHAB()
        check_bl()  # this will result in the feedback ON + diodqe IN
        bring_bpm_back()               
        t_ = att2.calc_T(t)[1]
        expt = dose/( t_ * imnum )        
        for rep in range(repeats):
                check_recover()
                fast_sh.close() # get ready for measurements
                goto_newspot()
                XPCS_slowseries(T=temp,repeat=rep, imnum=imnum, expt=expt, transmission=t_)
        check_bl()         
        bring_bpm_back()

                


                

def sample_series(Temperatures=[85,120,140,160,180],repeats=2,wait_time=1200):
	for temp in Temperatures:
		set_temperature(temp)
		check_bl()  # this will result in the feedback ON + diodqe IN
		wait_temperature(wait_time=wait_time)
		for rep in range(repeats):
			check_recover()
			fast_sh.close() # get ready for measurements
			goto_newspot()
			XPCS_slowseries(T=temp,repeat=rep)
			#goto_newspot()
			#XPCS_fastseries(T=temp,repeat=rep)
			#goto_newspot()
			#XPCS_flyseries(T=temp,repeat= rep )

		 
	#set_temperature(25,cool_ramp=0)
			

