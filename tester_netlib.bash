#!/bin/bash
echo "netlib_adlittle"
python3 lp_solver.py < test_LPs_volume1/input/netlib_adlittle.txt

echo \n"netlib_afiro"
python3 lp_solver.py < test_LPs_volume1/input/netlib_afiro.txt
echo \n"netlib_bgprtr"
python3 lp_solver.py < test_LPs_volume1/input/netlib_bgprtr.txt

echo \n"netlib_itest2"
python3 lp_solver.py < test_LPs_volume1/input/netlib_itest2.txt

echo \n"netlib_itest6"
python3 lp_solver.py < test_LPs_volume1/input/netlib_itest6.txt

echo \n"netlib_klein1"
python3 lp_solver.py < test_LPs_volume1/input/netlib_klein1.txt
echo \n"netlib_klein2"
python3 lp_solver.py < test_LPs_volume1/input/netlib_klein2.txt

echo \n"netlib_sc50a"
python3 lp_solver.py < test_LPs_volume1/input/netlib_sc50a.txt

echo \n"netlib_sc50b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_sc50b.txt

echo \n"netlib_sc50b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_sc105.txt
echo \n"netlib_sc50b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_scagr7.txt

echo \n"netlib_share1b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_share1b.txt
echo \n"netlib_share2b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_share2b.txt
echo \n"netlib_stocfor1"
python3 lp_solver.py < test_LPs_volume1/input/netlib_stocfor1.txt
