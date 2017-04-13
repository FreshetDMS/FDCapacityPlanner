# random read (128MB file)

## libaio

```
poisson-rate-submit: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=32
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit: Laying out IO file (1 file / 128MiB)
Jobs: 1 (f=1): [r(1)][96.8%][r=4480KiB/s,w=0KiB/s][r=1120,w=0 IOPS][eta 00m:02s]
poisson-rate-submit: (groupid=0, jobs=1): err= 0: pid=25009: Wed Apr 12 17:07:12 2017
   read: IOPS=532, BW=2129KiB/s (2180kB/s)(128MiB/61567msec)
    slat (usec): min=4, max=65905, avg=20.27, stdev=426.32
    clat (usec): min=79, max=752463, avg=60073.68, stdev=71744.33
     lat (usec): min=95, max=752480, avg=60094.29, stdev=71748.22
    clat percentiles (usec):
     |  1.00th=[  185],  5.00th=[  382], 10.00th=[  466], 20.00th=[ 5856],
     | 30.00th=[12992], 40.00th=[22912], 50.00th=[35072], 60.00th=[50432],
     | 70.00th=[70144], 80.00th=[101888], 90.00th=[156672], 95.00th=[205824],
     | 99.00th=[321536], 99.50th=[374784], 99.90th=[489472], 99.95th=[544768],
     | 99.99th=[667648]
    lat (usec) : 100=0.15%, 250=1.28%, 500=9.12%, 750=1.04%, 1000=0.50%
    lat (msec) : 2=2.23%, 4=3.19%, 10=8.59%, 20=11.39%, 50=22.38%
    lat (msec) : 100=19.44%, 250=17.99%, 500=2.61%, 750=0.08%, 1000=0.01%
  cpu          : usr=0.00%, sys=0.94%, ctx=32310, majf=0, minf=3
  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=32768,0,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=32

Run status group 0 (all jobs):
   READ: bw=2129KiB/s (2180kB/s), 2129KiB/s-2129KiB/s (2180kB/s-2180kB/s), io=128MiB (134MB), run=61567-61567msec

Disk stats (read/write):
  xvdca: ios=32451/9533, merge=28/15, ticks=1959740/146344, in_queue=2106936, util=99.98%
```

## psync

```
poisson-rate-submit: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=32
fio-2.19-12-gb94d
Starting 1 process
Jobs: 1 (f=1): [r(1)][100.0%][r=5409KiB/s,w=0KiB/s][r=1352,w=0 IOPS][eta 00m:00s]
poisson-rate-submit: (groupid=0, jobs=1): err= 0: pid=25046: Wed Apr 12 17:09:50 2017
   read: IOPS=535, BW=2144KiB/s (2195kB/s)(128MiB/61148msec)
    clat (usec): min=78, max=1013.8k, avg=59671.74, stdev=72293.79
     lat (usec): min=89, max=1013.8k, avg=59691.03, stdev=72298.48
    clat percentiles (usec):
     |  1.00th=[  189],  5.00th=[  382], 10.00th=[  474], 20.00th=[ 6112],
     | 30.00th=[13248], 40.00th=[22400], 50.00th=[34048], 60.00th=[48896],
     | 70.00th=[69120], 80.00th=[99840], 90.00th=[156672], 95.00th=[205824],
     | 99.00th=[321536], 99.50th=[374784], 99.90th=[522240], 99.95th=[585728],
     | 99.99th=[716800]
    lat (usec) : 100=0.08%, 250=1.32%, 500=9.06%, 750=0.88%, 1000=0.50%
    lat (msec) : 2=2.13%, 4=3.17%, 10=8.51%, 20=12.01%, 50=23.01%
    lat (msec) : 100=19.21%, 250=17.38%, 500=2.62%, 750=0.10%, 1000=0.01%
    lat (msec) : 2000=0.01%
  cpu          : usr=0.95%, sys=0.00%, ctx=32305, majf=0, minf=3
  IO depths    : 1=100.0%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=32768,0,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=32

Run status group 0 (all jobs):
   READ: bw=2144KiB/s (2195kB/s), 2144KiB/s-2144KiB/s (2195kB/s-2195kB/s), io=128MiB (134MB), run=61148-61148msec

Disk stats (read/write):
  xvdca: ios=32746/9479, merge=21/12, ticks=1953444/141684, in_queue=2095268, util=99.96%
```

