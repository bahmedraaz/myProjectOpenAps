import pytest
import telex.synth
import pandas

#templogicdata =  'G[0,6] F[b? 1;6,  a? 4;6](x1 > 2)'
templogicdata =  [
#	'G[0,299](((bg>=120)&(bg_1-bg>=th?0;8))->(rate_1-rate>=0))'
#	'G[0,299](((bg>=120)&(delBg>=th?0;8))->(delRate>=0))'
#	'G[0,20] (((bg<=290)&(IOB>1.65))->(rate<=a?1;4))'
#	'G[0,299] (((bg>120)&(delRate<0))->(delBg<=a?-10;10))' #working
#	'G[0,299] (((bg>120)&(delRate<0))->(delIOB<=a?-10;10))'#working
#	'G[0,299] (((bg>120)&(delRate<0))->(IOB<=a?-10;10))'#working

#	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB>0)))->(delBg<=a?-10;10))' # row_1, this gives threshold for delBG. If delBG > a, then decreasing rate will be hazard
	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB>0)))->(IOB>=a?-10;10))' # row_1, this gives threshold for IOB. If IOB < a, then decreasing rate will cause hazard
	
#	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB<0)))->(delBg<=a?-10;10))' # row_2
#	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB<0)))->(IOB>=a?-10;10))' # row_2
	
#	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB>0)))->(bg>=a?0;300))'
#	'G[0,299] ((((bg>120)&(delBg>0))&((delRate<0)&(delIOB>0)))->(bg<=a?0;300))'
	
#	'G[0,299] ((((bg>120)&(delBg>0))&(delRate<0))->(IOB>=a?-10;10))'
#	'G[0,299] ((((bg>120)&(delBg>0))&(delRate<0))->(delIOB>=a?-10;10))'
#	'G[0,299] ((((bg>120)&(delBg>0))&(delRate<0))->(IOB>=a?-10;10))'

#	'G[0,299] ((((bg>120)&(delIOB<0))&(delRate<0))->(IOB>=a?-10;10))'

#	'G[0,299]((bg>=120)->(delRate<=a?-5;5))'
#	'G[0,299]((bg>=120)->((rate-rate_1)<=a?-5;5))' # Does not work, you have to subtract rate_1 from rate beforehand and create new column named delRate(for example)
#	'G[0,50] F[0,299] bg<a?1;300'
#    'G[b? 1;6,  a? 1;9](x1 > 2)',
#    'G[0,5] F[a? 0;3, b? 0;5] (x1 > 2)',
#    'G[0,5] F[1, b? 0;5] (x1 > 2)',
#    'G[0,5] F[a? 0;2 , 2] (x1 > 2)',
#    'G[0,5] F[a? 1;2 , 3] (x1 > 2)',
#    'G[0,9] ({ x1 - x2 } < a? -2;8 )',
#    'G[0,9] ({ x2 - x1 } < a? -2;8 )',
#    'U[0,a? 0;2] (x1 <= 10, x2<=5)',
#    'U[0,2] (x1 > b? 0;5, x2 > 1)',
]

@pytest.mark.parametrize("tlStr", templogicdata)
def test_stl(tlStr):
    print(tlStr)
    try:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "participant0")
    except ValueError:
        (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "participant0", "nogradient")
    print(" Synthesized STL formula: {}\n Theta Optimal Value: {}\n Optimization time: {}\n".format(stlsyn, value, dur))
    (bres, qres) = telex.synth.verifySTL(stlsyn, "participant0")
    print(" Test result of synthesized STL on each trace: {}\n Robustness Metric Value: {}\n".format(bres, qres))
#    print(tlStr)
#    (stlsyn, value, dur) = telex.synth.synthSTLParam(tlStr, "traces")
#    print(stlsyn, value, dur)
#    (bres, qres) = telex.synth.verifySTL(stlsyn, "traces")
#    print(bres, qres)


def main():
    for templ in templogicdata:
        test_stl(templ)

if __name__ == "__main__":
    main()

