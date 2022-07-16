#!/bin/bash
echo "netlib_adlittle"
python3 lp_solver.py < test_LPs_volume1/input/netlib_adlittle.txt
echo
echo "netlib_afiro"
python3 lp_solver.py < test_LPs_volume1/input/netlib_afiro.txt
echo
echo "netlib_bgprtr"
python3 lp_solver.py < test_LPs_volume1/input/netlib_bgprtr.txt
echo
echo "netlib_itest2"
python3 lp_solver.py < test_LPs_volume1/input/netlib_itest2.txt
echo
echo "netlib_itest6"
python3 lp_solver.py < test_LPs_volume1/input/netlib_itest6.txt
echo
echo "netlib_klein1"
python3 lp_solver.py < test_LPs_volume1/input/netlib_klein1.txt
echo
echo "netlib_klein2"
python3 lp_solver.py < test_LPs_volume1/input/netlib_klein2.txt
echo
echo "netlib_sc50a"
python3 lp_solver.py < test_LPs_volume1/input/netlib_sc50a.txt
echo
echo "netlib_sc50b"
python3 lp_solver.py < test_LPs_volume1/input/netlib_sc50b.txt
echo