## Sequential write (2G)

```
poisson-rate-submit: (g=0): rw=write, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=psync, iodepth=32
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit: Laying out IO file (1 file / 2048MiB)
poisson-rate-submit: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit: (groupid=0, jobs=1): err= 0: pid=18229: Wed Apr 12 17:22:18 2017
  write: IOPS=6466, BW=25.3MiB/s (26.5MB/s)(1831MiB/72506msec)
    clat percentiles (usec):
     |  1.00th=[    0],  5.00th=[    0], 10.00th=[    0], 20.00th=[    0],
     | 30.00th=[    0], 40.00th=[    0], 50.00th=[    0], 60.00th=[    0],
     | 70.00th=[    0], 80.00th=[    0], 90.00th=[    0], 95.00th=[    0],
     | 99.00th=[    0], 99.50th=[    0], 99.90th=[    0], 99.95th=[    0],
     | 99.99th=[    0]
  cpu          : usr=5.05%, sys=9.69%, ctx=519246, majf=0, minf=522
  IO depths    : 1=111.8%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=0,468859,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=32

Run status group 0 (all jobs):
  WRITE: bw=25.3MiB/s (26.5MB/s), 25.3MiB/s-25.3MiB/s (26.5MB/s-26.5MB/s), io=1831MiB (1920MB), run=72506-72506msec

Disk stats (read/write):
  xvdca: ios=0/538201, merge=0/84, ticks=0/104484, in_queue=104456, util=81.28%
```

## Sequential write (20G-128k-1f-poisson)

```
poisson-rate-submit-20G-write-1f: (g=0): rw=write, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-write-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-write-1f: (groupid=0, jobs=1): err= 0: pid=18280: Wed Apr 12 17:30:24 2017
  write: IOPS=995, BW=124MiB/s (131MB/s)(18.8GiB/154407msec)
    clat (usec): min=393, max=256436, avg=1000.94, stdev=4073.88
     lat (usec): min=394, max=256437, avg=1002.59, stdev=4073.91
    clat percentiles (usec):
     |  1.00th=[  426],  5.00th=[  438], 10.00th=[  454], 20.00th=[  478],
     | 30.00th=[  524], 40.00th=[  668], 50.00th=[  700], 60.00th=[  708],
     | 70.00th=[  732], 80.00th=[  740], 90.00th=[  852], 95.00th=[ 1400],
     | 99.00th=[ 8768], 99.50th=[13888], 99.90th=[71168], 99.95th=[74240],
     | 99.99th=[88576]
    lat (usec) : 500=27.08%, 750=58.80%, 1000=6.01%
    lat (msec) : 2=6.70%, 4=0.10%, 10=0.51%, 20=0.40%, 50=0.17%
    lat (msec) : 100=0.22%, 250=0.01%, 500=0.01%
  cpu          : usr=0.43%, sys=1.99%, ctx=153814, majf=0, minf=10
  IO depths    : 1=106.5%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=0,153780,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
  WRITE: bw=124MiB/s (131MB/s), 124MiB/s-124MiB/s (131MB/s-131MB/s), io=18.8GiB (20.2GB), run=154407-154407msec

Disk stats (read/write):
  xvdca: ios=0/517742, merge=0/102, ticks=0/568268, in_queue=568264, util=99.30%
```

## Sequential write (20G-128k-1f-linear)

```
poisson-rate-submit-20G-write-1f: (g=0): rw=write, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-write-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-write-1f: (groupid=0, jobs=1): err= 0: pid=18287: Wed Apr 12 17:37:11 2017
  write: IOPS=990, BW=124MiB/s (130MB/s)(18.9GiB/155329msec)
    clat (usec): min=386, max=183193, avg=1006.61, stdev=4025.51
     lat (usec): min=388, max=183194, avg=1008.18, stdev=4025.53
    clat percentiles (usec):
     |  1.00th=[  414],  5.00th=[  430], 10.00th=[  442], 20.00th=[  466],
     | 30.00th=[  540], 40.00th=[  668], 50.00th=[  700], 60.00th=[  708],
     | 70.00th=[  732], 80.00th=[  740], 90.00th=[  924], 95.00th=[ 1400],
     | 99.00th=[ 8768], 99.50th=[13888], 99.90th=[72192], 99.95th=[74240],
     | 99.99th=[84480]
    lat (usec) : 500=26.98%, 750=57.36%, 1000=6.15%
    lat (msec) : 2=8.13%, 4=0.08%, 10=0.47%, 20=0.43%, 50=0.15%
    lat (msec) : 100=0.24%, 250=0.01%
  cpu          : usr=0.26%, sys=1.67%, ctx=153867, majf=0, minf=10
  IO depths    : 1=106.5%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=0,153867,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
  WRITE: bw=124MiB/s (130MB/s), 124MiB/s-124MiB/s (130MB/s-130MB/s), io=18.9GiB (20.2GB), run=155329-155329msec

Disk stats (read/write):
  xvdca: ios=0/518318, merge=0/70, ticks=0/543432, in_queue=543432, util=99.54%
```

