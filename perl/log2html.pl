#!/usr/bin/perl 

#Little Program to open a log file, then output a html file for online viewing.
#Declaration of global variables (yes I know this is bad...)
$numofargs = $#ARGV + 1;
$directory = "$ARGV[0]";
$infile = "$ARGV[1]";
$out_dir = "$ARGV[2]";

# Debug to make sure first command line argument is passed into the function
#print "First Argument from command line: $infile \n";
#$test = $#infile;
#print "# of command line arguments: $test\n";

#print "DEBUG CODE:\n";
#print "Directory: $directory\n";
#print "Infile: $infile\n";
#print "Output Directory: $out_dir\n";
#print "END DEBUG CODE.\n";

#Main portion of program where all subs will be called.
#&get_log_names();

if ($numofargs < 3) {

	$errormsg = "Please Enter the Directory for the log file, the File, ";
	$errormsg .= "and the output directory (e.g. \"./log2html.pl /var/log/ messages /userhome/html/\")\n";
	print $errormsg;
} else {
	print "\nCalling Function to parse log files into HTML";
	&parse_log_files($directory, $infile, $out_dir);
}

##Portion of the program used to declare subs.
##Subroutine to get all of the log names from a directory NOT CURRENTLY USED##
##sub get_log_names() {
##	opendir(DIR, "/var/log/") || die "Couldn't open Log directory: $!\n";
##	@logfiles = readdir(DIR);
##	closedir(DIR);
##	return @logfiles;
##}

sub parse_log_files() {
	($directory, $infile, $out_dir) = @_;
	#####DEBUG CODE#####
	#print "Infile in function: $infile\n";
	###END DEBUG CODE###
	print "\nOpening File: $infile\n";
	open(INFILE, "$directory" . "$infile") || die "Couldn't open file: $!\n";
	if((-B INFILE) || (-x INFILE)){
		print "Sorry Cannot Parse Binary Files.\n";
		exit;
	} else {
		print "Copying $infile into temporary array for parsing...\n";
		@int_log = <INFILE>;
		#Normal basic HTML header to write to beginning of file.
		  $header = "<html>\n<head>\n<title>Testing log2html parser...</title>\n</head>\n<br>\n<body>\n";
		#Lets make a pretty table with all the data, so it appears all nice and neat
		  $table = "<table border=4 align=top>\n";
		  $table .= "<tr><th align=left>Date  Time  Host  Message</th></td></tr><tr>\n";
		    print "Adding HTML header to $infile...\n";
		    open (OUTFILE, ">$out_dir" . "$infile" . "\.html");
		    seek (OUTFILE, 0, 0);
		    print OUTFILE $header;
		    print OUTFILE $table;
		foreach $line (@int_log) {
		    chomp($line);
		    print OUTFILE "<tr><td>$line<br>\n";
		}
		#print OUTFILE @int_log;
		  seek (OUTFILE, -1, -1);
		#Close out the table.
		  $end_table = "\n</tr>\n</td>\n</table>\n";
		#Close off the HTML.
		  print "Adding HTML footer to $infile...\n";
		  $footer = "<br>\n</body>\n</html>\n<br>\n<br>";
		print "Writing file $infile as $infile\.html in $out_dir directory...finished.\n\n";
		print OUTFILE $end_table;
		print OUTFILE $footer;
	}
	close(INFILE);
	close(OUTFILE);
}
