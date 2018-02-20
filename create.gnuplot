#!/usr/bin/gnuplot -p

set output "/tmp/thymba2_bot/temperature"
set terminal png font 'Hack,17' size 1640,1350
# enhanced background rgb 'white' 

set multiplot layout 2,1
#set xlabel "Orario"
set ylabel "Temperature"

set key right top
set key horizontal right
set key box opaque spacing 2

set tmargin 2
set rmargin 7
set lmargin 10
set bmargin 2

set xtics 30*60
set xtics nomirror
set ytics nomirror
set offset 0, 0, 0, 4

set xdata time
set style data lines
set timefmt "\"%Y-%m-%d %H:%M:%S\""
set yrange [30:70]
set format x "%H:%M\n%d-%m"

plot "/tmp/thymba2_bot/measurements.dat" using 1:2 title 'thermal zone0' lw 3
#
set bmargin 4
set yrange [600:1200]
set ylabel "Frequency"
set ytics 100
set offset 0,0,150,50

plot "/tmp/thymba2_bot/measurements.dat" using 1:3 title 'core0' lw 3 , \
	'' u 1:4 title 'core1' lw 3 lc rgb 'green', \
	'' u 1:5 title 'core2' lw 3 lc rgb 'red', \
	'' u 1:6 title 'core3' lw 3 lc rgb 'blue'

# vim: set ts=4 sw=4 tw=120 noet :