## Sequential read (20G-128k-1f-r100w0-poission)

```
poisson-rate-submit-20G-r100w0-1f: (g=0): rw=read, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r100w0-1f: Laying out IO file (1 file / 20480MiB)
poisson-rate-submit-20G-r100w0-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r100w0-1f: (groupid=0, jobs=1): err= 0: pid=18293: Wed Apr 12 17:45:40 2017
   read: IOPS=1137, BW=142MiB/s (149MB/s)(18.7GiB/134068msec)
    clat (usec): min=372, max=359015, avg=878.18, stdev=3771.10
     lat (usec): min=372, max=359016, avg=878.35, stdev=3771.10
    clat percentiles (usec):
     |  1.00th=[  398],  5.00th=[  434], 10.00th=[  652], 20.00th=[  676],
     | 30.00th=[  700], 40.00th=[  708], 50.00th=[  716], 60.00th=[  732],
     | 70.00th=[  740], 80.00th=[  748], 90.00th=[  796], 95.00th=[ 1400],
     | 99.00th=[ 1464], 99.50th=[ 2576], 99.90th=[34048], 99.95th=[104960],
     | 99.99th=[150528]
    lat (usec) : 500=6.53%, 750=75.32%, 1000=9.35%
    lat (msec) : 2=8.23%, 4=0.30%, 10=0.11%, 20=0.04%, 50=0.05%
    lat (msec) : 100=0.02%, 250=0.05%, 500=0.01%
  cpu          : usr=0.08%, sys=2.41%, ctx=152453, majf=0, minf=9
  IO depths    : 1=107.5%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=152452,0,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=142MiB/s (149MB/s), 142MiB/s-142MiB/s (149MB/s-149MB/s), io=18.7GiB (19.1GB), run=134068-134068msec

Disk stats (read/write):
  xvdca: ios=491260/16412, merge=0/23, ticks=333252/149544, in_queue=482796, util=98.82%
```

## Sequential rw (20G-128k-1f-r95w5-poisson)

```
poisson-rate-submit-20G-r95w5-1f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r95w5-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r95w5-1f: (groupid=0, jobs=1): err= 0: pid=18354: Wed Apr 12 18:02:43 2017
  mixed: IOPS=1217, BW=152MiB/s (160MB/s)(18.5GiB/124267msec)
    clat (usec): min=372, max=425691, avg=820.17, stdev=3210.21
     lat (usec): min=372, max=425691, avg=820.44, stdev=3210.21
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  434], 10.00th=[  466], 20.00th=[  604],
     | 30.00th=[  668], 40.00th=[  700], 50.00th=[  708], 60.00th=[  732],
     | 70.00th=[  748], 80.00th=[  748], 90.00th=[  804], 95.00th=[ 1400],
     | 99.00th=[ 1464], 99.50th=[ 1512], 99.90th=[25984], 99.95th=[67072],
     | 99.99th=[150528]
    lat (usec) : 500=14.87%, 750=64.80%, 1000=12.50%
    lat (msec) : 2=7.55%, 4=0.05%, 10=0.10%, 20=0.03%, 50=0.01%
    lat (msec) : 100=0.07%, 250=0.02%, 500=0.01%
  cpu          : usr=0.30%, sys=2.20%, ctx=151247, majf=0, minf=11
  IO depths    : 1=108.3%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=151247,0,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
  MIXED: bw=152MiB/s (160MB/s), 152MiB/s-152MiB/s (160MB/s-160MB/s), io=18.5GiB (19.9GB), run=124267-124267msec

Disk stats (read/write):
  xvdca: ios=466425/25084, merge=0/26, ticks=302952/14812, in_queue=317764, util=99.11%
```

