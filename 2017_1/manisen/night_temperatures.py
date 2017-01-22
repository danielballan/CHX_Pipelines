def night_series(temperatures=[150,130,110,80,190,175],repeats=3):
	x0=1.37
	xr=.02
	yr=.03
	for i in temperatures:		# change temperature
		set_temperature(i)
		try:
			olog_client.log( 'Changed temperature to T='+ str(caget('XF:11IDB-ES{Env:01-Out:1}T-SP')-273.15)[:5]+'C')
		except:
			pass
		print('changed temperature to '+str(i)+'C  ' +time.ctime() + ':   going to sleep....')
		if i==150:
			sleep(2000)
		elif i==190:
			sleep(3600)
		else: sleep(1800)
		movr(diff.yh,yr)			# setup sample spot
		mov(diff.xh,x0)
		check_cryo()
		check_recover()         # check ring and beamline -> beam on DBPM when done
		fast_sh.close()
		diode_OUT()
		for m in range(repeats):
			movr(diff.xh,xr);series(shutter_mode='single',expt=.00134,acqp='auto',imnum=500,comment='500fr 1.34ms 0s period T='+str(i)+'  repeat: '+str(m))
			movr(diff.xh,xr);series(shutter_mode='multi',expt=.00134,acqp=.05,imnum=500,comment='500fr 1.34ms 0.05s period T='+str(i)+'  repeat: '+str(m))
			movr(diff.xh,xr);series(shutter_mode='multi',expt=.00134,acqp=.2,imnum=500,comment='500fr 1.34ms 0.2s period T='+str(i)+'  repeat: '+str(m))
			movr(diff.xh,xr);series(shutter_mode='multi',expt=.00134,acqp=1.,imnum=200,comment='200fr 1.34ms 1s period T='+str(i)+'  repeat: '+str(m))
			movr(diff.xh,xr);series(shutter_mode='multi',expt=.00134,acqp=5.,imnum=100,comment='100fr 1.34ms 5s period T='+str(i)+'  repeat: '+str(m))
			feedback_ON()
			sleep(30)
			check_cryo()
			check_recover()
			fast_sh.close()
			diode_OUT()
		feedback_ON()
	set_temperature(25)


		
