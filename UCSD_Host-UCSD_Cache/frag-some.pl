#!/usr/bin/perl

system("ls -la");

my ($sample, $offset, $id, $count, $reqs) = @ARGV;

print "frag-some.pl --- ", join("   ", ($sample, $offset, $id, $count, $reqs)), "\n";

$PREF = "root://xrootd.t2.ucsd.edu:2050/";
$BASE = "./";
$XFCP = "${BASE}/xrdfragcp";
$SMPL = "${BASE}/${sample}";

open SS, $SMPL or die "Can not open $SMPL sample list.";
while (my $line = <SS>)
{
  chomp $line;
  my ($path, $size) = split /\s+/, $line;
  push @ss, $path;
}
close SS;

my $sss = $#ss + 1;

my $rd_size = $reqs * 1024 * 1024 * 20;   # 20 MB ...
my $rd_reqs = $reqs;
my $rd_time = $reqs * 10;                 # Per 10 seconds

print "Read $sss lines from $SMPL.\n";

system("ls -l");

$beg = $offset + $id * $count;
for ($i = $beg; $i < $beg + $count; ++$i)
{
  my $fid = $i % $sss;
  my $url = $PREF . $ss[$fid];
  my $cmd = "$XFCP";    # Removed strace
  $cmd .= " --verbose";
  $cmd .= " --cmsclientsim $rd_size $rd_reqs $rd_time ";
  $cmd .= $url;


  print("going to run $cmd\n");
  system("$cmd ");
  print("job ended\n");
};