## Sequential rw (20G-128k-1f-r95w5-poisson)

### Separate

```
poisson-rate-submit-20G-r95w5-1f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r95w5-1f: Laying out IO file (1 file / 20480MiB)
poisson-rate-submit-20G-r95w5-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r95w5-1f: (groupid=0, jobs=1): err= 0: pid=18348: Wed Apr 12 17:55:48 2017
   read: IOPS=1169, BW=146MiB/s (153MB/s)(17.6GiB/122784msec)
    clat (usec): min=374, max=242658, avg=825.76, stdev=2909.07
     lat (usec): min=374, max=242659, avg=825.95, stdev=2909.07
    clat percentiles (usec):


[poisson-rate-submit-20G-r90w10-1f]
     |  1.00th=[  394],  5.00th=[  426], 10.00th=[  466], 20.00th=[  668],
     | 30.00th=[  684], 40.00th=[  700], 50.00th=[  716], 60.00th=[  732],
     | 70.00th=[  748], 80.00th=[  748], 90.00th=[  788], 95.00th=[ 1400],
     | 99.00th=[ 1448], 99.50th=[ 1480], 99.90th=[18816], 99.95th=[67072],
     | 99.99th=[148480]
  write: IOPS=62, BW=8035KiB/s (8228kB/s)(964MiB/122784msec)
    clat (usec): min=413, max=138728, avg=523.71, stdev=2182.96
     lat (usec): min=415, max=138730, avg=525.53, stdev=2182.97
    clat percentiles (usec):
     |  1.00th=[  426],  5.00th=[  450], 10.00th=[  454], 20.00th=[  462],
     | 30.00th=[  466], 40.00th=[  470], 50.00th=[  474], 60.00th=[  482],
     | 70.00th=[  486], 80.00th=[  498], 90.00th=[  516], 95.00th=[  540],
     | 99.00th=[  636], 99.50th=[  716], 99.90th=[ 1816], 99.95th=[16768],
     | 99.99th=[138240]
    lat (usec) : 500=15.35%, 750=66.34%, 1000=10.65%
    lat (msec) : 2=7.41%, 4=0.01%, 10=0.09%, 20=0.04%, 50=0.01%
    lat (msec) : 100=0.07%, 250=0.02%
  cpu          : usr=0.22%, sys=2.35%, ctx=151248, majf=0, minf=9
  IO depths    : 1=108.3%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=143539,7708,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=146MiB/s (153MB/s), 146MiB/s-146MiB/s (153MB/s-153MB/s), io=17.6GiB (18.9GB), run=122784-122784msec
  WRITE: bw=8035KiB/s (8228kB/s), 8035KiB/s-8035KiB/s (8228kB/s-8228kB/s), io=964MiB (1010MB), run=122784-122784msec

Disk stats (read/write):
  xvdca: ios=466356/25085, merge=0/26, ticks=298516/13900, in_queue=312416, util=98.99%
```

## Sequential rw (20G-128k-1f-r90w10-poisson)

### Separate

```angular2html
poisson-rate-submit-20G-r90w10-1f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r90w10-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r90w10-1f: (groupid=0, jobs=1): err= 0: pid=18411: Wed Apr 12 18:21:49 2017
   read: IOPS=1093, BW=137MiB/s (143MB/s)(16.7GiB/124586msec)
    clat (usec): min=371, max=206046, avg=855.57, stdev=3445.57
     lat (usec): min=371, max=206047, avg=855.76, stdev=3445.57
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  418], 10.00th=[  438], 20.00th=[  502],
     | 30.00th=[  652], 40.00th=[  684], 50.00th=[  708], 60.00th=[  724],
     | 70.00th=[  748], 80.00th=[  748], 90.00th=[  812], 95.00th=[ 1384],
     | 99.00th=[ 1464], 99.50th=[ 1576], 99.90th=[67072], 99.95th=[73216],
     | 99.99th=[142336]
  write: IOPS=122, BW=15.3MiB/s (16.4MB/s)(1905MiB/124586msec)
    clat (usec): min=404, max=31516, avg=509.20, stdev=535.82
     lat (usec): min=406, max=31518, avg=511.04, stdev=535.83
    clat percentiles (usec):
     |  1.00th=[  426],  5.00th=[  450], 10.00th=[  454], 20.00th=[  462],
     | 30.00th=[  466], 40.00th=[  470], 50.00th=[  478], 60.00th=[  482],
     | 70.00th=[  494], 80.00th=[  510], 90.00th=[  548], 95.00th=[  604],
     | 99.00th=[  844], 99.50th=[ 1004], 99.90th=[ 1928], 99.95th=[14528],
     | 99.99th=[31104]
    lat (usec) : 500=25.27%, 750=55.76%, 1000=12.02%
    lat (msec) : 2=6.58%, 4=0.05%, 10=0.10%, 20=0.04%, 50=0.03%
    lat (msec) : 100=0.13%, 250=0.02%
  cpu          : usr=0.37%, sys=2.25%, ctx=151517, majf=0, minf=9
  IO depths    : 1=108.1%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=136275,15241,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=137MiB/s (143MB/s), 137MiB/s-137MiB/s (143MB/s-143MB/s), io=16.7GiB (17.9GB), run=124586-124586msec
  WRITE: bw=15.3MiB/s (16.4MB/s), 15.3MiB/s-15.3MiB/s (16.4MB/s-16.4MB/s), io=1905MiB (1998MB), run=124586-124586msec

Disk stats (read/write):
  xvdca: ios=441813/49381, merge=0/26, ticks=295480/23156, in_queue=318636, util=98.77%
```

## Sequential (20G-128k-1f-r80w20-poisson)

```
poisson-rate-submit-20G-r80w20-1f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r80w20-1f: Laying out IO file (1 file / 20480MiB)
poisson-rate-submit-20G-r80w20-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r80w20-1f: (groupid=0, jobs=1): err= 0: pid=18421: Wed Apr 12 18:32:33 2017
   read: IOPS=948, BW=119MiB/s (124MB/s)(14.9GiB/128048msec)
    clat (usec): min=371, max=171999, avg=917.98, stdev=4415.14
     lat (usec): min=371, max=172000, avg=918.17, stdev=4415.15
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  410], 10.00th=[  422], 20.00th=[  442],
     | 30.00th=[  474], 40.00th=[  548], 50.00th=[  660], 60.00th=[  700],
     | 70.00th=[  732], 80.00th=[  748], 90.00th=[  788], 95.00th=[ 1256],
     | 99.00th=[ 1480], 99.50th=[ 4896], 99.90th=[67072], 99.95th=[75264],
     | 99.99th=[132096]
  write: IOPS=237, BW=29.8MiB/s (31.2MB/s)(3802MiB/128048msec)
    clat (usec): min=400, max=166868, avg=535.53, stdev=1975.85
     lat (usec): min=402, max=166870, avg=537.43, stdev=1975.84
    clat percentiles (usec):
     |  1.00th=[  426],  5.00th=[  446], 10.00th=[  454], 20.00th=[  462],
     | 30.00th=[  466], 40.00th=[  470], 50.00th=[  478], 60.00th=[  482],
     | 70.00th=[  494], 80.00th=[  516], 90.00th=[  564], 95.00th=[  636],
     | 99.00th=[  892], 99.50th=[ 1080], 99.90th=[ 2448], 99.95th=[ 8768],
     | 99.99th=[129536]
    lat (usec) : 500=42.59%, 750=41.93%, 1000=10.29%
    lat (msec) : 2=4.66%, 4=0.08%, 10=0.11%, 20=0.04%, 50=0.02%
    lat (msec) : 100=0.27%, 250=0.02%
  cpu          : usr=0.00%, sys=2.63%, ctx=151878, majf=0, minf=11
  IO depths    : 1=107.9%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=121464,30414,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=119MiB/s (124MB/s), 119MiB/s-119MiB/s (124MB/s-124MB/s), io=14.9GiB (15.1GB), run=128048-128048msec
  WRITE: bw=29.8MiB/s (31.2MB/s), 29.8MiB/s-29.8MiB/s (31.2MB/s-31.2MB/s), io=3802MiB (3986MB), run=128048-128048msec

Disk stats (read/write):
  xvdca: ios=392983/98375, merge=0/26, ticks=283296/44484, in_queue=327780, util=98.79%
```

## Sequential (20G-128k-1f-r70w30-poisson)

```angular2html
poisson-rate-submit-20G-r70w30-1f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r70w30-1f: Laying out IO file (1 file / 20480MiB)
poisson-rate-submit-20G-r70w30-1f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r70w30-1f: (groupid=0, jobs=1): err= 0: pid=18462: Wed Apr 12 18:48:39 2017
   read: IOPS=802, BW=100MiB/s (105MB/s)(13.7GiB/132700msec)
    clat (usec): min=367, max=428806, avg=1012.24, stdev=5735.58
     lat (usec): min=367, max=428806, avg=1012.43, stdev=5735.58
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  406], 10.00th=[  410], 20.00th=[  426],
     | 30.00th=[  438], 40.00th=[  450], 50.00th=[  470], 60.00th=[  540],
     | 70.00th=[  676], 80.00th=[  724], 90.00th=[  764], 95.00th=[  916],
     | 99.00th=[ 1480], 99.50th=[63744], 99.90th=[74240], 99.95th=[75264],
     | 99.99th=[150528]
  write: IOPS=344, BW=43.3MiB/s (45.2MB/s)(5710MiB/132700msec)
    clat (usec): min=402, max=224877, avg=537.57, stdev=2335.08
     lat (usec): min=403, max=224881, avg=539.60, stdev=2335.09
    clat percentiles (usec):
     |  1.00th=[  426],  5.00th=[  446], 10.00th=[  450], 20.00th=[  458],
     | 30.00th=[  466], 40.00th=[  470], 50.00th=[  474], 60.00th=[  478],
     | 70.00th=[  486], 80.00th=[  498], 90.00th=[  532], 95.00th=[  572],
     | 99.00th=[  748], 99.50th=[  892], 99.90th=[ 4896], 99.95th=[21120],
     | 99.99th=[116224]
    lat (usec) : 500=63.15%, 750=26.94%, 1000=6.70%
    lat (msec) : 2=2.57%, 4=0.04%, 10=0.08%, 20=0.05%, 50=0.04%
    lat (msec) : 100=0.39%, 250=0.03%, 500=0.01%
  cpu          : usr=0.59%, sys=2.13%, ctx=152235, majf=0, minf=10
  IO depths    : 1=107.6%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=106553,45679,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=100MiB/s (105MB/s), 100MiB/s-100MiB/s (105MB/s-105MB/s), io=13.7GiB (13.1GB), run=132700-132700msec
  WRITE: bw=43.3MiB/s (45.2MB/s), 43.3MiB/s-43.3MiB/s (45.2MB/s-45.2MB/s), io=5710MiB (5987MB), run=132700-132700msec

Disk stats (read/write):
  xvdca: ios=343600/147370, merge=0/27, ticks=271496/64964, in_queue=336580, util=98.81%
```

## Sequential (20G-128k-2f-r70w30-poisson)

```
poisson-rate-submit-20G-r70w30-2f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r70w30-2f: Laying out IO files (2 files / total 20480MiB)
poisson-rate-submit-20G-r70w30-2f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r70w30-2f: (groupid=0, jobs=1): err= 0: pid=18469: Wed Apr 12 18:58:11 2017
   read: IOPS=513, BW=64.3MiB/s (67.4MB/s)(13.4GiB/213265msec)
    clat (usec): min=373, max=305820, avg=1677.74, stdev=5540.89
     lat (usec): min=374, max=305820, avg=1677.94, stdev=5540.89
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  406], 10.00th=[  410], 20.00th=[  418],
     | 30.00th=[  430], 40.00th=[  442], 50.00th=[  454], 60.00th=[  470],
     | 70.00th=[  494], 80.00th=[  556], 90.00th=[ 3760], 95.00th=[ 9152],
     | 99.00th=[26240], 99.50th=[36608], 99.90th=[51456], 99.95th=[87552],
     | 99.99th=[152576]
  write: IOPS=220, BW=27.6MiB/s (28.9MB/s)(5866MiB/213265msec)
    clat (usec): min=413, max=273505, avg=621.74, stdev=2989.11
     lat (usec): min=414, max=273508, avg=623.99, stdev=2989.12
    clat percentiles (usec):
     |  1.00th=[  442],  5.00th=[  466], 10.00th=[  490], 20.00th=[  506],
     | 30.00th=[  516], 40.00th=[  516], 50.00th=[  524], 60.00th=[  532],
     | 70.00th=[  548], 80.00th=[  572], 90.00th=[  636], 95.00th=[  716],
     | 99.00th=[  940], 99.50th=[ 1176], 99.90th=[ 8768], 99.95th=[27264],
     | 99.99th=[154624]
    lat (usec) : 500=55.21%, 750=34.95%, 1000=2.11%
    lat (msec) : 2=0.48%, 4=0.36%, 10=3.97%, 20=1.91%, 50=0.92%
    lat (msec) : 100=0.05%, 250=0.04%, 500=0.01%
  cpu          : usr=0.23%, sys=1.71%, ctx=156470, majf=0, minf=10
  IO depths    : 1=104.7%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=109533,46931,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=64.3MiB/s (67.4MB/s), 64.3MiB/s-64.3MiB/s (67.4MB/s-67.4MB/s), io=13.4GiB (14.4GB), run=213265-213265msec
  WRITE: bw=27.6MiB/s (28.9MB/s), 27.6MiB/s-27.6MiB/s (28.9MB/s-28.9MB/s), io=5866MiB (6151MB), run=213265-213265msec

Disk stats (read/write):
  xvdca: ios=343980/147590, merge=0/88, ticks=462824/78488, in_queue=541348, util=99.16%
```

## Sequential (20G-128k-3f-r70w30-poisson)

```angular2html
poisson-rate-submit-20G-r70w30-3f: (g=0): rw=rw, bs=(R) 128KiB-128KiB, (W) 128KiB-128KiB, (T) 128KiB-128KiB, ioengine=psync, iodepth=1
fio-2.19-12-gb94d
Starting 1 process
poisson-rate-submit-20G-r70w30-3f: Laying out IO files (3 files / total 20479MiB)
poisson-rate-submit-20G-r70w30-3f: No I/O performed by psync, perhaps try --debug=io option for details?

poisson-rate-submit-20G-r70w30-3f: (groupid=0, jobs=1): err= 0: pid=18486: Wed Apr 12 19:06:09 2017
   read: IOPS=448, BW=56.5MiB/s (58.8MB/s)(13.5GiB/245717msec)
    clat (usec): min=376, max=243214, avg=1939.93, stdev=5330.44
     lat (usec): min=376, max=243214, avg=1940.13, stdev=5330.44
    clat percentiles (usec):
     |  1.00th=[  394],  5.00th=[  406], 10.00th=[  410], 20.00th=[  422],
     | 30.00th=[  430], 40.00th=[  442], 50.00th=[  458], 60.00th=[  474],
     | 70.00th=[  498], 80.00th=[  572], 90.00th=[ 6624], 95.00th=[10432],
     | 99.00th=[24704], 99.50th=[31104], 99.90th=[44800], 99.95th=[58112],
     | 99.99th=[156672]
  write: IOPS=192, BW=24.1MiB/s (25.2MB/s)(5900MiB/245717msec)
    clat (usec): min=422, max=211393, avg=670.84, stdev=3401.81
     lat (usec): min=424, max=211396, avg=673.09, stdev=3401.81
    clat percentiles (usec):
     |  1.00th=[  450],  5.00th=[  466], 10.00th=[  490], 20.00th=[  506],
     | 30.00th=[  516], 40.00th=[  524], 50.00th=[  532], 60.00th=[  540],
     | 70.00th=[  548], 80.00th=[  572], 90.00th=[  628], 95.00th=[  716],
     | 99.00th=[ 1160], 99.50th=[ 4192], 99.90th=[19584], 99.95th=[91648],
     | 99.99th=[156672]
    lat (usec) : 500=53.76%, 750=34.83%, 1000=1.37%
    lat (msec) : 2=0.36%, 4=0.41%, 10=5.29%, 20=2.88%, 50=1.03%
    lat (msec) : 100=0.03%, 250=0.04%
  cpu          : usr=0.00%, sys=1.70%, ctx=157383, majf=0, minf=10
  IO depths    : 1=104.1%, 2=0.0%, 4=0.0%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwt: total=110177,47198,0, short=0,0,0, dropped=0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=1

Run status group 0 (all jobs):
   READ: bw=56.5MiB/s (58.8MB/s), 56.5MiB/s-56.5MiB/s (58.8MB/s-58.8MB/s), io=13.5GiB (14.5GB), run=245717-245717msec
  WRITE: bw=24.1MiB/s (25.2MB/s), 24.1MiB/s-24.1MiB/s (25.2MB/s-25.2MB/s), io=5900MiB (6186MB), run=245717-245717msec

Disk stats (read/write):
  xvdca: ios=343797/147539, merge=0/50, ticks=532440/85024, in_queue=617464, util=99.26%
```